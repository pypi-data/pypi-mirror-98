# Dataclass Dict Convert

This library converts between python [dataclasses](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass) and dicts (and json).

It was created because when using the [dataclasses-json](https://pypi.org/project/dataclasses-json/) library for my use case, I ran into limitations and performance issues. 
(There's also [typed-json-dataclass](https://pypi.org/project/typed-json-dataclass) but I haven't evaluated that library.)

`dataclass-dict-convert` supports lists, optionals, dicts, enums, nested dataclasses, etc. 
It handles dates using RFC3339 (and enforces timezones and timezone aware `datetime`).

Example:

```python
from dataclasses import dataclass
from stringcase import camelcase
from typing import Optional, List

from dataclass_dict_convert import dataclass_dict_convert


@dataclass_dict_convert(dict_letter_case=camelcase)
@dataclass(frozen=True)
class TestB:
    an_int: int
    a_str: str
    a_float: float
    a_bool: bool


@dataclass_dict_convert(dict_letter_case=camelcase)
@dataclass(frozen=True)
class Test:
    nestedClass: TestB
    nestedInOpt: Optional[TestB]
    nestedInList: List[TestB]


the_instanceB1 = TestB(1, 'foo', 0.1, True)
the_instanceB2 = TestB(2, 'bar', 0.2, False)
the_instanceB3 = TestB(3, 'baz', 0.3, True)
the_instanceB4 = TestB(4, 'huh', 0.4, False)
the_instance = Test(the_instanceB1, the_instanceB2, [the_instanceB3, the_instanceB4])
the_dict = {
    'nestedClass': {'anInt': 1, 'aStr': 'foo', 'aFloat': 0.1, 'aBool': True, },
    'nestedInOpt': {'anInt': 2, 'aStr': 'bar', 'aFloat': 0.2, 'aBool': False, },
    'nestedInList': [
        {'anInt': 3, 'aStr': 'baz', 'aFloat': 0.3, 'aBool': True, },
        {'anInt': 4, 'aStr': 'huh', 'aFloat': 0.4, 'aBool': False, },
    ],
}

expected = the_dict
actual = the_instance.to_dict()
assert actual == expected

expected = the_instance
actual = Test.from_dict(the_dict)
assert actual == expected
```

The library also includes:
- RFC3339 tools (the default format for converting datetime to string),
- dataclass type checking tools
- dataclass copy method generator
- dataclass multiline repr (replace auto generated repr for dataclasses by a multiline version)

Links:
- Gitlab: https://gitlab.ilabt.imec.be/wvdemeer/dataclass-dict-convert
- PyPi: https://pypi.org/project/dataclass-dict-convert/
