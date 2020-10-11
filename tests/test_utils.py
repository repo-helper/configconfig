# stdlib
from enum import Enum
from typing import Dict, List, Union

# 3rd party
import pytest
from typing_extensions import Literal

# this package
from configconfig.utils import check_union, get_json_type, get_yaml_type


def test_check_union():
	assert check_union("abc", Union[str, int])
	assert check_union(123, Union[str, int])
	assert not check_union(123, Union[str, bool])

	assert check_union("abc", List[str])
	assert check_union(123, List[int])
	assert not check_union("abc", List[int])
	assert not check_union(123, List[str])


class MyEnum(str, Enum):
	dog = "dog"
	cat = "cat"


@pytest.mark.parametrize(
		"value, expects",
		[
				(str, {'type': 'string'}),
				(int, {'type': 'number'}),
				(float, {'type': 'number'}),
				(dict, {'type': 'object'}),
				(bool, {'type': ['boolean', 'string']}),
				(list, {'type': 'array'}),
				(Dict, {'type': 'object'}),
				(Dict[str, int], {'type': 'object'}),
				(List, {'type': 'array'}),
				(List[str], {'items': {'type': 'string'}, 'type': 'array'}),
				(List[int], {'items': {'type': 'number'}, 'type': 'array'}),
				(List[float], {'items': {'type': 'number'}, 'type': 'array'}),
				(Union[str, float], {'type': ['string', 'number']}),
				(Literal["dog", "cat"], {'enum': ['dog', 'cat']}),
				(MyEnum, {'enum': ['dog', 'cat']}),
				]
		)
def test_get_json_type(value, expects):
	assert get_json_type(value) == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				(str, "String"),
				(int, "Integer"),
				(float, "Float"),
				(dict, "Mapping"),
				(bool, "Boolean"),
				(list, "Sequence"),
				(Dict, "Mapping"),
				(List, "Sequence"),
				(List[str], "Sequence of String"),
				(List[int], "Sequence of Integer"),
				(List[float], "Sequence of Float"),
				(Union[str, float], "String or Float"),
				(Literal["dog", "cat"], "'dog' or 'cat'"),
				(MyEnum, "'dog' or 'cat'"),
				]
		)
def test_get_yaml_type(value, expects):
	assert get_yaml_type(value) == expects
