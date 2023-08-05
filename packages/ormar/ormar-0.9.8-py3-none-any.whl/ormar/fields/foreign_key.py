import string
import sys
import uuid
from dataclasses import dataclass
from random import choices
from typing import Any, List, Optional, TYPE_CHECKING, Tuple, Type, Union

import sqlalchemy
from pydantic import BaseModel, create_model
from pydantic.typing import ForwardRef, evaluate_forwardref
from sqlalchemy import UniqueConstraint

import ormar  # noqa I101
from ormar.exceptions import ModelDefinitionError, RelationshipInstanceError
from ormar.fields.base import BaseField

if TYPE_CHECKING:  # pragma no cover
    from ormar.models import Model, NewBaseModel
    from ormar.fields import ManyToManyField

    if sys.version_info < (3, 7):
        ToType = Type["Model"]
    else:
        ToType = Union[Type["Model"], "ForwardRef"]


def create_dummy_instance(fk: Type["Model"], pk: Any = None) -> "Model":
    """
    Ormar never returns you a raw data.
    So if you have a related field that has a value populated
    it will construct you a Model instance out of it.

    Creates a "fake" instance of passed Model from pk value.
    The instantiated Model has only pk value filled.
    To achieve this __pk_only__ flag has to be passed as it skips the validation.

    If the nested related Models are required they are set with -1 as pk value.

    :param fk: class of the related Model to which instance should be constructed
    :type fk: Model class
    :param pk: value of the primary_key column
    :type pk: Any
    :return: Model instance populated with only pk
    :rtype: Model
    """
    init_dict = {
        **{fk.Meta.pkname: pk or -1, "__pk_only__": True},
        **{
            k: create_dummy_instance(v.to)
            for k, v in fk.Meta.model_fields.items()
            if v.is_relation and not v.nullable and not v.virtual
        },
    }
    return fk(**init_dict)


def create_dummy_model(
    base_model: Type["Model"],
    pk_field: Type[Union[BaseField, "ForeignKeyField", "ManyToManyField"]],
) -> Type["BaseModel"]:
    """
    Used to construct a dummy pydantic model for type hints and pydantic validation.
    Populates only pk field and set it to desired type.

    :param base_model: class of target dummy model
    :type base_model: Model class
    :param pk_field: ormar Field to be set on pydantic Model
    :type pk_field: Type[Union[BaseField, "ForeignKeyField", "ManyToManyField"]]
    :return: constructed dummy model
    :rtype: pydantic.BaseModel
    """
    alias = (
        "".join(choices(string.ascii_uppercase, k=2)) + uuid.uuid4().hex[:4]
    ).lower()
    fields = {f"{pk_field.name}": (pk_field.__type__, None)}

    dummy_model = create_model(  # type: ignore
        f"PkOnly{base_model.get_name(lower=False)}{alias}",
        __module__=base_model.__module__,
        **fields,  # type: ignore
    )
    return dummy_model


def populate_fk_params_based_on_to_model(
    to: Type["Model"], nullable: bool, onupdate: str = None, ondelete: str = None,
) -> Tuple[Any, List, Any]:
    """
    Based on target to model to which relation leads to populates the type of the
    pydantic field to use, ForeignKey constraint and type of the target column field.

    :param to: target related ormar Model
    :type to: Model class
    :param nullable: marks field as optional/ required
    :type nullable: bool
    :param onupdate: parameter passed to sqlalchemy.ForeignKey.
    How to treat child rows on update of parent (the one where FK is defined) model.
    :type onupdate: str
    :param ondelete: parameter passed to sqlalchemy.ForeignKey.
    How to treat child rows on delete of parent (the one where FK is defined) model.
    :type ondelete: str
    :return: tuple with target pydantic type, list of fk constraints and target col type
    :rtype: Tuple[Any, List, Any]
    """
    fk_string = to.Meta.tablename + "." + to.get_column_alias(to.Meta.pkname)
    to_field = to.Meta.model_fields[to.Meta.pkname]
    pk_only_model = create_dummy_model(to, to_field)
    __type__ = (
        Union[to_field.__type__, to, pk_only_model]
        if not nullable
        else Optional[Union[to_field.__type__, to, pk_only_model]]
    )
    constraints = [
        ForeignKeyConstraint(
            reference=fk_string, ondelete=ondelete, onupdate=onupdate, name=None
        )
    ]
    column_type = to_field.column_type
    return __type__, constraints, column_type


class UniqueColumns(UniqueConstraint):
    """
    Subclass of sqlalchemy.UniqueConstraint.
    Used to avoid importing anything from sqlalchemy by user.
    """


@dataclass
class ForeignKeyConstraint:
    """
    Internal container to store ForeignKey definitions used later
    to produce sqlalchemy.ForeignKeys
    """

    reference: Union[str, sqlalchemy.Column]
    name: Optional[str]
    ondelete: Optional[str]
    onupdate: Optional[str]


