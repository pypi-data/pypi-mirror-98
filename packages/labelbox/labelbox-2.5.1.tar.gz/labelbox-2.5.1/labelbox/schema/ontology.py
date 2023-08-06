import abc
from dataclasses import dataclass, field
from enum import Enum, auto
import colorsys

from typing import Any, Callable, Dict, List, Optional, Union

from labelbox.schema.project import Project
from labelbox.orm import query
from labelbox.orm.db_object import DbObject, Updateable, BulkDeletable
from labelbox.orm.model import Entity, Field, Relationship
from labelbox.utils import snake_case, camel_case
from labelbox.exceptions import InconsistentOntologyException


@dataclass
class Option:
    """
    An option is a possible answer within a Classification object in
    a Project's ontology. 

    To instantiate, only the "value" parameter needs to be passed in.

    Example(s):
        option = Option(value = "Option Example")

    Attributes:
        value: (str)
        schema_id: (str)
        feature_schema_id: (str)
        options: (list)
    """
    value: Union[str, int]
    schema_id: Optional[str] = None
    feature_schema_id: Optional[str] = None
    options: List["Classification"] = field(default_factory=list)

    @property
    def label(self):
        return self.value

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]):
        return Option(value=dictionary["value"],
                      schema_id=dictionary.get("schemaNodeId", []),
                      feature_schema_id=dictionary.get("featureSchemaId", []),
                      options=[
                          Classification.from_dict(o)
                          for o in dictionary.get("options", [])
                      ])

    def asdict(self) -> Dict[str, Any]:
        return {
            "schemaNodeId": self.schema_id,
            "featureSchemaId": self.feature_schema_id,
            "label": self.label,
            "value": self.value,
            "options": [o.asdict() for o in self.options]
        }

    def add_option(self, option: 'Classification'):
        if option.instructions in (o.instructions for o in self.options):
            raise InconsistentOntologyException(
                f"Duplicate nested classification '{option.instructions}' "
                f"for option '{self.label}'")
        self.options.append(option)


@dataclass
class Classification:
    """
    A classfication to be added to a Project's ontology. The  
    classification is dependent on the Classification Type.

    To instantiate, the "class_type" and "instructions" parameters must
    be passed in.

    The "options" parameter holds a list of Option objects. This is not 
    necessary for some Classification types, such as TEXT. To see which
    types require options, look at the "_REQUIRES_OPTIONS" class variable.

    Example(s):
        classification = Classification(
            class_type = Classification.Type.TEXT,
            instructions = "Classification Example")

        classification_two = Classification(
            class_type = Classification.Type.RADIO,
            instructions = "Second Example")
        classification_two.add_option(Option(
            value = "Option Example"))

    Attributes:
        class_type: (Classification.Type)
        instructions: (str)
        required: (bool)
        options: (list)
        schema_id: (str)
        feature_schema_id: (str)
    """

    class Type(Enum):
        TEXT = "text"
        CHECKLIST = "checklist"
        RADIO = "radio"
        DROPDOWN = "dropdown"

    _REQUIRES_OPTIONS = {Type.CHECKLIST, Type.RADIO, Type.DROPDOWN}

    class_type: Type
    instructions: str
    required: bool = False
    options: List[Option] = field(default_factory=list)
    schema_id: Optional[str] = None
    feature_schema_id: Optional[str] = None

    @property
    def name(self):
        return self.instructions

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]):
        return Classification(
            class_type=Classification.Type(dictionary["type"]),
            instructions=dictionary["instructions"],
            required=dictionary["required"],
            options=[Option.from_dict(o) for o in dictionary["options"]],
            schema_id=dictionary.get("schemaNodeId", []),
            feature_schema_id=dictionary.get("featureSchemaId", []))

    def asdict(self) -> Dict[str, Any]:
        if self.class_type in Classification._REQUIRES_OPTIONS \
                and len(self.options) < 1:
            raise InconsistentOntologyException(
                f"Classification '{self.instructions}' requires options.")
        return {
            "type": self.class_type.value,
            "instructions": self.instructions,
            "name": self.name,
            "required": self.required,
            "options": [o.asdict() for o in self.options],
            "schemaNodeId": self.schema_id,
            "featureSchemaId": self.feature_schema_id
        }

    def add_option(self, option: Option):
        if option.value in (o.value for o in self.options):
            raise InconsistentOntologyException(
                f"Duplicate option '{option.value}' "
                f"for classification '{self.name}'.")
        self.options.append(option)


