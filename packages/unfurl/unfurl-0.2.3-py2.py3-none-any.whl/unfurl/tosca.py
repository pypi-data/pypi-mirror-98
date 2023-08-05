# Copyright (c) 2020 Adam Souzis
# SPDX-License-Identifier: MIT
"""
TOSCA implementation
"""
from .tosca_plugins import TOSCA_VERSION
from .util import UnfurlError, UnfurlValidationError, getBaseDir
from .eval import Ref, RefContext, mapValue
from .result import ResourceRef, ResultsList
from .merge import patchDict
from . import getLogLevel
from toscaparser.tosca_template import ToscaTemplate
from toscaparser.properties import Property
from toscaparser.elements.entity_type import EntityType
from toscaparser.elements.statefulentitytype import StatefulEntityType
import toscaparser.workflow
import toscaparser.imports
import toscaparser.artifacts
from toscaparser.common.exception import ExceptionCollector
import six
import logging
from ruamel.yaml.comments import CommentedMap

logger = logging.getLogger("unfurl")

from toscaparser import functions


class RefFunc(functions.Function):
    def result(self):
        return {self.name: self.args}

    def validate(self):
        pass


for func in ["eval", "ref", "get_artifact", "has_env", "get_env"]:
    functions.function_mappings[func] = RefFunc

toscaIsFunction = functions.is_function


def is_function(function):
    return toscaIsFunction(function) or Ref.isRef(function)


functions.is_function = is_function


def findStandardInterface(op):
    if op in StatefulEntityType.interfaces_node_lifecycle_operations:
        return "Standard"
    elif op in ["check", "discover", "revert"]:
        return "Install"
    elif op in StatefulEntityType.interfaces_relationship_configure_operations:
        return "Configure"
    else:
        return ""


def createDefaultTopology():
    tpl = dict(
        tosca_definitions_version=TOSCA_VERSION,
        topology_template=dict(
            node_templates={"_default": {"type": "tosca.nodes.Root"}},
            relationship_templates={"_default": {"type": "tosca.relationships.Root"}},
        ),
    )
    return ToscaTemplate(yaml_dict_tpl=tpl)


