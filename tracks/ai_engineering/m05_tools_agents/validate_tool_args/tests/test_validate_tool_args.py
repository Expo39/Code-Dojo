from validate_tool_args import validate_tool_args

SCHEMA = {"city": {"type": "str", "required": True}, "days": {"type": "int"}}


def test_example():
    assert validate_tool_args(SCHEMA, {"days": "3", "units": "c"}) == [
        "missing required argument 'city'",
        "argument 'days' must be int, got str",
        "unknown argument 'units'",
    ]


def test_a_valid_call_gives_an_empty_list():
    assert validate_tool_args(SCHEMA, {"city": "Lyon", "days": 3}) == []
    assert validate_tool_args(SCHEMA, {"city": "Lyon"}) == []


def test_trace_bool_is_not_a_number_and_an_int_is_not_a_bool():
    schema = {"n": {"type": "float", "required": True}, "on": {"type": "bool"}}
    assert validate_tool_args(schema, {"on": 1, "n": True, "x": 0}) == [
        "argument 'n' must be float, got bool",
        "argument 'on' must be bool, got int",
        "unknown argument 'x'",
    ]


def test_an_int_is_fine_where_a_float_is_expected():
    assert validate_tool_args({"n": {"type": "float"}}, {"n": 3}) == []
    assert validate_tool_args({"n": {"type": "int"}}, {"n": 3.0}) == ["argument 'n' must be int, got float"]


def test_a_missing_optional_argument_is_fine_and_none_is_a_wrong_type():
    assert validate_tool_args({"a": {"type": "str"}}, {}) == []
    assert validate_tool_args({"a": {"type": "str"}}, {"a": None}) == ["argument 'a' must be str, got NoneType"]


def test_schema_errors_come_in_schema_order_then_unknown_in_args_order():
    schema = {"b": {"type": "str", "required": True}, "a": {"type": "str", "required": True}}
    assert validate_tool_args(schema, {"z": 1, "y": 2}) == [
        "missing required argument 'b'", "missing required argument 'a'",
        "unknown argument 'z'", "unknown argument 'y'",
    ]


def test_empty_schema_and_empty_args():
    assert validate_tool_args({}, {}) == []
    assert validate_tool_args({}, {"x": 1}) == ["unknown argument 'x'"]