def ForeignKey(  # noqa CFQ002
    to: "ToType",
    *,
    name: str = None,
    unique: bool = False,
    nullable: bool = True,
    related_name: str = None,
    virtual: bool = False,
    onupdate: str = None,
    ondelete: str = None,
    **kwargs: Any,
) -> Any:
    """
    Despite a name it's a function that returns constructed ForeignKeyField.
    This function is actually used in model declaration (as ormar.ForeignKey(ToModel)).

    Accepts number of relation setting parameters as well as all BaseField ones.

    :param to: target related ormar Model
    :type to: Model class
    :param name: name of the database field - later called alias
    :type name: str
    :param unique: parameter passed to sqlalchemy.ForeignKey, unique flag
    :type unique: bool
    :param nullable: marks field as optional/ required
    :type nullable: bool
    :param related_name: name of reversed FK relation populated for you on to model
    :type related_name: str
    :param virtual: marks if relation is virtual.
    It is for reversed FK and auto generated FK on through model in Many2Many relations.
    :type virtual: bool
    :param onupdate: parameter passed to sqlalchemy.ForeignKey.
    How to treat child rows on update of parent (the one where FK is defined) model.
    :type onupdate: str
    :param ondelete: parameter passed to sqlalchemy.ForeignKey.
    How to treat child rows on delete of parent (the one where FK is defined) model.
    :type ondelete: str
    :param kwargs: all other args to be populated by BaseField
    :type kwargs: Any
    :return: ormar ForeignKeyField with relation to selected model
    :rtype: ForeignKeyField
    """

    owner = kwargs.pop("owner", None)
    self_reference = kwargs.pop("self_reference", False)

    default = kwargs.pop("default", None)
    encrypt_secret = kwargs.pop("encrypt_secret", None)
    encrypt_backend = kwargs.pop("encrypt_backend", None)
    encrypt_custom_backend = kwargs.pop("encrypt_custom_backend", None)

    not_supported = [
        default,
        encrypt_secret,
        encrypt_backend,
        encrypt_custom_backend,
    ]
    if any(x is not None for x in not_supported):
        raise ModelDefinitionError(
            f"Argument {next((x for x in not_supported if x is not None))} "
            f"is not supported "
            "on relation fields!"
        )

    if to.__class__ == ForwardRef:
        __type__ = to if not nullable else Optional[to]
        constraints: List = []
        column_type = None
    else:
        __type__, constraints, column_type = populate_fk_params_based_on_to_model(
            to=to,  # type: ignore
            nullable=nullable,
            ondelete=ondelete,
            onupdate=onupdate,
        )

    namespace = dict(
        __type__=__type__,
        to=to,
        through=None,
        alias=name,
        name=kwargs.pop("real_name", None),
        nullable=nullable,
        constraints=constraints,
        unique=unique,
        column_type=column_type,
        related_name=related_name,
        virtual=virtual,
        primary_key=False,
        index=False,
        pydantic_only=False,
        default=None,
        server_default=None,
        onupdate=onupdate,
        ondelete=ondelete,
        owner=owner,
        self_reference=self_reference,
        is_relation=True,
    )

    return type("ForeignKey", (ForeignKeyField, BaseField), namespace)