class ToscaSpec(object):
    ConfiguratorType = "unfurl.nodes.Configurator"
    InstallerType = "unfurl.nodes.Installer"

    def _overlay(self, overlays):
        def _findMatches():
            ExceptionCollector.start()  # clears previous errors
            for expression, _tpl in overlays.items():
                try:
                    match = Ref(expression).resolveOne(
                        RefContext(self.topology, trace=0)
                    )
                    if not match:
                        continue
                    if isinstance(match, ResultsList):
                        for item in match:
                            yield (item, _tpl)
                    else:
                        yield (match, _tpl)
                except:
                    ExceptionCollector.appendException(
                        UnfurlValidationError(
                            'error evaluating decorator match expression "%s"'
                            % expression,
                            True,
                        )
                    )

        matches = list(_findMatches())

        def _patch(m):
            node = m[0]
            tpl = node.toscaEntityTemplate.entity_tpl
            patch = mapValue(m[1], RefContext(node, dict(template=tpl)))
            return patchDict(tpl, patch, True)

        return [_patch(m) for m in matches]

    def _parseTemplate(self, path, inputs, toscaDef, resolver):
        # need to set a path for the import loader
        self.template = ToscaTemplate(
            path=path,
            parsed_params=inputs,
            yaml_dict_tpl=toscaDef,
            import_resolver=resolver,
            verify=False,
        )

        self.nodeTemplates = {}
        self.installers = {}
        self.relationshipTemplates = {}
        for template in self.template.nodetemplates:
            nodeTemplate = NodeSpec(template, self)
            if template.is_derived_from(self.InstallerType):
                self.installers[template.name] = nodeTemplate
            self.nodeTemplates[template.name] = nodeTemplate
        if hasattr(self.template, "relationship_templates"):
            # user-declared RelationshipTemplates, source and target will be None
            for template in self.template.relationship_templates:
                relTemplate = RelationshipSpec(template, self)
                self.relationshipTemplates[template.name] = relTemplate
        self.loadImportedDefaultTemplates()
        self.topology = TopologySpec(self, inputs)
        self.loadWorkflows()
        self.groups = {
            g.name: GroupSpec(g, self) for g in self.template.topology_template.groups
        }
        self.policies = {
            p.name: PolicySpec(p, self)
            for p in self.template.topology_template.policies
        }

    def __init__(
        self,
        toscaDef,
        spec=None,
        path=None,
        resolver=None,
    ):
        self.discovered = None
        if spec:
            inputs = spec.get("inputs")
        else:
            inputs = None

        if isinstance(toscaDef, ToscaTemplate):
            self.template = toscaDef
        else:
            topology_tpl = toscaDef.get("topology_template")
            if not topology_tpl:
                toscaDef["topology_template"] = dict(
                    node_templates={}, relationship_templates={}
                )

            if spec:
                self.loadInstances(toscaDef, spec)

            logger.info("Validating TOSCA template at %s", path)
            self._parseTemplate(path, inputs, toscaDef, resolver)
            decorators = self.loadDecorators()
            if decorators:
                # copy errors before we clear them in _overlay
                errorsSoFar = ExceptionCollector.exceptions[:]
                self._overlay(decorators)
                if ExceptionCollector.exceptionsCaught():
                    # abort if overlay caused errors
                    # report previously collected errors too
                    ExceptionCollector.exceptions[:0] = errorsSoFar
                    message = "\n".join(
                        ExceptionCollector.getExceptionsReport(
                            getLogLevel() < logging.INFO
                        )
                    )
                    raise UnfurlValidationError(
                        "TOSCA validation failed for %s: \n%s" % (path, message),
                        ExceptionCollector.getExceptions(),
                    )
                # overlay modifies tosaDef in-place, try reparsing it
                self._parseTemplate(path, inputs, toscaDef, resolver)

            if ExceptionCollector.exceptionsCaught():
                message = "\n".join(
                    ExceptionCollector.getExceptionsReport(getLogLevel() < logging.INFO)
                )
                raise UnfurlValidationError(
                    "TOSCA validation failed for %s: \n%s" % (path, message),
                    ExceptionCollector.getExceptions(),
                )

    @property
    def baseDir(self):
        if self.template.path is None:
            return None
        return getBaseDir(self.template.path)

    def _getProjectDir(self, home=False):
        # hacky
        if self.template.import_resolver:
            manifest = self.template.import_resolver.manifest
            if manifest.localEnv:
                if home:
                    if manifest.localEnv.homeProject:
                        return manifest.localEnv.homeProject.projectRoot
                elif manifest.localEnv.project:
                    return manifest.localEnv.project.projectRoot
        return None

    def addNodeTemplate(self, name, tpl):
        nodeTemplate = self.template.topology_template.add_template(name, tpl)
        nodeSpec = NodeSpec(nodeTemplate, self)
        self.nodeTemplates[name] = nodeSpec
        if self.discovered is None:
            self.discovered = CommentedMap()
        self.discovered[name] = tpl
        return nodeSpec

    def loadDecorators(self):
        decorators = {}
        for import_tpl in self.template.nested_tosca_tpls.values():
            decorators.update(import_tpl.get("decorators") or {})
        decorators.update(self.template.tpl.get("decorators") or {})
        return decorators

    def loadImportedDefaultTemplates(self):
        decorators = {}
        for topology in self.template.nested_topologies.values():
            for nodeTemplate in topology.nodetemplates:
                if (
                    "default" in nodeTemplate.directives
                    and nodeTemplate.name not in self.nodeTemplates
                ):
                    nodeSpec = NodeSpec(nodeTemplate, self)
                    self.nodeTemplates[nodeSpec.name] = nodeSpec
        return decorators

    def loadWorkflows(self):
        # we want to let different types defining standard workflows like deploy
        # so we need to support importing workflows
        workflows = {
            name: [Workflow(w)]
            for name, w in self.template.topology_template.workflows.items()
        }
        for topology in self.template.nested_topologies.values():
            for name, w in topology.workflows.items():
                workflows.setdefault(name, []).append(Workflow(w))
        self._workflows = workflows

    def getWorkflow(self, workflow):
        # XXX need api to get all the workflows with the same name
        wfs = self._workflows.get(workflow)
        if wfs:
            return wfs[0]
        else:
            return None

    def getRepositoryPath(self, repositoryName, file=""):
        baseArtifact = Artifact(dict(repository=repositoryName, file=file), spec=self)
        if baseArtifact.repository:
            # may resolve repository url to local path (e.g. checkout a remote git repo)
            return baseArtifact.getPath()
        else:
            return None

    def getTemplate(self, name):
        if name == "~topology":
            return self.topology
        elif "~c~" in name:
            nodeName, capability = name.split("~c~")
            nodeTemplate = self.nodeTemplates.get(nodeName)
            if not nodeTemplate:
                return None
            return nodeTemplate.getCapability(capability)
        elif "~r~" in name:
            nodeName, requirement = name.split("~r~")
            if nodeName:
                nodeTemplate = self.nodeTemplates.get(nodeName)
                if not nodeTemplate:
                    return None
                return nodeTemplate.getRelationship(requirement)
            else:
                return self.relationshipTemplates.get(name)
        elif "~q~" in name:
            nodeName, requirement = name.split("~q~")
            nodeTemplate = self.nodeTemplates.get(nodeName)
            if not nodeTemplate:
                return None
            return nodeTemplate.getRequirement(requirement)
        else:
            return self.nodeTemplates.get(name)

    def isTypeName(self, typeName):
        return (
            typeName in self.template.topology_template.custom_defs
            or typeName in EntityType.TOSCA_DEF
        )

    def findMatchingTemplates(self, typeName):
        for template in self.nodeTemplates:
            if template.isCompatibleType(typeName):
                yield template

    def loadInstances(self, toscaDef, tpl):
        """
        Creates node templates for any instances defined in the spec

        .. code-block:: YAML

          spec:
                instances:
                  test:
                    installer: test
                installers:
                  test:
                    operations:
                      default:
                        implementation: TestConfigurator
                        inputs:"""
        node_templates = toscaDef["topology_template"]["node_templates"]
        for name, impl in tpl.get("installers", {}).items():
            if name not in node_templates:
                node_templates[name] = dict(type=self.InstallerType, properties=impl)
            else:
                raise UnfurlValidationError(
                    'can not add installer "%s", there is already a node template with that name'
                    % name
                )

        for name, impl in tpl.get("instances", {}).items():
            if name not in node_templates and impl is not None:
                node_templates[name] = self.loadInstance(impl.copy())

        if "discovered" in tpl:
            # node templates added dynamically by configurators
            self.discovered = tpl["discovered"]
            for name, impl in tpl["discovered"].items():
                if name not in node_templates:
                    node_templates[name] = impl

    def loadInstance(self, impl):
        if "type" not in impl:
            impl["type"] = "unfurl.nodes.Default"
        installer = impl.pop("install", None)
        if installer:
            impl["requirements"] = [{"install": installer}]
        return impl

    def importConnections(self, importedSpec):
        # user-declared telationship templates, source and target will be None
        for template in importedSpec.template.relationship_templates:
            assert template.default_for  # it's a default relationship template
            relTemplate = RelationshipSpec(template, self)
            if template.name not in self.relationshipTemplates:  # not defined yet
                self.relationshipTemplates[template.name] = relTemplate


