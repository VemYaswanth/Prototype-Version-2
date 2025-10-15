import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# NOTE: For demo purposes; use a KMS in production

def pad(s: bytes) -> bytes:
    pad_len = 16 - len(s) % 16
    return s + bytes([pad_len]) * pad_len

def unpad(s: bytes) -> bytes:
    pad_len = s[-1]
    return s[:-pad_len]

def aes_encrypt(plaintext: str, key: bytes) -> str:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext.encode()))
    return base64.b64encode(iv + ct).decode()

def aes_decrypt(token: str, key: bytes) -> str:
    raw = base64.b64decode(token)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct))
    return pt.decode()