@dataclass
class Tool:
    """
    A tool to be added to a Project's ontology. The tool is
    dependent on the Tool Type.

    To instantiate, the "tool" and "name" parameters must
    be passed in.

    The "classifications" parameter holds a list of Classification objects. 
    This can be used to add nested classifications to a tool.

    Example(s):
        tool = Tool(
            tool = Tool.Type.LINE,
            name = "Tool example")    
        classification = Classification(
            class_type = Classification.Type.TEXT,
            instructions = "Classification Example")
        tool.add_classification(classification)

    Attributes:
        tool: (Tool.Type)
        name: (str)
        required: (bool)
        color: (str)
        classifications: (list)
        schema_id: (str)
        feature_schema_id: (str)
    """

    class Type(Enum):
        POLYGON = "polygon"
        SEGMENTATION = "superpixel"
        POINT = "point"
        BBOX = "rectangle"
        LINE = "line"
        NER = "named-entity"

    tool: Type
    name: str
    required: bool = False
    color: Optional[str] = None
    classifications: List[Classification] = field(default_factory=list)
    schema_id: Optional[str] = None
    feature_schema_id: Optional[str] = None

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]):
        return Tool(name=dictionary['name'],
                    schema_id=dictionary.get("schemaNodeId", []),
                    feature_schema_id=dictionary.get("featureSchemaId", []),
                    required=dictionary["required"],
                    tool=Tool.Type(dictionary["tool"]),
                    classifications=[
                        Classification.from_dict(c)
                        for c in dictionary["classifications"]
                    ],
                    color=dictionary["color"])

    def asdict(self) -> Dict[str, Any]:
        return {
            "tool": self.tool.value,
            "name": self.name,
            "required": self.required,
            "color": self.color,
            "classifications": [c.asdict() for c in self.classifications],
            "schemaNodeId": self.schema_id,
            "featureSchemaId": self.feature_schema_id
        }

    def add_classification(self, classification: Classification):
        if classification.instructions in (
                c.instructions for c in self.classifications):
            raise InconsistentOntologyException(
                f"Duplicate nested classification '{classification.instructions}' "
                f"for tool '{self.name}'")
        self.classifications.append(classification)


class Ontology(DbObject):
    """An ontology specifies which tools and classifications are available
    to a project. This is read only for now.
    Attributes:
        name (str)
        description (str)
        updated_at (datetime)
        created_at (datetime)
        normalized (json)
        object_schema_count (int)
        classification_schema_count (int)
        projects (Relationship): `ToMany` relationship to Project
        created_by (Relationship): `ToOne` relationship to User
    """

    name = Field.String("name")
    description = Field.String("description")
    updated_at = Field.DateTime("updated_at")
    created_at = Field.DateTime("created_at")
    normalized = Field.Json("normalized")
    object_schema_count = Field.Int("object_schema_count")
    classification_schema_count = Field.Int("classification_schema_count")

    projects = Relationship.ToMany("Project", True)
    created_by = Relationship.ToOne("User", False, "created_by")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tools: Optional[List[Tool]] = None
        self._classifications: Optional[List[Classification]] = None

    def tools(self) -> List[Tool]:
        """Get list of tools (AKA objects) in an Ontology."""
        if self._tools is None:
            self._tools = [
                Tool.from_dict(tool) for tool in self.normalized['tools']
            ]
        return self._tools

    def classifications(self) -> List[Classification]:
        """Get list of classifications in an Ontology."""
        if self._classifications is None:
            self._classifications = [
                Classification.from_dict(classification)
                for classification in self.normalized['classifications']
            ]
        return self._classifications


@dataclass
class OntologyBuilder:
    """
    A class to help create an ontology for a Project. This should be used
    for making Project ontologies from scratch. OntologyBuilder can also
    pull from an already existing Project's ontology.

    There are no required instantiation arguments. 

    To create an ontology, use the asdict() method after fully building your 
    ontology within this class, and inserting it into project.setup() as the
    "labeling_frontend_options" parameter.

    Example:
        builder = OntologyBuilder()
        ...
        frontend = list(client.get_labeling_frontends())[0]
        project.setup(frontend, builder.asdict())

    attributes:
        tools: (list)
        classifications: (list)

    
    """
    tools: List[Tool] = field(default_factory=list)
    classifications: List[Classification] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]):
        return OntologyBuilder(
            tools=[Tool.from_dict(t) for t in dictionary["tools"]],
            classifications=[
                Classification.from_dict(c)
                for c in dictionary["classifications"]
            ])

    def asdict(self):
        self._update_colors()
        return {
            "tools": [t.asdict() for t in self.tools],
            "classifications": [c.asdict() for c in self.classifications]
        }

    def _update_colors(self):
        num_tools = len(self.tools)

        for index in range(num_tools):
            hsv_color = (index * 1 / num_tools, 1, 1)
            rgb_color = tuple(
                int(255 * x) for x in colorsys.hsv_to_rgb(*hsv_color))
            if self.tools[index].color is None:
                self.tools[index].color = '#%02x%02x%02x' % rgb_color

    @classmethod
    def from_project(cls, project: Project):
        ontology = project.ontology().normalized
        return OntologyBuilder.from_dict(ontology)

    def add_tool(self, tool: Tool):
        if tool.name in (t.name for t in self.tools):
            raise InconsistentOntologyException(
                f"Duplicate tool name '{tool.name}'. ")
        self.tools.append(tool)

    def add_classification(self, classification: Classification):
        if classification.instructions in (
                c.instructions for c in self.classifications):
            raise InconsistentOntologyException(
                f"Duplicate classification instructions '{classification.instructions}'. "
            )
        self.classifications.append(classification)
