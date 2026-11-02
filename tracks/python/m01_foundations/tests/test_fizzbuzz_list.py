from fizzbuzz_list import fizzbuzz_list


def test_five():
    assert fizzbuzz_list(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fifteen_end():
    assert fizzbuzz_list(15)[-1] == "FizzBuzz"
    assert len(fizzbuzz_list(15)) == 15


def test_zero():
    assert fizzbuzz_list(0) == []


def test_types():
    assert all(isinstance(x, str) for x in fizzbuzz_list(10))
