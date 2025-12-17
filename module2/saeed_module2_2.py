"""Custom simple symmetric text cipher.

This module provides `custom_encrypt` and `custom_decrypt` functions.

Encryption method (design summary):
- Step 1: Convert input text to UTF-8 bytes.
- Step 2: Derive a repeating key-bytes sequence from the provided key string.
- Step 3: For each byte, compute a transformed byte = ((b ^ key_byte) + pos) & 0xFF,
  where `pos` is the byte index (0-based). This combines XOR with a
  position-dependent additive shift to make identical bytes map differently
  depending on position.
- Step 4: Output is base64-url-safe encoded string of the transformed bytes.

Notes / security:
- This is a custom, non-standard cipher intended for learning/demo only.
- Do NOT use this for real security-sensitive data. Use established
  algorithms (e.g., AES-GCM) for production.

Functions:
- `custom_encrypt(plaintext: str, key: str) -> str` : returns encrypted base64 string
- `custom_decrypt(ciphertext_b64: str, key: str) -> str` : returns original plaintext

"""
import base64
from typing import Sequence


def _key_bytes(key: str) -> bytes:
    return key.encode("utf-8") if key is not None else b""


def custom_encrypt(plaintext: str, key: str) -> str:
    """Encrypt `plaintext` with `key` and return a url-safe base64 string.

    Method details:
    - Convert plaintext -> bytes.
    - Create repeating key bytes from `key`.
    - For each byte at index `i`: t = ((b ^ k) + i) & 0xFF
    - Return base64.urlsafe_b64encode(transformed_bytes).decode()

    """
    if plaintext is None:
        raise TypeError("plaintext must be a string")
    if key is None:
        raise TypeError("key must be a string")

    data = plaintext.encode("utf-8")
    kb = _key_bytes(key)
    if len(kb) == 0:
        raise ValueError("key must be non-empty")

    out = bytearray(len(data))
    for i, b in enumerate(data):
        k = kb[i % len(kb)]
        out[i] = ((b ^ k) + i) & 0xFF

    return base64.urlsafe_b64encode(bytes(out)).decode("ascii")


def custom_decrypt(ciphertext_b64: str, key: str) -> str:
    """Reverse `custom_encrypt` and return the plaintext string.

    Raises ValueError on malformed input or incorrect key.
    """
    if ciphertext_b64 is None:
        raise TypeError("ciphertext_b64 must be a string")
    if key is None:
        raise TypeError("key must be a string")

    try:
        data = base64.urlsafe_b64decode(ciphertext_b64.encode("ascii"))
    except Exception as e:
        raise ValueError("ciphertext is not valid base64") from e

    kb = _key_bytes(key)
    if len(kb) == 0:
        raise ValueError("key must be non-empty")

    out = bytearray(len(data))
    for i, t in enumerate(data):
        k = kb[i % len(kb)]
        # reverse: b = ((t - i) & 0xFF) ^ k
        b = ((t - i) & 0xFF) ^ k
        out[i] = b

    try:
        return out.decode("utf-8")
    except Exception as e:
        raise ValueError("decrypted bytes are not valid UTF-8") from e


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4 and sys.argv[1] in ("enc", "dec"):
        mode = sys.argv[1]
        key = sys.argv[2]
        rest = " ".join(sys.argv[3:])
        if mode == "enc":
            print(custom_encrypt(rest, key))
        else:
            try:
                print(custom_decrypt(rest, key))
            except Exception as e:
                print("Error:", e)
    else:
        print("Usage:")
        print("  python module2/saeed_module2_2.py enc <key> <text to encrypt>")
        print("  python module2/saeed_module2_2.py dec <key> <base64-cipher>")
