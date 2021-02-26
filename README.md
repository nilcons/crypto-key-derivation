# crypto-key-derivation
Document all the mess around bip32+bip39+bip44 and similar key generation schemes

# Overview
Our overall goal is to generate bitcoin/litecon/ethereum/etc
private+public keys from a list of english words.  We also want to
keep compatibility with hardware wallets (Trezor One and Ledger Nano
S), so we can use this tool in an emergency when a hardware wallet is
not available.  If you want other hardware wallets to be tested too,
feel free to donate.

BIP39: Given a list of words, generate a seed (512 bit),
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

BIP32: Given a seed (any 128-512 bit will do), generate a master key
which can be used to generate further subkeys.

BIP44: Just a bunch of recommendations on how to use BIP39+BIP32
together.  This is followed by some wallets (e.g. Trezor), while not
followed by others (e.g. Electrum).

Useful docs derivation paths and standards:
  - https://docs.trezor.io/trezor-firmware/misc/coins-bip44-paths.html
  - https://github.com/satoshilabs/slips/blob/master/slip-0044.md
  - https://github.com/trezor/trezor-firmware/tree/master/python/src/trezorlib
  - https://github.com/satoshilabs/slips/blob/master/slip-0010/testvectors.py

# Setup

    rm -rf venv
    python3.9 -m venv venv
    . venv/bin/activate
    pip install -U pip wheel
    echo $PWD >venv/lib/python3.9/site-packages/crypto-key-derivation.pth
    pip install -r requirements.txt
    pip install -r requirements2.txt
    touch venv/lib/python3.9/site-packages/electrum/py.typed
    touch venv/lib/python3.9/site-packages/electrum_ltc/py.typed
    sudo apt install libsecp256k1-0

# BIP39
Online tool: https://iancoleman.github.io/bip39/#english

The standard BIP39 seed derivation can be used like this:

    $ ./bip39.py <<EOF
      scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
      TREZOR
      EOF
    7b4a10be9d98e6cba265566db7f136718e1398c71cb581e1b2f464cac1ceedf4f3e274dc270003c670ad8d02c4558b2f8e39edea2775c9e232c7cb798b069e88

The string "TREZOR" here is the so called passphrase, which in BIP39
makes it possible for the user to add an additional phrase not in an
english dictionary.  You do not have to use it if you don't want to:

    $ ./bip39.py <<EOF
      scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
      EOF
    a555426999448df9022c3afc2ed0e4aebff3a0ac37d8a395f81412e14994efc960ed168d39a80478e0467a3d5cfc134fef2767c1d3a27f18e3afeb11bfc8e6ad

# BIP39, Electrum variant
If you create a new wallet with Electrum, they use a modified version
of BIP39, because they have some reasons how theirs is better...

    $ ./electrum_mnemonic.py <<EOF
      scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
      TREZOR
      EOF
    7d8b4005aa5e21e438057535a8a37944f5b110f3df91743bca22ffdcd2690fd1d83611d7740719199fa3e6093a756b2bf6a4e1975da733a114325733b056d86a
    $ ./electrum_mnemonic.py <<EOF
      scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
      EOF
    d27376868abe32360d112c0afd31298b0d5a91d895a3edebbccabb96a58161b67a2e7f35902d958bb3fedac0b818c87ce7e97b5309af612ee0a539ed029a107b

# BIP32
Once we have a seed, we can use BIP32 for the derivation of a
hierarchy of keys.

The tree starts with one root, and every node in the tree can have
2^31 non-hardened and 2^31 hardened child.

The generation unfortunately generates invalid children with
probability less than 1/2^127.  We haven't made any effort in this
toolchain to handle or detect these issues...

Every level (including the root and the leafs) of the hierarchy has a
so called extended private key, from which everything below the tree
can be generated.  This is a string starting with "xprv".  From this
we can generate an extended public key (starting with "xpub"), which
can be used to generate the 2^31 non-hardened sub extended public
keys.  Subnodes are indexed from 0 to 2^31-1.