_defaultTopology = createDefaultTopology()


def findProps(attributes, attributeDefs, matchfn):
    if not attributes:
        return
    for propdef in attributeDefs.values():
        if propdef.name not in attributes:
            continue
        match = matchfn(propdef.entry_schema_entity or propdef.entity)
        if not propdef.entry_schema and not propdef.entity.properties:
            # it's a simple value type
            if match:
                yield propdef.name, attributes[propdef.name]
            continue

        if not propdef.entry_schema:
            # it's complex datatype
            value = attributes[propdef.name]
            if match:
                yield propdef.name, value
            elif value:
                # descend into its properties
                for name, v in findProps(value, propdef.entity.properties, matchfn):
                    yield name, v
            continue

        properties = propdef.entry_schema_entity.properties
        if not match and not properties:
            # entries are simple value types and didn't match
            continue

        value = attributes[propdef.name]
        if not value:
            continue
        if propdef.type == "map":
            for key, val in value.items():
                if match:
                    yield key, val
                elif properties:
                    for name, v in findProps(val, properties, matchfn):
                        yield name, v
        elif propdef.type == "list":
            for val in value:
                if match:
                    yield None, val
                elif properties:
                    for name, v in findProps(val, properties, matchfn):
                        yield name, v


# represents a node, capability or relationship
class EntitySpec(ResourceRef):
    # XXX need to define __eq__ for spec changes
    def __init__(self, toscaNodeTemplate, spec=None):
        self.toscaEntityTemplate = toscaNodeTemplate
        self.spec = spec
        self.name = toscaNodeTemplate.name
        self.type = toscaNodeTemplate.type
        # nodes have both properties and attributes
        # as do capability properties and relationships
        # but only property values are declared
        self.attributeDefs = toscaNodeTemplate.get_properties()
        self.properties = {
            prop.name: prop.value for prop in self.attributeDefs.values()
        }
        if toscaNodeTemplate.type_definition:
            # add attributes definitions
            attrDefs = toscaNodeTemplate.type_definition.get_attributes_def()
            self.defaultAttributes = {
                prop.name: prop.default
                for prop in attrDefs.values()
                if prop.default is not None
            }
            for name, aDef in attrDefs.items():
                self.attributeDefs[name] = Property(
                    name, aDef.default, aDef.schema, toscaNodeTemplate.custom_def
                )
            # now add any property definitions that haven't been defined yet
            # i.e. missing properties without a default and not required
            props_def = toscaNodeTemplate.type_definition.get_properties_def()
            for pDef in props_def.values():
                if pDef.name not in self.attributeDefs:
                    self.attributeDefs[pDef.name] = Property(
                        pDef.name,
                        pDef.default,
                        pDef.schema,
                        toscaNodeTemplate.custom_def,
                    )
        else:
            self.defaultAttributes = {}

    parent = None

    def __reflookup__(self, key):
        """Make attributes available to expressions"""
        if key[0] == ".":
            return self._getProp(key)
        if key in ["name", "type", "uri", "groups", "policies"]:
            return getattr(self, key)
        raise KeyError(key)

    def getInterfaces(self):
        return self.toscaEntityTemplate.interfaces

    @property
    def groups(self):
        if not self.spec:
            return
        for g in self.spec.groups.values():
            if self.name in g.members:
                yield g

    @property
    def policies(self):
        return []

    def isCompatibleTarget(self, targetStr):
        if self.name == targetStr:
            return True
        return self.toscaEntityTemplate.is_derived_from(targetStr)

    def isCompatibleType(self, typeStr):
        return self.toscaEntityTemplate.is_derived_from(typeStr)

    @property
    def uri(self):
        return self.getUri()

    def getUri(self):
        return self.name  # XXX

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.name)

    @property
    def artifacts(self):
        return {}

    def findOrCreateArtifact(self, nameOrTpl, path=None):
        if isinstance(nameOrTpl, six.string_types):
            artifact = self.artifacts.get(nameOrTpl)
            if artifact:
                return artifact
            # name not found, assume its a file path or URL
            tpl = dict(file=nameOrTpl)
        else:
            tpl = nameOrTpl
        # create an anonymous, inline artifact
        return Artifact(tpl, self, path=path)

    @property
    def abstract(self):
        return None

    @property
    def directives(self):
        return []

    def findProps(self, attributes, matchfn):
        for name, val in findProps(attributes, self.attributeDefs, matchfn):
            yield name, val

    @property
    def baseDir(self):
        if self.toscaEntityTemplate._source:
            return self.toscaEntityTemplate._source
        elif self.spec:
            return self.spec.baseDir
        else:
            return None


