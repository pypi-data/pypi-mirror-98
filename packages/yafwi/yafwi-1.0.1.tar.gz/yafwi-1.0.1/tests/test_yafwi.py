from hypothesis import assume, given
from hypothesis.strategies import composite, integers, sampled_from
import pytest

from yafwi import *


@pytest.mark.parametrize('cls, expected', [
    (sbyte, int8),
    (byte, uint8),
    (short, int16),
    (ushort, uint16),
    (int_, int32),
    (uint, uint32),
    (long, int64),
    (ulong, uint64),
])
def test_aliases(cls: FixedWidthInt, expected: FixedWidthInt):
    assert cls is expected


@pytest.mark.parametrize('cls, min_val, max_val', [
    (int8, -128, 127),
    (uint8, 0, 255),
    (int16, -32768, 32767),
    (uint16, 0, 65535),
    (int32, -2147483648, 2147483647),
    (uint32, 0, 4294967295),
    (int64, -9223372036854775808, 9223372036854775807),
    (uint64, 0, 18446744073709551615),
    (int128, -170141183460469231731687303715884105728, 170141183460469231731687303715884105727),
    (uint128, 0, 340282366920938463463374607431768211455),
    (int256, -57896044618658097711785492504343953926634992332820282019728792003956564819968, 57896044618658097711785492504343953926634992332820282019728792003956564819967),
    (uint256, 0, 115792089237316195423570985008687907853269984665640564039457584007913129639935),
])
def test_limits(cls: FixedWidthInt, min_val: int, max_val: int):
    assert isinstance(cls.min, cls)
    assert cls.min == min_val
    assert isinstance(cls.max, cls)
    assert cls.max == max_val


@pytest.mark.parametrize('cls', [
    int8, uint8, int16, uint16, int32, uint32,
    int64, uint64, int128, uint128, int256, uint256,
])
def test_overflow(cls: FixedWidthInt):
    assert cls.max + 1 == cls.min
    assert cls.min - 1 == cls.max


@given(reference=sampled_from((int8, uint8, int16, uint16,
                               int32, uint32, int64, uint64)),
       value=integers(min_value=int(int64.min) * 100,
                      max_value=int(uint64.max) * 100))
def test_generated(reference, value):
    generated = generate_int(reference.width, reference.unsigned)
    assert generated(value) == reference(value)


@composite
def ref_and_value(draw, references=(int8, uint8, int16, uint16,
                                    int32, uint32, int64, uint64,
                                    int128, uint128, int256, uint256)):
    reference = draw(sampled_from(references))
    value = draw(integers(min_value=reference.min, max_value=reference.max))
    return reference, value


@given(ref=ref_and_value())
def test_eq(ref):
    reference, value = ref
    assert reference(value) == value
    assert reference(value) >= value
    assert reference(value) <= value
    assert reference(value) == reference(value)
    assert reference(value) >= reference(value)
    assert reference(value) <= reference(value)


@composite
def ref_and_neq_values(draw, references=(int8, uint8, int16, uint16,
                                         int32, uint32, int64, uint64,
                                         int128, uint128, int256, uint256)):
    reference = draw(sampled_from(references))
    value1 = draw(integers(min_value=reference.min, max_value=reference.max))
    value2 = draw(integers(min_value=reference.min, max_value=reference.max))
    assume(value1 != value2)
    return reference, value1, value2


@given(ref=ref_and_neq_values())
def test_neq(ref):
    reference, value1, value2 = ref
    assert reference(value1) != value2
    assert reference(value2) != value1
    assert reference(value1) != reference(value2)


@composite
def ref_and_lt_values(draw, references=(int8, uint8, int16, uint16,
                                         int32, uint32, int64, uint64,
                                         int128, uint128, int256, uint256)):
    reference = draw(sampled_from(references))
    value1 = draw(integers(min_value=reference.min, max_value=reference.max))
    value2 = draw(integers(min_value=reference.min, max_value=reference.max))
    assume(value1 < value2)
    return reference, value1, value2


@given(ref=ref_and_lt_values())
def test_lt_gt(ref):
    reference, value1, value2 = ref
    assert reference(value1) < value2
    assert reference(value1) <= value2
    assert reference(value2) > value1
    assert reference(value2) >= value1
    assert reference(value1) < reference(value2)
    assert reference(value1) <= reference(value2)
    assert reference(value2) > reference(value1)
    assert reference(value2) >= reference(value1)