This means that as far as you are using non-hardened derivation paths,
you can generate all the valid public keys from the root without
knowing any of the secrets.  This can be used to gather balances
without having the ability to spend them (e.g. webshop).

Math warning: anyone who has the extended public key, and just ONE
(non-extended, normal) secret key, can calculate all the secret keys
in the whole hierarcy (up and down and sideways), until a hardening
boundary is met.

The standard notation of a path in the tree is like this:
"m/44'/0'/0'/1/3".  Here we generating the root from a seed and then
taking the path of: harden 44 -> harden 0 -> harden 0 -> non-harden 1
-> non-harden 3.  Note the apostrophes, when they are present, that's
a hardened derivation in the path.  According to BIP44, this is the
4th change address of the first account in a wallet.

We provide the following utilities to walk the tree:

`seed2xprv.py`: stdin is a hex encoded seed from the BIP39 chapter,
stdout is an xprv, containing the root of the tree.  This path is
usually called "m" or "m/".

`seed2xprv-ed25519.py`: same as `seed2xprv.py`, but have to use this
one if you are generating XLM or XTZ addresses.

`xderive.py 10`: stdin is an xprv/xpub, output is the xprv/xpub of
10th child on the next level.

`xderive.py 10h`: stdin is an xprv/xpub, output is the xprv/xpub of
10th hardened child on the next level.

`xderive.py n`: stdin is an xprv, output is the xpub (that doesn't
have the secret anymore).

`x2btc.py`: stdin is an xprv/xpub, output is a BTC secret key or
address.  You can use https://www.bitaddress.org/ to check the keypair.

`x2eth.py`: stdin is an xprv/xpub, output is an ETH secret key or
address.  You can use https://www.myetherwallet.com/, to check the keypair.

`x2xrp.py`: stdin is an xprv/xpub, output is an XRP secret key (usable
with http://ripplerm.github.io/ripple-wallet/) or an XRP address.

`x2xlm.py`: stdin is an xprv or an xpub, output is an XLM private key or address.

`tools/xkeydump.py`: stdin is an xprv or an xpub, stdout is human readable dump.

Examples:

    $ ./seed2xprv.py <<< 000102030405060708090a0b0c0d0e0f
    xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
    $ ./xderive.py n <<< xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
    xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8
    $ ./xderive.py 0 <<< xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U
    xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt
    $ echo "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U" | ./xderive.py 0 n
    xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH
    $ ./xderive.py 2147483647h <<< xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt
    xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9
    $ ./xderive.py 1 <<< xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a
    xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon
    $ ./x2btc.py <<< xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP
    p2pkh:L15hj1TsQC1eCnMwd4CkZTGh8iusyHjDtz2oNL968oPz9dXGEeP4
    $ echo "xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP" | ./xderive.py n | ./x2btc.py
    19C8rUkmD1QG13qrpqypo3pEGuVMfEd8q5

You can also get segwit addresses or P2SH compatible segwit addresses:

    $ echo "xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP" | ./xderive.py n | ./x2btc.py p2wpkh
    bc1qt8wzxfq4p2ufpumd6w02p7kdr5c7uaqeekmeje
    $ echo "xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP" | ./xderive.py n | ./x2btc.py p2wpkh-p2sh
    37GxRVzwaiQ7vdZbVJpmfG64gy8tWWomFz

Note, that for P2SH and legacy the casing of the address is important,
for the new segwit address type everything is lowercase.

# A full example for BTC+Electrum

Given the initial seed of "aerobic melody aerobic join crunch quiz
ring icon brisk speak someone marine", we generate the electrum
specific binary seed, from which we get an xprv and convert it to
xpub.  Once we have the xpub, the only thing we need to know is that
Electrum stores public addresses at "m/0/i" and change addresses at
"m/1/i".

Therefore:

    $ ./electrum_mnemonic.py <<< "aerobic melody aerobic join crunch quiz ring icon brisk speak someone marine" | ./seed2xprv.py | ./xderive.py 0 n | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xderive.py $i | ./x2btc.py ; done ; }
    19C8rUkmD1QG13qrpqypo3pEGuVMfEd8q5
    17p8unm85w7uDVpxhp16y6DKbJJT8S3ZgY
    1JkEikqjLMVpJLBUPwK3HqbTkMYN1tw6jg
    13Vzzos4GGiFuojJfphZnp56Z1wTgf84RB
    1PTp9KgEHM3oqN6jJuFjVgG3Dq4ZiedxNU
    12YA627tRfApBriCtwhA5gDqp4FhNjVTEX
    15xN2PGGhHdf8d186HmT81o87Vuof66Ycj
    12Uhpf3GDSeENinsVwdYZEH11YRSJ1ovcC
    18kBZBYU3rRSgFJSDmRqBR5Qha7eid88BN
    1JvxirnjZrvCeQtZivYisZUDKixuUvdA1L
    1KgGzrtDLyrgQXpymVWoMXovq8kV1A64Ya
    1P8L8eG1LTDUQCAsRR1LWqj2gZKkK1z8WD
    113SW2JqU5xDGVYckTcvWM9pWnfnUp8ehv
    1LQyZWScfG5Y81DwxUgPdJJbpAk3ZWWr1f
    17x4Lmw6yYa7zieziWmjsgLLYTsGwzgyrf
    1DmsZGdvwpBN4HZqATjSxcX9rnpXgVXb49
    1NMFAKSy3zKMA7tb7RicXG8Y1ESN5j67xJ
    126TCaqairxXAY3M1PCD3UokubBh6rN8aN
    1HJpJnHX2q1GZQHPKg1vLG2dkL6CNMr3E9
    15Ve2ATPKfSQrwvzn72yUPunQj3Eao7EyC

