"""Yet another fixed width integer (library)."""

from ctypes import (c_int16, c_int32, c_int64, c_int8,
                    c_uint16, c_uint32, c_uint64, c_uint8)
from functools import wraps
from sys import byteorder
from typing import Callable, ClassVar, Optional, Tuple, Type, TypeVar

__all__ = ('FixedWidthInt', 'BaseFixedWidthInt', 'generate_int',
           'int8', 'int16', 'int32', 'int64', 'int128', 'int256',
           'uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256',
           'sbyte', 'byte',
           'short', 'ushort',
           'int_', 'uint',
           'long', 'ulong')
__version__ = '1.0.1'

T = TypeVar('T', bound=int)


class FixedWidthInt(type):
    _raw: Callable[[int], int]
    _width: int
    _unsigned: bool

    @property
    def width(cls) -> int:
        return cls._width

    @property
    def unsigned(cls) -> bool:
        return cls._unsigned

    @property
    def max(cls) -> int:
        if cls._unsigned:
            return cls(2 ** cls._width - 1)
        return cls(2 ** (cls._width - 1) - 1)

    @property
    def min(cls) -> int:
        if cls._unsigned:
            return cls(0)
        return cls(-(2 ** (cls._width - 1)))


def take_wider(fn):
    @wraps(fn)
    def wrapper(self: 'BaseFixedWidthInt', other: int):
        if (isinstance(other, BaseFixedWidthInt)
                and (other.width > self.width
                     or other.width == self.width
                     and other.unsigned
                     and not self.unsigned)):
            return NotImplemented
        return fn(self, other)

    return wrapper


class BaseFixedWidthInt(int, metaclass=FixedWidthInt):
    _raw: Callable[[int], int]
    _width: ClassVar[int]
    _unsigned: ClassVar[bool]

    def __new__(cls, value: int) -> 'BaseFixedWidthInt':
        if cls is BaseFixedWidthInt:
            raise RuntimeError('Use concrete implementation, not base _Int')

        raw = cls._raw(value)
        if hasattr(raw, 'value'):
            return int.__new__(cls, raw.value)
        return int.__new__(cls, raw)

    @property
    def width(self: FixedWidthInt) -> T:
        # noinspection PyTypeChecker
        return type(self).width

    @property
    def unsigned(self: FixedWidthInt) -> bool:
        # noinspection PyTypeChecker
        return type(self).unsigned

    @property
    def max(self: FixedWidthInt) -> T:
        # noinspection PyTypeChecker
        return type(self).max

    @property
    def min(self: FixedWidthInt) -> T:
        # noinspection PyTypeChecker
        return type(self).min

    # Conversion / reprs

    def __bytes__(self) -> bytes:
        return self.to_bytes(self.width // 8,
                             byteorder=byteorder,
                             signed=not self.unsigned)

    @property
    def bin(self) -> str:
        if byteorder == 'little':
            return '0b' + ''.join(f'{b:08b}' for b in reversed(bytes(self)))
        return '0b' + ''.join(f'{b:08b}' for b in bytes(self))

    @property
    def hex(self) -> str:
        if byteorder == 'little':
            return '0x' + ''.join(f'{b:02x}' for b in reversed(bytes(self)))
        return '0x' + ''.join(f'{b:02x}' for b in bytes(self))

    def __repr__(self: T) -> str:
        if self._unsigned:
            prefix = 'u'
        else:
            prefix = ''
        return f'{prefix}int{self.width}({super().__repr__()})'

    # Arithmetic

    @take_wider
    def __add__(self: T, other: int) -> T:
        return type(self)(super().__add__(other))

    @take_wider
    def __radd__(self: T, other: int) -> T:
        return type(self)(super().__radd__(other))

    @take_wider
    def __sub__(self: T, other: int) -> T:
        return type(self)(super().__sub__(other))

    @take_wider
    def __rsub__(self: T, other: int) -> T:
        return type(self)(super().__rsub__(other))

    @take_wider
    def __mul__(self: T, other: int) -> T:
        return type(self)(super().__mul__(other))

    @take_wider
    def __rmul__(self: T, other: int) -> T:
        return type(self)(super().__rmul__(other))

    def __divmod__(self: T, other: int) -> Tuple[T, T]:
        div, mod = super().__divmod__(other)
        return type(self)(div), type(self)(mod)

    def __floordiv__(self: T, other: int) -> T:
        return type(self)(super().__floordiv__(other))

    def __mod__(self: T, other: int) -> T:
        return type(self)(super().__mod__(other))

    def __pow__(self: T, power: int, modulo: Optional[int] = None) -> T:
        return type(self)(super().__pow__(power, modulo))

    # Bitwise ops

    @take_wider
    def __and__(self: T, other: int) -> T:
        return type(self)(super().__and__(other))

    @take_wider
    def __rand__(self: T, other: int) -> T:
        return type(self)(super().__rand__(other))

    @take_wider
    def __or__(self: T, other: int) -> T:
        return type(self)(super().__or__(other))

    @take_wider
    def __ror__(self: T, other: int) -> T:
        return type(self)(super().__ror__(other))

    @take_wider
    def __xor__(self: T, other: int) -> T:
        return type(self)(super().__xor__(other))

    @take_wider
    def __rxor__(self: T, other: int) -> T:
        return type(self)(super().__rxor__(other))

    def __lshift__(self: T, other: int) -> T:
        return type(self)(super().__lshift__(other))

    def __rshift__(self: T, other: int) -> T:
        return type(self)(super().__rshift__(other))

    def __invert__(self: T) -> T:
        return type(self)(super().__invert__())

    # Other maths / conversions

    def __abs__(self: T) -> T:
        return type(self)(super().__abs__())

    def __ceil__(self: T) -> T:
        return type(self)(self)

    def __floor__(self: T) -> T:
        return type(self)(self)

    # pylint: disable=invalid-index-returned
    def __index__(self: T) -> T:
        return type(self)(self)

    def __trunc__(self: T) -> T:
        return type(self)(self)

    def __round__(self: T, n: Optional[int] = None) -> T:
        return type(self)(super().__round__(n))

    def __pos__(self: T) -> T:
        return type(self)(super().__pos__())

    def __neg__(self: T) -> T:
        return type(self)(super().__neg__())


