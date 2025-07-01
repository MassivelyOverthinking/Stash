# 📦 Stash - Memory Optimisation Class-Decorator

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - 0.1.0](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

## What is Stash?

Stash is a '__slots__'-based Python class-decorator developed to assist Python developers in 
significantly reducing memory overhead when initiating individual classes. It dynamically creates a new optimised class with necessary dunder-methods behind the scene (__init__, __repr__, __eq__), and also add user-specified methods to ensure custom functionality. The application also supports immutability through 'Freeze' parameter, disabling user's ability to set attribute values post-initialisation for better memory efficiency.

## 📋 Key Features
* 🎁 Simple-to-use Python class decorator for memory optimisation.
* 🛠️ Dynamically creates __slots__-based classes to minimize memory overhead.
* ⚗️ Adds essential dunder methods (__init__, __repr__, __eq__).
* 🔄 Allows user to specify class-methods to preserve and inherit.
* ❄️ Supports attribute Freeze-functionality (_frozen) for increased memory efficiency.
* 📊 Retains original class metadata for analysis, debugging and introspection.

---

## 🧠 Installation

Install Stash using your preferred Package Manager.
```bash
pip install Stash
# or
poetry add Stash
# or
conda install Stash 
```

## #️⃣ Code Example

```python
from Stash import Stash

@Stash
class Example():
    name: str
    age: 
    is_single: bool

# An __init__-method is automatically generated similar to @dataclass

example1 = Example(
    name="Tony Stark",
    age=34,
    is_single=False
)

print(example1.name)        # Tony Stark
print(example1.age)         # 34
print(example1.is_single)   # False
```

## 🧊 Freeze mechanic

Stash also supports immutability by disabling modifications to instance attributes after initialization. By setting `freeze=True`, individual instances become read-only. Any attempts to odify or change attributes raises and `AttributeError`.

```python
from Stash import Stash

@Stash(freeze=True)
class Example():
    name: str
    age: int
    is_villain: bool

example1 = Example(
    name="Otto Octavius",
    age=52, 
    is_villain=True
)

example1.name = "Norman Osborn"     # Raises an AttributeError, as value are immutable.
```