And for the change addresses:

    $ ./electrum_mnemonic.py <<< "aerobic melody aerobic join crunch quiz ring icon brisk speak someone marine" | ./seed2xprv.py | ./xderive.py 1 n | { read xpub ; for i in `seq 0 4` ; do echo $xpub | ./xderive.py $i | ./x2btc.py ; done ; }
    1MTWgVQQLEj8YMckR2p6CuXyc3AviAHkY5
    17TBRJy4NG6sqmfMYnKJ2bb7w7prb2mDAx
    1BTY3J6dqst3zYjQtpty3HGxomUAQ4D2Vv
    1GfzFS1hyeMfch3nFc3ghosYK2MJrcnuJ5
    1JfLH3gU9iTeb19w2P6MbdxPyXePozepNz

Compatiblity with Electrum 2.9.3 has been verified on 2017-10-19.

Compatiblity with Electrum 4.0.9 has been verified on 2021-02-08.

# A full example for BTC+Trezor/LedgerNanoS

Given the following trezor seed: nation grab van ride cloth wash
endless gorilla speed core dry shop raise later wedding sweet minimum
rifle market inside have ill true analyst

You can generate the first 2 addresses of the first legacy, segwit and
native segwit account like this:

    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py ; done ; }
    1GhzX8gLBfG96Qg1mk9S5ckhVPsxeeBiSC
    18sRn1xohBhxHH9XZHgFBmZmuH5cUWpWwz
    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 49h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py p2wpkh-p2sh ; done ; }
    39Fh4GYAW5QWuT118vYMhfatQtz5UcTaa7
    38xnPRH891kEGkqQKi7yF3uPACGksjp56B
    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py p2wpkh ; done ; }
    bc1q4qfcaq4fzcn3q5tvksds4e00hs45fcu6pznsy8
    bc1qgwtfdq3jzv2324hy7l9575x73sjmgky0ky08fk