class NodeSpec(EntitySpec):
    # has attributes: tosca_id, tosca_name, state, (3.4.1 Node States p.61)
    def __init__(self, template=None, spec=None):
        if not template:
            template = next(iter(_defaultTopology.topology_template.nodetemplates))
            spec = ToscaSpec(_defaultTopology)
        else:
            assert spec
        EntitySpec.__init__(self, template, spec)
        self._capabilities = None
        self._requirements = None
        self._relationships = []
        self._artifacts = None

    def __reflookup__(self, key):
        try:
            return super(NodeSpec, self).__reflookup__(key)
        except KeyError:
            relationship = self.getRelationship(key)
            if not relationship:
                raise KeyError(key)
            return relationship

    @property
    def artifacts(self):
        if self._artifacts is None:
            self._artifacts = {
                name: Artifact(artifact, self)
                for name, artifact in self.toscaEntityTemplate.artifacts.items()
            }
        return self._artifacts

    @property
    def policies(self):
        if not self.spec:
            return
        for p in self.spec.policies.values():
            if p.toscaEntityTemplate.targets_type == "groups":
                # the policy has groups as members, see if this node's groups is one of them
                if p.members & set(g.name for g in self.groups):
                    yield p
            elif p.toscaEntityTemplate.targets_type == "node_templates":
                if self.name in p.members:
                    yield p

    @property
    def requirements(self):
        if self._requirements is None:
            self._requirements = {}
            nodeTemplate = self.toscaEntityTemplate
            for (relTpl, req, reqDef) in nodeTemplate.relationships:
                name, values = next(iter(req.items()))
                reqSpec = RequirementSpec(name, reqDef, self)
                if relTpl.target:
                    nodeSpec = self.spec.getTemplate(relTpl.target.name)
                    assert nodeSpec
                    nodeSpec.addRelationship(reqSpec)
                self._requirements[name] = reqSpec
        return self._requirements

    def getRequirement(self, name):
        return self.requirements.get(name)

    def getRelationship(self, name):
        req = self.requirements.get(name)
        if not req:
            return None
        return req.relationship

    @property
    def relationships(self):
        """
        returns a list of RelationshipSpecs that are targeting this node template.
        """
        for r in self.toscaEntityTemplate.relationship_tpl:
            assert r.source
            # calling requirement property will ensure the RelationshipSpec is properly linked
            self.spec.getTemplate(r.source.name).requirements
        return self._getRelationshipSpecs()

    def _getRelationshipSpecs(self):
        if len(self._relationships) != len(self.toscaEntityTemplate.relationship_tpl):
            # relationship_tpl is a list of RelationshipTemplates that target the node
            rIds = set(id(r.toscaEntityTemplate) for r in self._relationships)
            for r in self.toscaEntityTemplate.relationship_tpl:
                if id(r) not in rIds:
                    self._relationships.append(RelationshipSpec(r, self.spec, self))
        return self._relationships

    def getCapabilityInterfaces(self):
        idefs = [r.getInterfaces() for r in self._getRelationshipSpecs()]
        return [i for elem in idefs for i in elem if i.name != "default"]

    def getRequirementInterfaces(self):
        idefs = [r.getInterfaces() for r in self.requirements.values()]
        return [i for elem in idefs for i in elem if i.name != "default"]

    @property
    def capabilities(self):
        if self._capabilities is None:
            self._capabilities = {
                c.name: CapabilitySpec(self, c)
                for c in self.toscaEntityTemplate.get_capabilities_objects()
            }
        return self._capabilities

    def getCapability(self, name):
        return self.capabilities.get(name)

    def addRelationship(self, reqSpec):
        # find the relationship for this requirement:
        for relSpec in self._getRelationshipSpecs():
            # the RelationshipTemplate should have had the source node assigned by the tosca parser
            # XXX this won't distinguish between more than one relationship between the same two nodes
            # to fix this have the RelationshipTemplate remember the name of the requirement
            if (
                relSpec.toscaEntityTemplate.source
                is reqSpec.parentNode.toscaEntityTemplate
            ):
                assert not reqSpec.relationship or reqSpec.relationship is relSpec
                reqSpec.relationship = relSpec
                assert not relSpec.requirement or relSpec.requirement is reqSpec
                relSpec.requirement = reqSpec
                break
        else:
            msg = (
                'relationship not found for requirement "%s" on "%s" targeting "%s"'
                % (reqSpec.name, reqSpec.parentNode, self.name)
            )
            raise UnfurlValidationError(msg)

    @property
    def abstract(self):
        for name in ("select", "substitute"):
            if name in self.toscaEntityTemplate.directives:
                return name
        return None

    @property
    def directives(self):
        return self.toscaEntityTemplate.directives


