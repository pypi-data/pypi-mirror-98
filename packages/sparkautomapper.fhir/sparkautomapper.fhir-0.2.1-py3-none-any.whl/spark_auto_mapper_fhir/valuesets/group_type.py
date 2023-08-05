from typing import Callable, Any, Type

from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType

from spark_auto_mapper_fhir.valuesets.FhirValueSetBase import FhirValueSetBase


class GroupTypeCode(FhirValueSetBase):
    def __init__(self, value: AutoMapperTextInputType):
        assert not isinstance(value, str) or value in [
            "person", "animal", "practitioner", "device", "medication",
            "substance"
        ]
        super().__init__(value=value)

    # noinspection PyPep8Naming,SpellCheckingInspection
    class classproperty(object):
        def __init__(self, f: Callable[..., 'GroupTypeCode']) -> None:
            self.f: Callable[..., 'GroupTypeCode'] = f

        def __get__(
            self, obj: Any, owner: Type['GroupTypeCode']
        ) -> 'GroupTypeCode':
            return self.f(owner)

    # noinspection PyMethodParameters
    @classproperty
    def person(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("person")

    # noinspection PyMethodParameters
    @classproperty
    def animal(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("animal")

    # noinspection PyMethodParameters
    @classproperty
    def practitioner(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("practitioner")

    # noinspection PyMethodParameters
    @classproperty
    def device(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("device")

    # noinspection PyMethodParameters
    @classproperty
    def medication(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("medication")

    # noinspection PyMethodParameters
    @classproperty
    def substance(cls) -> 'GroupTypeCode':
        """
        Male
        """
        # noinspection PyCallingNonCallable
        return GroupTypeCode("substance")