Or if you have a secret wallet with the passphrase of "do not
show my wife", then you can get the addresses like this:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py ; done ; }
    1Hvv8XyMtT8QGAXLTRE1bgEYbpfj7bZmN9
    1JiWHCAHmzsfJcag78339H1UNbkgb7cyTz
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 49h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py p2wpkh-p2sh ; done ; }
    3FdXjsy32tZdrma6WvApUvFwFv8oNhPnp1
    3AuVfCnp19R8Eoa5CZXeGJjU1TQDy6fW58
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 0h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py p2wpkh ; done ; }
    bc1q3jl5dkp57fgs3uxcyz56dpdgv7d3pg00jvlxc3
    bc1q7u0hytrgmd6xllkrz0npflcpzukjdktg6zuu6v

Get the private keys for the last 2 output:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 0h 0h 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2btc.py p2wpkh ; done ; }
    p2wpkh:Kwo5JqiLtw3ktrzQ3aqqJ3hoVfNcgCJZZ7TCbvrXjhz8tqQNPrQu
    p2wpkh:L1cc4Q1UTmzgcE8p7pgNX4pnekyejbDfXbH1rh3WHTpTdgVbmJmq

4 modes have been checked for compatility with a real Trezor on 2017-10-19:

  - legacy + no passphrase,
  - legacy + passphrase,
  - segwit + no passphrase,
  - segwit + passphrase.

6 modes have been checked for compatility with a real Trezor on 2021-02-08:

  - legacy + no passphrase,
  - legacy + passphrase,
  - segwit + no passphrase,
  - segwit + passphrase,
  - segwit native + no passphrase,
  - segwit native + passphrase,
  - private key matches public key was checked for "segwit native + passphrase".

4 modes have been checked with Ledger Nano S on 2021-02-08:

  - segwit + no passphrase,
  - segwit + passphrase,
  - segwit native + no passphrase,
  - segwit native + passphrase.

# A full example for LTC+Trezor/LedgerNanoS

Legacy address and it's secret key:

    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 2h 0h n 0 0 |./x2ltc.py
    LRZrQayJyVWwQQw9VRVz1uDq3y42pwzLu7
    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 2h 0h 0 0 |./x2ltc.py
    p2pkh:TAFkrmCtXjVUMXJdthrspNi3Km3dQkq2VFixFGNERs83VtM9kArH

Segwit address and it's secret key:

    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 49h 2h 0h 0 0 |./x2ltc.py p2wpkh-p2sh
    p2wpkh-p2sh:T7bFZEhuwmcRF3eaYHyuDeEJLaU549KKBoKUL3Exhf9Kaa9TAQJq
    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 49h 2h 0h 0 0 n |./x2ltc.py p2wpkh-p2sh
    MKMPWJ4t5h3sbZTYgPraevEYqecQKSz46Z

Native segwit address and it's secret key:

    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 2h 0h 0 0 |./x2ltc.py p2wpkh
    p2wpkh:T5J1kC22CWCZeDnhaKm7qWa3Ur5xk9SfRKw4iVm784qMLD3F5B7Z
    $ echo "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 2h 0h 0 0 n |./x2ltc.py p2wpkh
    ltc1qcnwyxrceaz50ygfdqxd3at48j474sxtsnpz8y3

Same tests with passphrase:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\nabc" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 2h 0h 0 0 n |./x2ltc.py
    LduZ8dL5REw7NnhNx9j5qBwdUfqPP9Sb4f
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\nabc" | ./bip39.py | ./seed2xprv.py | ./xderive.py 49h 2h 0h 0 0 n |./x2ltc.py p2wpkh-p2sh
    MG6vu3q25343H9JHkn3jAXffKsJbLua2Vx
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\nabc" | ./bip39.py | ./seed2xprv.py | ./xderive.py 84h 2h 0h 0 0 n |./x2ltc.py p2wpkh
    ltc1qhqw64frfanzsktas5xtykpz0gxszzljrcwlmzz