class RelationshipSpec(EntitySpec):
    """
    Links a RequirementSpec to a CapabilitySpec.
    """

    def __init__(self, template=None, spec=None, targetNode=None):
        # template is a RelationshipTemplate
        # It is a full-fledged entity with a name, type, properties, attributes, interfaces, and metadata.
        # its connected through target, source, capability
        # its RelationshipType has valid_target_types
        if not template:
            template = _defaultTopology.topology_template.relationship_templates[0]
            spec = ToscaSpec(_defaultTopology)
        else:
            assert spec
        EntitySpec.__init__(self, template, spec)
        self.requirement = None
        self.capability = None
        if targetNode:
            assert targetNode.toscaEntityTemplate is template.target
            for c in targetNode.capabilities.values():
                if c.toscaEntityTemplate is template.capability:
                    self.capability = c
                    break
            else:
                raise UnfurlError(
                    "capability %s not found in %s for %s"
                    % (
                        template.capability.name,
                        [c.name for c in targetNode.capabilities.values()],
                        targetNode.name,
                    )
                )

    @property
    def source(self):
        return self.requirement.parentNode if self.requirement else None

    @property
    def target(self):
        return self.capability.parentNode if self.capability else None

    def __reflookup__(self, key):
        try:
            return super(RelationshipSpec, self).__reflookup__(key)
        except KeyError:
            if self.capability:
                if self.capability.parentNode.isCompatibleTarget(key):
                    return self.capability.parentNode
                if self.capability.isCompatibleTarget(key):
                    return self.capability
            raise KeyError(key)

    def getUri(self):
        suffix = "~r~" + self.name
        return self.source.name + suffix if self.source else suffix

    def matches_target(self, capability):
        defaultFor = self.toscaEntityTemplate.default_for
        if not defaultFor:
            return False
        nodeTemplate = capability.parentNode.toscaEntityTemplate

        if (
            defaultFor == self.toscaEntityTemplate.ANY
            or defaultFor == nodeTemplate.name
            or nodeTemplate.is_derived_from(defaultFor)
            or defaultFor == capability.name
            or capability.is_derived_from(defaultFor)
        ):
            return self.toscaEntityTemplate.get_matching_capabilities(
                nodeTemplate, capability.name
            )

        return False


