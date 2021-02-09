#!./venv/bin/python

# Multi BIP32: will work with all coins where they already implemented
# any kind of BIP32, so we will not focus only on secp256k1, but also
# on ed25519, and on Cardano's modified ed25519.
#
# We will also try to limit ourselves to our target use-case:
# generating private/public keypairs in a trezor/ledger nano
# compatible way.

from enum import Enum
from typing import NamedTuple, Union

from base58 import b58decode_check, b58encode_check
from electrum import ecc
from electrum.crypto import hash_160

from lib import utils


class Version(Enum):
    PUBLIC = 0x0488B21E
    PRIVATE = 0x0488ADE4


class XKey(NamedTuple):
    version: Version
    depth: int
    parent_fp: bytes
    child_number: int
    hardened: bool
    chain_code: bytes
    key: Union[ecc.ECPubkey, ecc.ECPrivkey]

    @classmethod
    def from_xkey(cls, xkey: str) -> "XKey":
        xkey = b58decode_check(xkey)
        vrs = None
        key = xkey[13 + 32 :]
        k = None
        if len(key) != 33:
            raise Exception("Incorrect key length while parsing XKey")
        if xkey[0:4].hex() == "0488b21e":
            vrs = Version.PUBLIC
            k = ecc.ECPubkey(key)
        elif xkey[0:4].hex() == "0488ade4":
            vrs = Version.PRIVATE
            if key[0] != 0:
                raise Exception("Incorrect private key while parsing XKey")
            k = ecc.ECPrivkey(key[1:])
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
        return hash_160(self.key.get_public_key_bytes(compressed=True))

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
        if self.version == Version.PUBLIC and isinstance(self.key, ecc.ECPubkey):
            ret += self.key.get_public_key_bytes()
        elif self.version == Version.PRIVATE and isinstance(self.key, ecc.ECPrivkey):
            ret += b"\x00" + self.key.get_secret_bytes()
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