4 modes have been checked with Ledger Nano S on 2021-02-16:
  - legacy NOT SUPPORTED by Ledger Nano S,
  - segwit + no passphrase,
  - segwit + passphrase,
  - native segwit + no passphrase,
  - native segwit + passphrase.

4 modes have been checked with Trezor One on 2021-02-16:
  - native segwit NOT SUPPORTED by Trezor One,
  - legacy + no passphrase,
  - legacy + passphrase.
  - segwit + no passphrase,
  - segwit + passphrase.

# A full example of ETH/ETC+Trezor/LedgerNanoS

First 2 private keys for Ethereum and for Ethereum Classic without passphrase:

    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv.py | ./xderive.py 44h 60h 0h 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    bb36972e4db24cffd1dba3342c4c801c3344fe429500bdba192e2f49673f9139
    6a72d0345f06270cabe20f8f218f25073108586bc81c985eaa02a27533949a35
    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv.py | ./xderive.py 44h 61h 0h 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    fc265563c97398fc26f6e47eda38827f865dead4f853f2f571654f4eaf6667f0
    31a6315abcc2fdcb47c14eea6d7c1b357cfdfe17674f34f43af7722d87d2350d

Addresses for these:

    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv.py | ./xderive.py 44h 60h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    0x154D15BB73A7c01a208D3b7fEB1d77cd65756f86
    0xf8dFcB912129C22Db155Fb861D6F7A9DdDAEe0Be
    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv.py | ./xderive.py 44h 61h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    0x919903583020fb1dc543284bcD75d4737baD415A
    0x3e605cD53A01Cbe4604f4C750855874CC90D6116

First 2 private keys for Ethereum and for Ethereum Classic with passphrase:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 60h 0h 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    be080f5d5bd51985b05b001159a1bb5676309006577e0c2711658b96face6c57
    115bf63c5495145d99434db3408cb323664c427c45a0a46b5b5e5a6dadc70ab1
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 61h 0h 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    8c7e65a7d43fbfca98ad6127511fd41a4d3ebc6adc976d8239bdc8f18e2b3e7d
    21f8616e3f200fdc7054565a7be929acf91ebd884b7244ea8727a7d9393d4820

Addresses for these:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 60h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    0xc629c12cea4a2Cf61286F46649282f482A872bbd
    0x961b12F54a3132b4EaA6108349FeBC90531B2bbb
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 61h 0h n 0 | { read xpub ; for i in `seq 0 1` ; do echo $xpub | ./xderive.py $i | ./x2eth.py ; done ; }
    0xACAA32F9dD8c6a028A78140bFCe50dCEcAA74554
    0xd01629D284C7d7d7D261d5F847328B23645Fb7E0

Compatibility for all these use cases (ETH/ETC with or without passphrase) has been checked:
  - Trezor 2021-02-08,
  - Ledger Nano S 2021-02-08,
  - myetherwallet.com 2021-02-08.

# XLM (Stellar) + Trezor/LedgerNanoS

Unfortunately XLM (Stellar) uses the BIP32 derivation a bit
differently (because it uses the curve ed25519 instead of secp256k1).

The ED25519 curve doesn't support the same trick regarding
public-private derivations as Secp256k1.  (Although Cardano has an
extension to make it happen, but that extension is not used by
Stellar.)

This means that with XLM, you will always have to use private hardened
derivations and then only in the last step (before printing the
address) can you go to xpub with `xprv2xpub.py`.

Also note, that we had to extend the xpub/xprv format a bit, to
represent the fact that the key is an ed25519 key, not a secp256k1, so
the intermediate xprv/xpub strings might not be compatible with any
other tool when using XLM.  If you find any RFC/SLIP/BIP that
documents how to properly encode xprv/xpub for XLM, please contact us
via Github.

