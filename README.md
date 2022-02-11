# Ferris wouldn't approve!
Accessing methods in modules with :: rather than . like in Rust, using format specs

## Examples
```py
import random

import ferris_wouldnt_approve

>>> print(f"{random::randint(1, 5)}")
4

>>> print(f"{random::randint(1, 5)}")
5
```
