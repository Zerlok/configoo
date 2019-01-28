# Python configoo

A simple library for loading application configurations from files, environments and etc. Configuration variables declares in ORM model class maner to make it easier to use config variables in code with IDE syntax highlights.

## Setup

TODO: write it

## Example

```python
# config.py

from configoo import Model, field, load_from_env

class Config(Model):
    """A simple configuration model.

    FOO - an integer value (default value is 123)
    BAR - a string value (must be specified in config source, otherwise the exception about missed field value will be thrown)
    """

    FOO = field.Integer(default=123)
    BAR = field.List(field.String(), required=True)

# Load `Config` field from process environment.
config = load_from_env(Config)


# test.py

# Assume environment contains:
#   FOO="321"
#   BAR="1,2,3"

from config import config

print(config.FOO, type(config.FOO)) # 321 <class 'int'>
print(config.BAR, type(config.BAR)) # [1, 2, 3] <class 'list'>

```