First keypair without passphrase:

    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv-ed25519.py | ./xderive.py 44h 148h 0h | ./x2xlm.py
    SCGVFOJNHSOR55IAQQT2R6PFHEHCD3HVTB7PGTC3DNVL74LZQBYUBHAT
    $ ./bip39.py <<< "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./seed2xprv-ed25519.py | ./xderive.py 44h 148h 0h n | ./x2xlm.py
    GD23O4PMK22FKSQECOOBOE3WUEPHTB2QKMALHZIADYREY3WGZFUBHNFX

First keypair with passphrase:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv-ed25519.py | ./xderive.py 44h 148h 0h | ./x2xlm.py
    SB5UTCQCF3DO54PRN2TXDV2UGJR6UEBMNGMVFRWXMRM2U6W5WC7FJRNZ
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv-ed25519.py | ./xderive.py 44h 148h 0h n | ./x2xlm.py
    GB7MHY2KDXUW6MY3PPACEOJOFSZ7EFDSY4L2C3Z4AF5VT7WPJ6R3KO3V

Compatibility has been checked:
  - Trezor One on 2021-02-08,
  - Ledger Nano S on 2021-02-08.

# XRP (Ripple)

Info about XRP key generation in the original XRP wallet: https://xrpl.org/cryptographic-keys.html

Info about address encoding: https://xrpl.org/accounts.html#address-encoding

Trezor One doesn't support XRP.  The Ledger Nano S wallet supports XRP
with derivation path of m/44'/144'/0'/0/0.  But the resulting keypair
at this derivation path is used DIRECTLY, and the picture described in
the XRP documentation
(https://xrpl.org/cryptographic-keys.html#secp256k1-key-derivation) is
not used at all.

This means that XRP is a very weird crypto regarding BIP32: I can
generate you the public key that will be the same as Ledger Nano's
key, but I can't give you a private seed that XRP wallets will accept,
because the XRP wallets want to have a seed and then run the algorithm
in the above picture on the seed to get the private key.  But we don't
have a seed, we have the private key itself.  So because of this, the
`x2xrp.py` tool will never be able to give you a secret seed usable with
native XRP tools.

To interact with the XRP chain without a hardware wallet, somebody
would have to implement a desktop/javascript client that accepts a
private key (in some encoding, e.g. hex), instead of a seed.  And
there is an implementation like that, here:
http://ripplerm.github.io/ripple-wallet/

So in an emergency, when you don't have a hardware wallet, and still
want to do XRP transactions with your private key, you have to use
this web tool, since it's compatible with our `x2xrp.py` hex output.

Example without passphrase:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 144h 0h 0 0 | ./x2xrp.py
    xrp-hex:58fe510ffea22709defc4a2c55d1054d2d37ef46bb4a728f38d6b3fbe112850b
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 144h 0h 0 0 n | ./x2xrp.py
    rH4b7nXtPgfjmtdfVLcY7qvMUFcMwLE5HX

Example with passphrase:

    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 144h 0h 0 0 | ./x2xrp.py
    xrp-hex:dffefc577f9b97008f60592482d29d8da5a19b202b22f887d1b234df7c2edad2
    $ echo -e "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst\ndo not show my wife" | ./bip39.py | ./seed2xprv.py | ./xderive.py 44h 144h 0h 0 0 n | ./x2xrp.py
    rhbZf6hesPYXX1VgBqCXjK6jvAAbiwL4T6

Compatibility has been checked:
  - Trezor One HAS NO SUPPORT for XRP on 2021-02-08,
  - Ledger Nano S on 2021-02-08,
  - http://ripplerm.github.io/ripple-wallet/ on 2021-02-08.

# Generating the last word in the passphrase.

In bip39 the passphrase checksum should be valid. After choosing the first n-1
words randomly the last can be chosen only from a subset of words. Generate
the list like this:

    $ ./bip39-last-word/last_word.py <<< "scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress"
    Good last words:
    alcohol
    another
    ball
    brother
    cherry
    clump
    ...
    A random choice would be:
    photo

For reading words interactively in shuffled order (against keylogger):

    $ ./bip39-last-word/interactive_input.py 23 | ./bip39-last-word/last_word.py