class RequirementSpec(object):
    """
    A Requirement shares a Relationship with a Capability.
    """

    # XXX need __eq__ since this doesn't derive from EntitySpec
    def __init__(self, name, req, parent):
        self.source = self.parentNode = parent  # NodeSpec
        self.spec = parent.spec
        self.name = name
        self.requirements_tpl = req
        self.relationship = None
        # requirements_tpl may specify:
        # capability (definition name or type name), node (template name or type name), and node_filter,
        # relationship (template name or type name or inline relationship template)
        # occurrences

    @property
    def artifacts(self):
        return self.parentNode.artifacts

    def getUri(self):
        return self.parentNode.name + "~q~" + self.name

    def getInterfaces(self):
        return self.relationship.getInterfaces() if self.relationship else []


class CapabilitySpec(EntitySpec):
    def __init__(self, parent=None, capability=None):
        if not parent:
            parent = NodeSpec()
            capability = parent.toscaEntityTemplate.get_capabilities_objects()[0]
        self.parentNode = parent
        assert capability
        # capabilities.Capability isn't an EntityTemplate but duck types with it
        EntitySpec.__init__(self, capability, parent.spec)
        self._relationships = None
        self._defaultRelationships = None

    @property
    def parent(self):
        return self.parentNode

    @property
    def artifacts(self):
        return self.parentNode.artifacts

    def getInterfaces(self):
        # capabilities don't have their own interfaces
        return self.parentNode.getInterfaces()

    def getUri(self):
        # capabilities aren't standalone templates
        # this is demanagled by getTemplate()
        return self.parentNode.name + "~c~" + self.name

    @property
    def relationships(self):
        return [r for r in self.parentNode.relationships if r.capability is self]

    @property
    def defaultRelationships(self):
        if self._defaultRelationships is None:
            self._defaultRelationships = [
                relSpec
                for relSpec in self.spec.relationshipTemplates.values()
                if relSpec.matches_target(self)
            ]
        return self._defaultRelationships

    def getDefaultRelationships(self, relation=None):
        if not relation:
            return self.defaultRelationships
        return [
            relSpec
            for relSpec in self.defaultRelationships
            if relSpec.isCompatibleType(relation)
        ]


