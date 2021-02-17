#!./venv/bin/python

# Multi BIP32: will work with all coins where they already implemented
# any kind of BIP32, so we will not focus only on secp256k1, but also
# on ed25519, and on Cardano's modified ed25519.
#
# We will also try to limit ourselves to our target use-case:
# generating private/public keypairs in a trezor/ledger nano
# compatible way.

from enum import Enum
from typing import NamedTuple, Tuple

from base58 import XRP_ALPHABET, b58decode_check, b58encode_check
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat
from electrum import bitcoin
from electrum_ltc import bitcoin as litecoin
from eth_utils.crypto import keccak
from stellar_sdk.keypair import Keypair
from web3 import Web3
from pytezos.crypto.key import Key as TezosKey

from lib import secp256k1, utils


class Version(Enum):
    PUBLIC = 0x0488B21E
    PRIVATE = 0x0488ADE4


class Key:
    def get_public_bytes(self) -> bytes:
        raise Exception("abstract", self)

    def get_private_bytes(self) -> bytes:
        raise Exception("abstract", self)

    def hardened_derivation(self, chain_code: bytes, child_index: int) -> Tuple["Key", bytes]:
        raise Exception("abstract", self)

    def derivation(self, chain_code: bytes, child_index: int) -> Tuple["Key", bytes]:
        raise Exception("abstract", self)


# Derivation is similar for public and private bytes, so we try to abstract...
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
class Secp256k1Deriv(Key):
    def __init__(self, p1):
        raise Exception("abstract", self)

    def derive(self, il):
        raise Exception("abstract", self)

    def derivation(self, chain_code: bytes, child_index: int) -> Tuple["Secp256k1Deriv", bytes]:
        if child_index < 0 or child_index >= 2 ** 31:
            raise Exception("invalid child index")
        I = utils.hmac512(chain_code, self.get_public_bytes() + utils.tb(child_index, 4))
        return (self.__class__(self.derive(Secp256k1Priv(I[0:32]))), I[32:])


class Secp256k1Pub(Secp256k1Deriv):
    def __init__(self, key: bytes):
        self.key = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256K1(),
            key,
        )

    def __str__(self):
        return f"<Secp256k1Pub {self.get_public_bytes().hex()}>"

    def get_public_bytes(self):
        return self.key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    def hardened_derivation(self, *_args):
        raise Exception("impossible")

    def derive(self, il):
        return secp256k1.add_pubkeys(self.get_public_bytes(), il.get_public_bytes())


class Secp256k1Priv(Secp256k1Deriv):
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

    def hardened_derivation(self, chain_code: bytes, child_index: int) -> Tuple["Secp256k1Priv", bytes]:
        if child_index < 0 or child_index >= 2 ** 31:
            raise Exception("invalid hardened child index")
        I = utils.hmac512(chain_code, b"\x00" + self.get_private_bytes() + utils.tb(child_index + 0x80000000, 4))
        return (Secp256k1Priv(self.derive(Secp256k1Priv(I[0:32]))), I[32:])

    def derive(self, il):
        return secp256k1.add_privkeys(self.get_private_bytes(), il.get_private_bytes())


class ED25519Pub(Key):
    def __init__(self, key: bytes):
        self.key = ed25519.Ed25519PublicKey.from_public_bytes(key)

    def __str__(self):
        return f"<ED25519Pub {self.get_public_bytes().hex()}>"

    def get_public_bytes(self):
        return self.key.public_bytes(Encoding.Raw, PublicFormat.Raw)

    def hardened_derivation(self, *_args):
        raise Exception("impossible")

    def derivation(self, *_args):
        raise Exception("impossible, XLM doesn't support xpub derivation")