class ForeignKeyField(BaseField):
    """
    Actual class returned from ForeignKey function call and stored in model_fields.
    """

    to: Type["Model"]
    name: str
    related_name: str  # type: ignore
    virtual: bool
    ondelete: str
    onupdate: str

    @classmethod
    def get_source_related_name(cls) -> str:
        """
        Returns name to use for source relation name.
        For FK it's the same, differs for m2m fields.
        It's either set as `related_name` or by default it's owner model. get_name + 's'
        :return: name of the related_name or default related name.
        :rtype: str
        """
        return cls.get_related_name()

    @classmethod
    def get_related_name(cls) -> str:
        """
        Returns name to use for reverse relation.
        It's either set as `related_name` or by default it's owner model. get_name + 's'
        :return: name of the related_name or default related name.
        :rtype: str
        """
        return cls.related_name or cls.owner.get_name() + "s"

    @classmethod
    def evaluate_forward_ref(cls, globalns: Any, localns: Any) -> None:
        """
        Evaluates the ForwardRef to actual Field based on global and local namespaces

        :param globalns: global namespace
        :type globalns: Any
        :param localns: local namespace
        :type localns: Any
        :return: None
        :rtype: None
        """
        if cls.to.__class__ == ForwardRef:
            cls.to = evaluate_forwardref(
                cls.to,  # type: ignore
                globalns,
                localns or None,
            )
            (
                cls.__type__,
                cls.constraints,
                cls.column_type,
            ) = populate_fk_params_based_on_to_model(
                to=cls.to,
                nullable=cls.nullable,
                ondelete=cls.ondelete,
                onupdate=cls.onupdate,
            )

    @classmethod
    def _extract_model_from_sequence(
        cls, value: List, child: "Model", to_register: bool,
    ) -> List["Model"]:
        """
        Takes a list of Models and registers them on parent.
        Registration is mutual, so children have also reference to parent.

        Used in reverse FK relations.

        :param value: list of Model
        :type value: List
        :param child: child/ related Model
        :type child: Model
        :param to_register: flag if the relation should be set in RelationshipManager
        :type to_register: bool
        :return: list (if needed) registered Models
        :rtype: List["Model"]
        """
        return [
            cls.expand_relationship(  # type: ignore
                value=val, child=child, to_register=to_register,
            )
            for val in value
        ]

    @classmethod
    def _register_existing_model(
        cls, value: "Model", child: "Model", to_register: bool,
    ) -> "Model":
        """
        Takes already created instance and registers it for parent.
        Registration is mutual, so children have also reference to parent.

        Used in reverse FK relations and normal FK for single models.

        :param value: already instantiated Model
        :type value: Model
        :param child: child/ related Model
        :type child: Model
        :param to_register: flag if the relation should be set in RelationshipManager
        :type to_register: bool
        :return: (if needed) registered Model
        :rtype: Model
        """
        if to_register:
            cls.register_relation(model=value, child=child)
        return value

    @classmethod
    def _construct_model_from_dict(
        cls, value: dict, child: "Model", to_register: bool
    ) -> "Model":
        """
        Takes a dictionary, creates a instance and registers it for parent.
        If dictionary contains only one field and it's a pk it is a __pk_only__ model.
        Registration is mutual, so children have also reference to parent.

        Used in normal FK for dictionaries.

        :param value: dictionary of a Model
        :type value: dict
        :param child: child/ related Model
        :type child: Model
        :param to_register: flag if the relation should be set in RelationshipManager
        :type to_register: bool
        :return: (if needed) registered Model
        :rtype: Model
        """
        if len(value.keys()) == 1 and list(value.keys())[0] == cls.to.Meta.pkname:
            value["__pk_only__"] = True
        model = cls.to(**value)
        if to_register:
            cls.register_relation(model=model, child=child)
        return model

    @classmethod
    def _construct_model_from_pk(
        cls, value: Any, child: "Model", to_register: bool
    ) -> "Model":
        """
        Takes a pk value, creates a dummy instance and registers it for parent.
        Registration is mutual, so children have also reference to parent.

        Used in normal FK for dictionaries.

        :param value: value of a related pk / fk column
        :type value: Any
        :param child: child/ related Model
        :type child: Model
        :param to_register: flag if the relation should be set in RelationshipManager
        :type to_register: bool
        :return: (if needed) registered Model
        :rtype: Model
        """
        if cls.to.pk_type() == uuid.UUID and isinstance(value, str):  # pragma: nocover
            value = uuid.UUID(value)
        if not isinstance(value, cls.to.pk_type()):
            raise RelationshipInstanceError(
                f"Relationship error - ForeignKey {cls.to.__name__} "
                f"is of type {cls.to.pk_type()} "
                f"while {type(value)} passed as a parameter."
            )
        model = create_dummy_instance(fk=cls.to, pk=value)
        if to_register:
            cls.register_relation(model=model, child=child)
        return model

    @classmethod
    def register_relation(cls, model: "Model", child: "Model") -> None:
        """
        Registers relation between parent and child in relation manager.
        Relation manager is kep on each model (different instance).

        Used in Metaclass and sometimes some relations are missing
        (i.e. cloned Models in fastapi might miss one).

        :param model: parent model (with relation definition)
        :type model: Model class
        :param child: child model
        :type child: Model class
        """
        model._orm.add(
            parent=model, child=child, field=cls,
        )

    @classmethod
    def has_unresolved_forward_refs(cls) -> bool:
        """
        Verifies if the filed has any ForwardRefs that require updating before the
        model can be used.

        :return: result of the check
        :rtype: bool
        """
        return cls.to.__class__ == ForwardRef

    @classmethod
    def expand_relationship(
        cls,
        value: Any,
        child: Union["Model", "NewBaseModel"],
        to_register: bool = True,
    ) -> Optional[Union["Model", List["Model"]]]:
        """
        For relations the child model is first constructed (if needed),
        registered in relation and returned.
        For relation fields the value can be a pk value (Any type of field),
        dict (from Model) or actual instance/list of a "Model".

        Selects the appropriate constructor based on a passed value.

        :param value: a Model field value, returned untouched for non relation fields.
        :type value: Any
        :param child: a child Model to register
        :type child: Union["Model", "NewBaseModel"]
        :param to_register: flag if the relation should be set in RelationshipManager
        :type to_register: bool
        :return: returns a Model or a list of Models
        :rtype: Optional[Union["Model", List["Model"]]]
        """
        if value is None:
            return None if not cls.virtual else []
        constructors = {
            f"{cls.to.__name__}": cls._register_existing_model,
            "dict": cls._construct_model_from_dict,
            "list": cls._extract_model_from_sequence,
        }

        model = constructors.get(  # type: ignore
            value.__class__.__name__, cls._construct_model_from_pk
        )(value, child, to_register)
        return model

    @classmethod
    def get_relation_name(cls) -> str:  # pragma: no cover
        """
        Returns name of the relation, which can be a own name or through model
        names for m2m models

        :return: result of the check
        :rtype: bool
        """
        return cls.name

    @classmethod
    def get_source_model(cls) -> Type["Model"]:  # pragma: no cover
        """
        Returns model from which the relation comes -> either owner or through model

        :return: source model
        :rtype: Type["Model"]
        """
        return cls.owner