class TopologySpec(EntitySpec):
    # has attributes: tosca_id, tosca_name, state, (3.4.1 Node States p.61)
    def __init__(self, spec=None, inputs=None):
        if spec:
            self.spec = spec
            template = spec.template.topology_template
        else:
            template = _defaultTopology.topology_template
            self.spec = ToscaSpec(_defaultTopology)
            self.spec.topology = self

        inputs = inputs or {}
        self.toscaEntityTemplate = template
        self.name = "~topology"
        self.type = "~topology"
        self.inputs = {
            input.name: inputs.get(input.name, input.default)
            for input in template.inputs
        }
        self.outputs = {output.name: output.value for output in template.outputs}
        self.properties = {}
        self.defaultAttributes = {}
        self.attributeDefs = {}
        self.capabilities = []

    def getInterfaces(self):
        # doesn't have any interfaces
        return []

    def isCompatibleTarget(self, targetStr):
        if self.name == targetStr:
            return True
        return False

    def isCompatibleType(self, typeStr):
        return False

    @property
    def baseDir(self):
        return self.spec.baseDir

    def __reflookup__(self, key):
        """Make attributes available to expressions"""
        try:
            return super(TopologySpec, self).__reflookup__(key)
        except KeyError:
            nodeTemplates = self.spec.nodeTemplates
            nodeSpec = nodeTemplates.get(key)
            if nodeSpec:
                return nodeSpec
            matches = [n for n in nodeTemplates.values() if n.isCompatibleType(key)]
            if not matches:
                raise KeyError(key)
            return matches


class Workflow(object):
    def __init__(self, workflow):
        self.workflow = workflow

    def initialSteps(self):
        preceeding = set()
        for step in self.workflow.steps.values():
            preceeding.update(step.on_success + step.on_failure)
        return [
            step for step in self.workflow.steps.values() if step.name not in preceeding
        ]

    def getStep(self, stepName):
        return self.workflow.steps.get(stepName)

    def matchStepFilter(self, stepName, resource):
        step = self.getStep(stepName)
        if step:
            return all(filter.evaluate(resource.attributes) for filter in step.filter)
        return None

    def matchPreconditions(self, resource):
        for precondition in self.workflow.preconditions:
            target = resource.root.findResource(precondition.target)
            # XXX if precondition.target_relationship
            if not target:
                # XXX target can be a group
                return False
            if not all(
                filter.evaluate(target.attributes) for filter in precondition.condition
            ):
                return False
        return True


class Artifact(EntitySpec):
    def __init__(self, artifact_tpl, template=None, spec=None, path=None):
        # 3.6.7 Artifact definition p. 84
        self.parentNode = template
        spec = template.spec if template else spec
        if isinstance(artifact_tpl, toscaparser.artifacts.Artifact):
            artifact = artifact_tpl
        else:
            # inline artifact
            custom_defs = spec and spec.template.topology_template.custom_defs or {}
            artifact = toscaparser.artifacts.Artifact(
                artifact_tpl.get("file", ""), artifact_tpl, custom_defs, path
            )
        EntitySpec.__init__(self, artifact, spec)
        self.repository = (
            spec
            and artifact.repository
            and spec.template.repositories.get(artifact.repository)
            or None
        )

    @property
    def file(self):
        return self.toscaEntityTemplate.file

    @property
    def baseDir(self):
        if self.toscaEntityTemplate._source:
            return getBaseDir(self.toscaEntityTemplate._source)
        else:
            return super(Artifact, self).baseDir

    def getPath(self, resolver=None):
        return self.getPathAndFragment(resolver)[0]

    def getPathAndFragment(self, resolver=None, tpl=None):
        """
        returns path, fragment
        """
        tpl = self.spec and self.spec.template.tpl or tpl
        if not resolver and self.spec:
            resolver = self.spec.template.import_resolver

        loader = toscaparser.imports.ImportsLoader(
            None, self.baseDir, tpl=tpl, resolver=resolver
        )
        path, isFile, fragment = loader._resolve_import_template(
            None, self.asImportSpec()
        )
        return path, fragment

    def asImportSpec(self):
        return dict(file=self.file, repository=self.toscaEntityTemplate.repository)


class GroupSpec(EntitySpec):
    def __init__(self, template, spec):
        EntitySpec.__init__(self, template, spec)
        self.members = template.members

    # XXX getNodeTemplates() getInstances(), getChildren()

    @property
    def memberGroups(self):
        return [self.spec.groups[m] for m in self.members if m in self.spec.groups]

    @property
    def policies(self):
        if not self.spec:
            return
        for p in self.spec.policies.values():
            if p.toscaEntityTemplate.targets_type == "groups":
                if self.name in p.members:
                    yield p


class PolicySpec(EntitySpec):
    def __init__(self, template, spec):
        EntitySpec.__init__(self, template, spec)
        self.members = set(template.targets_list)