class ED25519Priv(Key):
    def __init__(self, key: bytes):
        self.key = ed25519.Ed25519PrivateKey.from_private_bytes(key)

    def __str__(self):
        return f"<ED25519Priv {self.get_public_bytes().hex()}>"

    def get_public_bytes(self):
        return self.key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    def get_private_bytes(self):
        return self.key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

    def hardened_derivation(self, chain_code: bytes, child_index: int) -> Tuple["ED25519Priv", bytes]:
        if child_index < 0 or child_index >= 2 ** 31:
            raise Exception("invalid hardened child index")
        I = utils.hmac512(chain_code, b"\x00" + self.get_private_bytes() + utils.tb(child_index + 0x80000000, 4))
        return (ED25519Priv(I[0:32]), I[32:])

    def derivation(self, *_args):
        raise Exception("impossible, XLM doesn't support non-hardened derivation")


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
            if key[0] == 255:
                # non standard, invented by this project :(
                k = ED25519Pub(key[1:])
            else:
                k = Secp256k1Pub(key)
        elif xkey[0:4].hex() == "0488ade4":
            vrs = Version.PRIVATE
            if key[0] == 255:
                # non standard, invented by this project :(
                k = ED25519Priv(key[1:])
            elif key[0] == 0:
                k = Secp256k1Priv(key[1:])
            else:
                raise Exception("Incorrect private key while parsing XKey")
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

    @classmethod
    def from_seed(cls, seed: bytes) -> "XKey":
        I = utils.hmac512(b"Bitcoin seed", seed)
        return XKey(Version.PRIVATE, 0, b"\x00\x00\x00\x00", 0, False, I[32:], Secp256k1Priv(I[0:32]))

    @classmethod
    def from_seed_ed25519(cls, seed: bytes) -> "XKey":
        I = utils.hmac512(b"ed25519 seed", seed)
        return XKey(Version.PRIVATE, 0, b"\x00\x00\x00\x00", 0, False, I[32:], ED25519Priv(I[0:32]))

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

    def _to_bytes(self) -> bytes:
        ret = utils.tb(self.version.value, 4)
        ret += utils.tb(self.depth, 1)
        ret += self.parent_fp
        cn = self.child_number
        if self.hardened:
            cn += 0x80000000
        ret += utils.tb(cn, 4)
        ret += self.chain_code
        if self.version == Version.PUBLIC:
            if isinstance(self.key, ED25519Pub):
                # non standard, invented by this project :(
                ret += b"\xff" + self.key.get_public_bytes()
            else:
                ret += self.key.get_public_bytes()
        elif self.version == Version.PRIVATE:
            if isinstance(self.key, ED25519Priv):
                # non standard, invented by this project :(
                ret += b"\xff" + self.key.get_private_bytes()
            else:
                ret += b"\x00" + self.key.get_private_bytes()
        else:
            raise Exception("Incorrect version while dumping an XKey")
        return ret

    def to_xkey(self):
        return b58encode_check(self._to_bytes())

    def neuter(self):
        if isinstance(self.key, Secp256k1Priv):
            return XKey(Version.PUBLIC, self.depth, self.parent_fp, self.child_number, self.hardened, self.chain_code, Secp256k1Pub(self.key.get_public_bytes()))
        elif isinstance(self.key, ED25519Priv):
            # Ed25519 doesn't support public derivation, so we zero out the chain code, to be safe
            return XKey(Version.PUBLIC, self.depth, self.parent_fp, self.child_number, self.hardened, b"\x00" * 32, ED25519Pub(self.key.get_public_bytes()))
        else:
            raise Exception("Only secp256k1 or ed25519 private xkeys can be neutered")

    def derivation(self, child_index: str):
        if child_index[-1] in "hH'\"":
            hardened = True
            ci = int(child_index[:-1])
        else:
            hardened = False
            ci = int(child_index)
        if hardened:
            k, cc = self.key.hardened_derivation(self.chain_code, ci)
        else:
            k, cc = self.key.derivation(self.chain_code, ci)
        return XKey(self.version, self.depth + 1, self.fp(), ci, hardened, cc, k)

    # We use electrum here instead of a smaller library,
    # because we haven't found one that:
    #  - has a good API (easy to use),
    #  - has type annotations,
    #  - is maintained.
    def to_btc(self, type: str) -> str:
        if self.version == Version.PRIVATE:
            return bitcoin.serialize_privkey(self.key.get_private_bytes(), True, type)
        else:
            return bitcoin.pubkey_to_address(type, self.key.get_public_bytes().hex())

    def to_ltc(self, type: str) -> str:
        if self.version == Version.PRIVATE:
            return litecoin.serialize_privkey(self.key.get_private_bytes(), True, type)
        else:
            return litecoin.pubkey_to_address(type, self.key.get_public_bytes().hex())

    def to_eth(self) -> str:
        if self.version == Version.PRIVATE:
            return self.key.get_private_bytes().hex()
        else:
            if isinstance(self.key, Secp256k1Pub):
                return Web3.toChecksumAddress(keccak(self.key.key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)[1:]).hex()[24:])
            else:
                raise NotImplementedError("eth addr from non-public secp256k1")

    def to_xrp(self) -> str:
        if self.version == Version.PRIVATE:
            return "xrp-hex:" + self.key.get_private_bytes().hex()
        else:
            return b58encode_check(b"\x00" + utils.ripemd(utils.sha256(self.key.get_public_bytes())), XRP_ALPHABET).decode("ascii")

    def to_xlm(self) -> str:
        if self.version == Version.PRIVATE:
            return Keypair.from_raw_ed25519_seed(self.key.get_private_bytes()).secret
        else:
            return Keypair.from_raw_ed25519_public_key(self.key.get_public_bytes()).public_key

    def to_xtz(self) -> str:
        if self.version == Version.PRIVATE:
            return TezosKey.from_secret_exponent(self.key.get_private_bytes()).secret_key()
        else:
            return TezosKey.from_public_point(self.key.get_public_bytes()).public_key_hash()


if __name__ == "__main__":
    # This is xprv from "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst"
    # at path 44' -> 144'
    xk = XKey.from_xkey("xprv9wx8CqATXR9ebGGh1Ya2JHrT8QaCtQpwd16C9DzGH7q8twWFKWnW9c4EPiYV6BU4GHJJJnmaYDJFxi6Cace8i2CPbPdVN2hdSf9ZJpuQZDP")
    print(xk)
