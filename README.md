# 📦 Stash (Memory Optimisation Class-Decorator)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - 0.1.0](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

Stash is a '__slots__'-based Python class-decorator developed to assist Python developers in 
significantly reducing memory overhead when initiating individual classes. It dynamically creates a new optimised class with necessary dunder-methods behind the scene (__init__, __repr__, __eq__), and also add user-specified methods to ensure custom functionality. The application also supports immutability through 'Freeze' parameter, disabling user's ability to set attribute values post-initialisation for better memory efficiency.

## 📋 Key Features
* 🎁 Versatile Python class-decorator.
* 🛠️ Dynamically creates a new memory efficient class-object.
* ⚗️ Utilises __slots__ to store varaibles and respective values.
* 🔄 Allows user to specify class-methods to preserve and inherit.
* ❄️ Supports attribute Freeze-functionality (_frozen) for increased memory efficiency.
* 📊 Preserves original class metadata for improved analysis and tracking.