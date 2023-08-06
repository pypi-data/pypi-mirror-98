# Ruled-Password-Generator

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hkcomori/ruled-password-generator/test)](https://github.com/hkcomori/ruled-password-generator/actions/workflows/deploy.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hkcomori/ruled-password-generator?label=version)](https://pypi.org/ruled-password-generator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ruled-password-generator)](https://pypi.org/project/ruled-password-generator/)
[![GitHub](https://img.shields.io/github/license/hkcomori/ruled-password-generator)](https://github.com/hkcomori/ruled-password-generator/blob/main/LICENSE)

**A password generator with customizable rules.**

* Generate a password of the given length.
* Generate a password from given letters.
* Generate non duplicate passwords.

## Install

``` bash
pip install ruled-passwd-generator
```

## Usage (Example)

### Generate a password with 12 letters which have non-duplicate letters

``` python
from ruled_password_generator import PasswordGenerator

pwg = PasswordGenerator(12, uniques=-1)
password = pwg.generate()
```

### Generate a password with 10 to 16 letters which have at least 9 non-duplicate letters

``` python
pwg = PasswordGenerator(10, 16, uniques=9)
password = pwg.generate()
```

### Generate a password with 10 letters which have given letters

* Password has at least 3 letters in 'ABCDEF'.
* Password has at least 4 letters in '123456789'.
* Password has at least 1 letters in '-'.

``` python
rules = {'ABCDEF': 3, '123456789': 4, '-': 1}
pwg = PasswordGenerator(10, rules=rules)
password = pwg.generate()
```

If no rules are given, the default rules are following:
* It has [lowercases](https://docs.python.org/ja/3/library/string.html#string.ascii_lowercase) at least one.
* It has [uppercases](https://docs.python.org/ja/3/library/string.html#string.ascii_uppercase) at least one.
* It has [digits](https://docs.python.org/ja/3/library/string.html#string.digits) at least one.
* It has [symbols](https://docs.python.org/ja/3/library/string.html#string.punctuation) at least one.

### Generate 20 unique passwords

``` python
passwords = pwg.bulk_generate(20, unique=True)
```

## Contributions
Contributions are welcomed via PR.

## License
 * [MIT](LICENSE)
