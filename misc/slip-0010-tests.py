#!/usr/bin/env python3

# Downloaded from https://github.com/satoshilabs/slips/blob/master/slip-0010/testvectors.py on 2021-02-09
# and adopted for python 3.
#
# License for this file is: https://github.com/satoshilabs/slips/blob/master/LICENSE

import binascii
import hashlib
import hmac
import struct
import ecdsa
import ed25519
from base58 import b58encode_check

privdev = 0x80000000

def int_to_bytes(x: int, pad: int) -> bytes:
    return int.to_bytes(x, length=pad, byteorder='big')

def bytes_to_int(s: bytes) -> int:
    return int.from_bytes(s, 'big')

# mode 0 - compatible with BIP32 private derivation
def seed2hdnode(seed: bytes, modifier: bytes, curve):
    k = seed
    while True:
        h = hmac.new(modifier, seed, hashlib.sha512).digest()
        key, chaincode = h[:32], h[32:]
        a = bytes_to_int(key)
        if (curve == 'ed25519'):
            break
        if (a < curve.order and a != 0):
            break
        seed = h
        #print 'RETRY seed: ' + binascii.hexlify(seed)
    return (key, chaincode)

def fingerprint(publickey: bytes) -> bytes:
    h = hashlib.new('ripemd160', hashlib.sha256(publickey).digest()).digest()
    return h[:4]

def b58xprv(parent_fingerprint: bytes, private_key: bytes, chain: bytes, depth: int, childnr: int) -> bytes:
    raw = (b'\x04\x88\xad\xe4' +
              int_to_bytes(depth, 1) + parent_fingerprint + int_to_bytes(childnr, 4) +
              chain + b'\x00' + private_key)
    return b58encode_check(raw)

def b58xpub(parent_fingerprint: bytes, public_key: bytes, chain: bytes, depth: int, childnr: int) -> bytes:
    raw = (b'\x04\x88\xb2\x1e' +
              int_to_bytes(depth, 1) + parent_fingerprint + int_to_bytes(childnr, 4) +
              chain + public_key)
    return b58encode_check(raw)

def publickey(private_key: bytes, curve) -> bytes:
    if curve == 'ed25519':
        sk = ed25519.SigningKey(private_key)
        return b'\x00' + sk.get_verifying_key().to_bytes()
    else:
        Q = bytes_to_int(private_key) * curve.generator
        xstr = int_to_bytes(Q.x(), 32)
        parity = Q.y() & 1
        return b'' + int_to_bytes(2 + parity, 1) + xstr

def derive(parent_key: bytes, parent_chaincode: bytes, i: int, curve):
    assert len(parent_key) == 32
    assert len(parent_chaincode) == 32
    k = parent_chaincode
    if ((i & privdev) != 0):
        key = b'\x00' + parent_key
    else:
        key = publickey(parent_key, curve)
    d = key + struct.pack('>L', i)
    while True:
        h = hmac.new(k, d, hashlib.sha512).digest()
        key, chaincode = h[:32], h[32:]
        if curve == 'ed25519':
            break
        #print 'I: ' + binascii.hexlify(h)
        a = bytes_to_int(key)
        keyi = (a + bytes_to_int(parent_key)) % curve.order
        if (a < curve.order and keyi != 0):
            key = int_to_bytes(keyi, 32)
            break
        d = b'\x01' + h[32:] + struct.pack('>L', i)
        #print 'a failed: ' + binascii.hexlify(h[:32])
        #print 'RETRY: ' + binascii.hexlify(d)

    return (key, chaincode)

def get_curve_info(curvename):
    if curvename == 'secp256k1':
        return (ecdsa.curves.SECP256k1, b'Bitcoin seed')
    if curvename == 'nist256p1':
        return (ecdsa.curves.NIST256p, b'Nist256p1 seed')
    if curvename == 'ed25519':
        return ('ed25519', b'ed25519 seed')
    raise BaseException('unsupported curve: '+curvename)

def show_testvector(name, curvename, seedhex, derivationpath):
    curve, seedmodifier = get_curve_info(curvename)
    master_seed = binascii.unhexlify(seedhex)
    k,c = seed2hdnode(master_seed, seedmodifier, curve)
    p = publickey(k, curve)
    fpr = b'\x00\x00\x00\x00'
    path = 'm'
    print("### "+name+" for "+curvename)
    print('')
    print("Seed (hex): " + seedhex)
    print('')
    print('* Chain ' + path)
    print(f'  * fingerprint: {binascii.hexlify(fpr)}')
    print(f'  * chain code: {binascii.hexlify(c)}')
    print(f'  * private: {binascii.hexlify(k)}')
    print(f'  * public: {binascii.hexlify(p)}')
    depth = 0
    print(b58xprv(fpr, k, c, depth, 0))
    print(b58xpub(fpr, p, c, depth, 0))
    for i in derivationpath:
        if curve == 'ed25519':
            # no public derivation for ed25519
            i = i | privdev
        fpr = fingerprint(p)
        depth = depth + 1
        path = path + "/" + str(i & (privdev-1))
        if ((i & privdev) != 0):
            path = path + "H"
        k,c = derive(k, c, i, curve)
        p = publickey(k, curve)
        print('* Chain ' + path)
        print(f'  * fingerprint: {binascii.hexlify(fpr)}')
        print(f'  * chain code: {binascii.hexlify(c)}')
        print(f'  * private: {binascii.hexlify(k)}')
        print(f'  * public: {binascii.hexlify(p)}')
        print(b58xprv(fpr, k, c, depth, i))
        print(b58xpub(fpr, p, c, depth, i))
    print

def show_testvectors(name, curvenames, seedhex, derivationpath):
    for curvename in curvenames:
        show_testvector(name, curvename, seedhex, derivationpath)


curvenames = ['secp256k1', 'nist256p1', 'ed25519'];

show_testvectors("Test vector 1", curvenames,
                 '000102030405060708090a0b0c0d0e0f',
                 [privdev + 0, 1, privdev + 2, 2, 1000000000])
show_testvectors("Test vector 2", curvenames,
                 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542',
                 [0, privdev + 2147483647, 1, privdev + 2147483646, 2])

show_testvectors("Test derivation retry", ['nist256p1'],
                 '000102030405060708090a0b0c0d0e0f',
                 [privdev + 28578, 33941])

show_testvectors("Test seed retry", ['nist256p1'],
                 'a7305bc8df8d0951f0cb224c0e95d7707cbdf2c6ce7e8d481fec69c7ff5e9446',
                 [])