# noinspection PyPep8Naming
class int8(BaseFixedWidthInt):
    _raw = c_int8
    _width = 8
    _unsigned = False


# noinspection PyPep8Naming
class int16(BaseFixedWidthInt):
    _raw = c_int16
    _width = 16
    _unsigned = False


# noinspection PyPep8Naming
class int32(BaseFixedWidthInt):
    _raw = c_int32
    _width = 32
    _unsigned = False


# noinspection PyPep8Naming
class int64(BaseFixedWidthInt):
    _raw = c_int64
    _width = 64
    _unsigned = False


# noinspection PyPep8Naming
class uint8(BaseFixedWidthInt):
    _raw = c_uint8
    _width = 8
    _unsigned = True


# noinspection PyPep8Naming
class uint16(BaseFixedWidthInt):
    _raw = c_uint16
    _width = 16
    _unsigned = True


# noinspection PyPep8Naming
class uint32(BaseFixedWidthInt):
    _raw = c_uint32
    _width = 32
    _unsigned = True


# noinspection PyPep8Naming
class uint64(BaseFixedWidthInt):
    _raw = c_uint64
    _width = 64
    _unsigned = True


def generate_int(width: int, unsigned: bool) -> Type[BaseFixedWidthInt]:
    name = f'int{width}'
    if unsigned:
        name = f'u{name}'

    def _raw(value: int) -> int:
        if not unsigned:
            value = value + 2 ** (width - 1)
        value = value % (2 ** width)
        if not unsigned:
            value = value - 2 ** (width - 1)
        return value

    # noinspection PyTypeChecker
    return type(name, (BaseFixedWidthInt,), {
        '_raw': _raw,
        '_width': width,
        '_unsigned': unsigned
    })


int128 = generate_int(128, unsigned=False)
uint128 = generate_int(128, unsigned=True)
int256 = generate_int(256, unsigned=False)
uint256 = generate_int(256, unsigned=True)

# Aliases
sbyte = int8
byte = uint8
short = int16
ushort = uint16
int_ = int32
uint = uint32
long = int64
ulong = uint64


def __getattr__(name: str) -> Type[BaseFixedWidthInt]:
    bits = name
    if bits.startswith('u'):
        unsigned = True
        bits = name[1:]
    else:
        unsigned = False
    if bits.startswith('int'):
        bits = bits[3:]
    else:
        raise AttributeError(name)
    if bits.isnumeric():
        width = int(bits)
    else:
        raise AttributeError(name)
    return generate_int(width, unsigned)
