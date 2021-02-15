#!./venv/bin/python

# Extra functions from libsecp256k1.so.0, which are not available from pyca/cryptography.

import ctypes
import secrets

secp256k1 = ctypes.cdll.LoadLibrary('libsecp256k1.so.0')
secp256k1.secp256k1_context_create.argtypes = [ctypes.c_uint]
secp256k1.secp256k1_context_create.restype = ctypes.c_void_p
secp256k1.secp256k1_context_randomize.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
secp256k1.secp256k1_context_randomize.restype = ctypes.c_int
secp256k1.secp256k1_ec_pubkey_combine.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t]
secp256k1.secp256k1_ec_pubkey_combine.restype = ctypes.c_int
secp256k1.secp256k1_ec_pubkey_parse.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
secp256k1.secp256k1_ec_pubkey_parse.restype = ctypes.c_int
secp256k1.secp256k1_ec_pubkey_serialize.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
secp256k1.secp256k1_ec_pubkey_serialize.restype = ctypes.c_int
secp256k1.secp256k1_ec_pubkey_tweak_add.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
secp256k1.secp256k1_ec_pubkey_tweak_add.restype = ctypes.c_int
SECP256K1_FLAGS_TYPE_MASK = ((1 << 8) - 1)
SECP256K1_FLAGS_TYPE_CONTEXT = (1 << 0)
SECP256K1_FLAGS_TYPE_COMPRESSION = (1 << 1)
SECP256K1_FLAGS_BIT_CONTEXT_VERIFY = (1 << 8)
SECP256K1_FLAGS_BIT_CONTEXT_SIGN = (1 << 9)
SECP256K1_FLAGS_BIT_COMPRESSION = (1 << 8)
SECP256K1_CONTEXT_VERIFY = (SECP256K1_FLAGS_TYPE_CONTEXT | SECP256K1_FLAGS_BIT_CONTEXT_VERIFY)
SECP256K1_CONTEXT_SIGN = (SECP256K1_FLAGS_TYPE_CONTEXT | SECP256K1_FLAGS_BIT_CONTEXT_SIGN)
SECP256K1_CONTEXT_NONE = (SECP256K1_FLAGS_TYPE_CONTEXT)
SECP256K1_EC_COMPRESSED = (SECP256K1_FLAGS_TYPE_COMPRESSION | SECP256K1_FLAGS_BIT_COMPRESSION)
SECP256K1_EC_UNCOMPRESSED = (SECP256K1_FLAGS_TYPE_COMPRESSION)

_ctx = secp256k1.secp256k1_context_create(SECP256K1_CONTEXT_SIGN | SECP256K1_CONTEXT_VERIFY)
if 1 != secp256k1.secp256k1_context_randomize(_ctx, secrets.token_bytes(32)):
    raise Exception("randomization failed")

def _parse_pubkey(pk: bytes) -> "ctypes.c_char_p":
    ret = ctypes.create_string_buffer(64)
    if 0 == secp256k1.secp256k1_ec_pubkey_parse(_ctx, ret, pk, len(pk)):
        raise Exception("parse failed")
    return ctypes.cast(ret, ctypes.c_char_p)

def add_pubkeys(pk1b: bytes, pk2b: bytes) -> bytes:
    pk1 = _parse_pubkey(pk1b)
    pk2 = _parse_pubkey(pk2b)
    cmb = ctypes.create_string_buffer(64)
    if 0 == secp256k1.secp256k1_ec_pubkey_combine(_ctx, cmb, (ctypes.c_char_p * 2)(pk1, pk2), 2):
        raise Exception("combine failed")

    ret = ctypes.create_string_buffer(33)
    ret_size = ctypes.c_size_t(33)
    secp256k1.secp256k1_ec_pubkey_serialize(_ctx, ret, ctypes.byref(ret_size), cmb, SECP256K1_EC_COMPRESSED)
    if ret_size.value != 33:
        raise Exception("serialize failed")

    return bytes(ret)

def add_privkeys(k1b: bytes, k2b: bytes) -> bytes:
    if 0 == secp256k1.secp256k1_ec_seckey_tweak_add(_ctx, k1b, k2b):
        raise Exception("tweak failed")
    return k1b
