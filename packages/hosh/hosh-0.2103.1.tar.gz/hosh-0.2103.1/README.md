![test](https://github.com/davips/hosh/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/hosh/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/hosh)

# hosh
Fast cryptographic hash (half-blake3) and operators for Rust and Python.

## Python installation
### from package
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI
pip install hosh
```

### from source
```bash
cd my-project
git clone https://github.com/davips/hosh ../hosh
pip install -e ../hosh
```


### Examples
**Basic operations**
<details>
<p>

```python3
from hosh import Hash

# Hashes can be multiplied.
a = Hash(blob=b"Some large binary content...")
b = Hash(blob=b"Some other binary content. Might be, e.g., an action or another large content.")
c = a * b
print(f"{a} * {b} = {c}")
"""
0Sux8dX5O3gkPx5KkGKYKP * 0Q7q8pNuFRZwoBBzM1RYiq = 0EHzVjd9q7pK4AmiZlCffL
"""
```

```python3

# Multiplication can be reverted by the inverse hash. Zero is the identity hash.
print(f"{b} * {~b} = {b * ~b} = 0")
"""
0Q7q8pNuFRZwoBBzM1RYiq * 3TW3af8GIVKzzojLZbBqq5 = 0000000000000000000000 = 0
"""
```

```python3

print(f"{c} * {~b} = {c * ~b} = {a} = a")
"""
0EHzVjd9q7pK4AmiZlCffL * 3TW3af8GIVKzzojLZbBqq5 = 0Sux8dX5O3gkPx5KkGKYKP = 0Sux8dX5O3gkPx5KkGKYKP = a
"""
```

```python3

print(f"{~a} * {c} = {~a * c} = {b} = b")
"""
6Ms8EdXd3yzeddcxefn5FF * 0EHzVjd9q7pK4AmiZlCffL = 0Q7q8pNuFRZwoBBzM1RYiq = 0Q7q8pNuFRZwoBBzM1RYiq = b
"""
```

```python3

# Division is shorthand for reversion.
print(f"{c} / {b} = {c / b} = a")
"""
0EHzVjd9q7pK4AmiZlCffL / 0Q7q8pNuFRZwoBBzM1RYiq = 0Sux8dX5O3gkPx5KkGKYKP = a
"""
```

```python3

# Hash multiplication is not expected to be commutative.
print(f"{a * b} != {b * a}")
"""
0EHzVjd9q7pK4AmiZlCffL != 3qXz8PSpGGugRb0jP9BEzd
"""
```

```python3

# Hash multiplication is associative.
print(f"{a * (b * c)} = {(a * b) * c}")
"""
2xWdrj6rCfITvCfiU31v96 = 2xWdrj6rCfITvCfiU31v96
"""
```

```python3


```


</p>
</details>




### Features
