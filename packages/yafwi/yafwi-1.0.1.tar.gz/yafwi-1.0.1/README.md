# yafwi [<img src="https://img.shields.io/gitlab/pipeline/alen/yafwi/main?gitlab_url=https%3A%2F%2Fgitlab.home.alen.sh%2F&label=Gitlab%20CI&style=flat-square" align="right">](https://gitlab.home.alen.sh/alen/yafwi) [<img src="https://img.shields.io/travis/buhanec/yafwi/master.svg?label=Travis+CI&style=flat-square" align="right">](https://travis-ci.org/buhanec/yafwi) [<img src="https://img.shields.io/azure-devops/build/buhanec/yafwi/3?label=Azure%20DevOps%20build&style=flat-square" align="right">](https://dev.azure.com/buhanec/yafwi/_build)

## Yet Another Fixed Width Integer (Library)

Simple fixed with integers for developer experimentation.

# Usage

## Installation

Available through [yafwi - PyPI](https://pypi.org/project/yafwi/) using `pip install yafwi`.

## Some Examples

```python
>>> from yafwi import *
>>> from yafwi import __all__
>>> __all__
('FixedWidthInt', 'BaseFixedWidthInt', 'generate_int', 
 'int8', 'int16', 'int32', 'int64', 'int128', 'int256', 
 'uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256', 
 'sbyte', 'byte', 'short', 'ushort', 'int_', 'uint', 'long', 'ulong')

>>> int8(120)
int8(120)

>>> int8(120) + 120  # Arithmetic with Python int preserves type
int8(-16)
>>> int8(120) + int16(120)  # Arithmetic will take result in larger width
int16(240)

>>> int16.max, int16.min  # Utility sentinels
(int16(32767), int16(-32768))
>>> uint32.min, uint32.max
(uint32(0), uint32(4294967295))

>>> int8(0b11110000)  # Utility represenations
int8(-16)
>>> int8(0b11110000).bin
'0b11110000'
>>> int8(0b11110000).hex
'0xf0'

>>> (~int8(0b10010110)).bin
'0b01101001'
>>> (int8(0b10010110) >> 2).bin
'0b11100101'
>>> (int8(0b10010110) << 2).bin
'0b01011000'
>>> ((uint32(uint8.max) << 10 | uint8.max) ^ uint32.max - (1 << 31)).bin
'0b01111111111111000000001100000000'

>>> bytes(uint32(8))  # Output depends on system byteorder
b'\x08\x00\x00\x00'  
>>> uint32(8).hex  # Output independent of system byteorder
'0x00000008'
```

## Convenient Aliases

```python
>>> from yafwi import *

>>> uint is uint32
True
>>> long is int64
True
>>> ushort is uint16
True
[...]
```

## Arbitrary Sizes

```python
>>> import yafwi

>>> yafwi.generate_int(1024, unsigned=True)
<class 'yafwi.uint1024'>
>>> yafwi.int512
<class 'yafwi.int512'>

>>> yafwi.int3.max, yafwi.int3.min  # Including some fun ones... 
(int3(3), int3(-4))
```

# Platform Independence

If run on a big-endian system, the bytes associated with the numbers will be different, but higher-level functionality should remain unchanged.
