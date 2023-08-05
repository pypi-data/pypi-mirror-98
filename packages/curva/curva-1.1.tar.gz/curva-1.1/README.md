# Curva - ECIES based on AES and HKDF

__Repos: http://github.com/origamizyt/curva__

Simple library for Elliptic-Curve Integrated Encryption Scheme with Rijndael and Hmac-based Key Deriviation Function.

Replacement for blowcurve since blowfish is deprecated now.

## Installation

This module uses `ecdsa` and `PyCryptodome` module as backend. No DLLs are needed.

This module is avaiable on PyPI:
```
$ pip install curva
```

Or you can download the source .tar.gz and execute `setup.py` manually:
```
$ python setup.py install
```

## Usage

This module exposes interfaces for key agreement, signatures and encryptions.

Use class `curva.Curva` to access all interfaces:
```py
>>> c1 = Curva() # create instance, generate keys
>>> c2 = Curva()
```

Use its `export` / `exportHex` method to export local public key, and `load` / `loadHex` method to load remote public key:
```py
>>> c1.load(c2.export()) # bytes
>>> c2.loadHex(c1.exportHex()) # hex string
```

After exchanging public keys, a shared secret can now be established:
```py
>>> c1.secret() == c2.secret() # shared secret (bytes)
True
```

Use the `sign` / `verify` method to create signatures and verify them:
```py
>>> data = b'data'
>>> signature = c1.sign(data)
>>> c2.verify(data, signature)
True
>>> c2.verify(b'attack!', signature)
False
```

Use the `encrypt` / `decrypt` method to encrypt / decrypt data:
```py
>>> data = b'data'
>>> encrypted = c1.encrypt(data)
>>> c2.decrypt(encrypted)
b'data'
```