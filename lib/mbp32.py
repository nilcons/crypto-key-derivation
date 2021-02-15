#!./venv/bin/python

# Multi BIP32: will work with all coins where they already implemented
# any kind of BIP32, so we will not focus only on secp256k1, but also
# on ed25519, and on Cardano's modified ed25519.
#
# We will also try to limit ourselves to our target use-case:
# generating private/public keypairs in a trezor/ledger nano
# compatible way.

from enum import Enum
from typing import NamedTuple

from base58 import b58decode_check, b58encode_check
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from lib import utils


class Version(Enum):
    PUBLIC = 0x0488B21E
    PRIVATE = 0x0488ADE4


class Key:
    def get_public_bytes(self) -> bytes:
        raise Exception("abstract", self)

    def get_private_bytes(self) -> bytes:
        raise Exception("abstract", self)


class Secp256k1Pub(Key):
    def __init__(self, key: bytes):
        self.key = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256K1(),
            key,
        )

    def __str__(self):
        return f"<Secp256k1Pub {self.get_public_bytes().hex()}>"

    def get_public_bytes(self):
        return self.key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)


class Secp256k1Priv(Key):
    def __init__(self, key: bytes):
        self.key = ec.derive_private_key(int.from_bytes(key, "big"), ec.SECP256K1())

    def __str__(self):
        return f"<Secp256k1Priv {self.get_public_bytes().hex()}>"

    def get_public_bytes(self):
        return self.key.public_key().public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    def get_private_bytes(self):
        # I think this should be the supported API, but seems not to be working...
        # return self.key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        return self.key.private_numbers().private_value.to_bytes(length=32, byteorder="big")


class XKey(NamedTuple):
    version: Version
    depth: int
    parent_fp: bytes
    child_number: int
    hardened: bool
    chain_code: bytes
    key: Key

    @classmethod
    def from_xkey(cls, xkey: str) -> "XKey":
        xkey = b58decode_check(xkey)
        vrs = None
        key = xkey[13 + 32 :]
        k: Key
        if len(key) != 33:
            raise Exception("Incorrect key length while parsing XKey")
        if xkey[0:4].hex() == "0488b21e":
            vrs = Version.PUBLIC
            k = Secp256k1Pub(key)
        elif xkey[0:4].hex() == "0488ade4":
            vrs = Version.PRIVATE
            if key[0] != 0:
                raise Exception("Incorrect private key while parsing XKey")
            k = Secp256k1Priv(key[1:])
        else:
            raise Exception("Incorrect version while parsing XKey")
        d = xkey[4]
        pfp = xkey[5:9]
        cn = utils.fb(xkey[9:13])
        hardened = False
        if cn >= 0x80000000:
            cn -= 0x80000000
            hardened = True
        cc = xkey[13 : 13 + 32]
        return XKey(vrs, d, pfp, cn, hardened, cc, k)

    def __str__(self):
        return f"{self.version.name}({self.parent_fp.hex()}--{self.depth}:{self.child_number_with_tick()}-->{self.fp().hex()})"

    def child_number_with_tick(self) -> str:
        if self.hardened:
            return f"{self.child_number}'"
        else:
            return f"{self.child_number}"

    def keyid(self):
        return utils.hash_160(self.key.get_public_bytes())

    def fp(self):
        return self.keyid()[:4]

    def to_bytes(self) -> bytes:
        ret = utils.tb(self.version.value, 4)
        ret += utils.tb(self.depth, 1)
        ret += self.parent_fp
        cn = self.child_number
        if self.hardened:
            cn += 0x80000000
        ret += utils.tb(cn, 4)
        ret += self.chain_code
        if self.version == Version.PUBLIC:
            ret += self.key.get_public_bytes()
        elif self.version == Version.PRIVATE:
            ret += b"\x00" + self.key.get_private_bytes()
        else:
            raise Exception("Incorrect version while dumping an XKey")
        return ret

    def to_xkey(self):
        return b58encode_check(self.to_bytes())


if __name__ == "__main__":
    # This is xprv from "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst"
    # at path 44' -> 144'
    xk = XKey.from_xkey("xprv9wx8CqATXR9ebGGh1Ya2JHrT8QaCtQpwd16C9DzGH7q8twWFKWnW9c4EPiYV6BU4GHJJJnmaYDJFxi6Cace8i2CPbPdVN2hdSf9ZJpuQZDP")
    print(xk)
