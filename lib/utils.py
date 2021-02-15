import hashlib
import hmac
import sys

def hmac512(key: bytes, msg: bytes) -> bytes:
    return hmac.digest(key, msg, hashlib.sha512)

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def ripemd(x):
    md = hashlib.new('ripemd160')
    md.update(x)
    return md.digest()

def hash_160(x: bytes) -> bytes:
    return ripemd(sha256(x))

def fb(b: bytes) -> int:
    return int.from_bytes(b, "big")

def tb(i: int, l: int) -> bytes:
    return int.to_bytes(i, length = l, byteorder = "big")

def one_line_from_stdin() -> str:
    lines = [x.strip() for x in sys.stdin.readlines()]

    if len(lines) != 1:
        print("wrong input")
        sys.exit(1)

    return lines[0]
