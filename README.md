# crypto-key-derivation
Document all the mess around bip32+bip39+bip44 and similar key generation schemes

# Overview
Our overall goal is to generate bitcoin/litecon/ethereum/etc
private+public keys from a list of english words.

BIP39: Given a list of words, generate a seed (512 bit),
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

BIP32: Given a seed (any 128-512 bit will do), generate a master key
which can be used to generate further subkeys.

BIP44: Just a bunch of recommendations on how to use BIP39+BIP32
together.  This is followed by some wallets (e.g. Trezor), while not
followed by others (e.g. Electrum).

# Setup

    virtualenv -p python3 venv
    venv/bin/pip install https://github.com/spesmilo/electrum/archive/3c281c4056f94476a1352b89d284bfd0559206fd.tar.gz#sha256=2bae55c6452a6e3d6eff64fefa262906aad0472939990a2e97469309c5afc133
    venv/bin/pip install ipython pysha3

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

    $ ./mnemonic.py <<EOF
        scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
        TREZOR
        EOF
    7d8b4005aa5e21e438057535a8a37944f5b110f3df91743bca22ffdcd2690fd1d83611d7740719199fa3e6093a756b2bf6a4e1975da733a114325733b056d86a
    $ ./mnemonic.py <<EOF
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
without having the ability to spend them.

The standard notation of a path in the tree is like this:
"m/44'/0'/0'/1/3".  Here we generating the root from a seed and then
taking the path of: harden 44 -> harden 0 -> harden 0 -> non-harden 1
-> non-harden 3.  Note the apostrophes, when they are present, that's
a hardened derivation in the path.  According to BIP44, this is the
4th change address of the first account in a wallet.

We provide the following utilities to walk the tree.

`seed2xprv.py`: stdin is a hex encoded seed from the BIP39 chapter,
stdout is an xprv, containing the root of the tree.  This path is
usually called "m" or "m/".

`xprv2xpub.py`: stdin is an xprv, output is an xpub.

`xprv2xprv.py`: stdin is an xprv, first arg is a number, output is the derived xprv

`xprv2xprv-hardened.py`: stdin is an xprv, first arg is a number, output is the derived xprv

`xpub2xpub.py`: stdin is an xpub, first arg is a number, output is the derived xpub

`xprv2btc.py`: stdin is an xprv, output is a BTC secret key.

`xpub2btc.py`: stdin is an xpub, output is a BTC address, note that
this address must match the private key generated with
`xprv2btc.py`.  You can use https://www.bitaddress.org/ to check this.

`xprv2eth.py`: stdin is an xprv, output is an ETH secret key.

`xpub2eth.py`: stdin is an xpub, output is an ETH address.  Easiest
way to check if this is working correctly is to login into the secret
key with myetherwallet and check the public key on the screen.

Examples:

    $ ./seed2xprv.py << EOF
      000102030405060708090a0b0c0d0e0f
      EOF
    xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
    $ ./xprv2xpub.py << EOF
      xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
      EOF
    xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8
    $ ./xprv2xprv.py 0 << EOF
      xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U
      EOF
    xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt
    $ ./xprv2xprv.py 0 | ./xprv2xpub.py << EOF
      xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U
      EOF
    xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH
    $ ./xprv2xprv-hardened.py 2147483647 << EOF
      xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt
      EOF
    xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9
    $ ./xpub2xpub.py 1 <<EOF
      xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a
      EOF
    xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon
    $ ./xprv2btc.py <<EOF
      xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP
      EOF
    L15hj1TsQC1eCnMwd4CkZTGh8iusyHjDtz2oNL968oPz9dXGEeP4
    $ ./xprv2xpub.py <<EOF | ./xpub2btc.py
      xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP
      EOF
    19C8rUkmD1QG13qrpqypo3pEGuVMfEd8q5

You can also get segwit addresses or P2SH compatible segwit addresses:

    $ ./xprv2xpub.py <<EOF | ./xpub2btc.py p2wpkh
      xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP
      EOF
    bc1qt8wzxfq4p2ufpumd6w02p7kdr5c7uaqeekmeje
    $ ./xprv2xpub.py <<EOF | ./xpub2btc.py p2wpkh-p2sh
      xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP
      EOF
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

    $ ./mnemonic.py  <<EOF   | ./seed2xprv.py | ./xprv2xprv.py 0 | ./xprv2xpub.py | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2btc.py ; done ; }
      aerobic melody aerobic join crunch quiz ring icon brisk speak someone marine
      EOF
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

    $ ./mnemonic.py <<EOF | ./seed2xprv.py | ./xprv2xprv.py 1 | ./xprv2xpub.py | { read xpub ; for i in `seq 0 4` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2btc.py ; done ; }
      aerobic melody aerobic join crunch quiz ring icon brisk speak someone marine
      EOF
    1MTWgVQQLEj8YMckR2p6CuXyc3AviAHkY5
    17TBRJy4NG6sqmfMYnKJ2bb7w7prb2mDAx
    1BTY3J6dqst3zYjQtpty3HGxomUAQ4D2Vv
    1GfzFS1hyeMfch3nFc3ghosYK2MJrcnuJ5
    1JfLH3gU9iTeb19w2P6MbdxPyXePozepNz

Compatiblity with Electrum 2.9.3 has been verified on 2017-10-19.

# A full example for BTC+Trezor

Given the following trezor seed: nation grab van ride cloth wash
endless gorilla speed core dry shop raise later wedding sweet minimum
rifle market inside have ill true analyst

You can generate the first 20 addresses of the first legacy account
like this:

    $ ./bip39.py <<EOF | ./seed2xprv.py | ./xprv2xprv-hardened.py 44 | ./xprv2xprv-hardened.py 0 | ./xprv2xprv-hardened.py 0 | ./xprv2xpub.py | ./xpub2xpub.py 0 | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2btc.py ; done ; }
      nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst
      EOF
    1GhzX8gLBfG96Qg1mk9S5ckhVPsxeeBiSC
    18sRn1xohBhxHH9XZHgFBmZmuH5cUWpWwz
    1JTmDmWGHhKzQz6eqVVFUcTtLu8cbHpPME
    1G4V5azXZVwBvUpJTTXF3p8xMNbXW4eK1K
    1DKfZirvSHm3BbUn4r2CJjiDCCDWdVHocu
    1PcaRLpZj1xwtHfjsTrgRGPBisj4GBCJJR
    1PgjbqNsqkQ37z7rfV4NXqRJV8wH6szaCX
    18ZVzPh3sZBYWwZnHdtCiy8nCJCE4BgqjP
    14HKC5JoJ8t5AKXfbsYQ8hRdprLG3PhTd7
    1N62dYLNHEaLAAm26YKaupK3acU1rSbtKd
    1MkYKrzgAVow18HEGyMVihHsmNNbhE6hFV
    17d6it2WbUBkQsnFkUQNFhyKLuQDp641kZ
    17RcQRVcAa67e2JWQALAsFjhdHifz4pYLQ
    1736NfiMMqqfMtY8Eum1kNYmPJ3kTK7PiS
    1CPWJTzSGQfuAtH4o6jjzFYtnSJLsyHAdo
    1BeRvCBQ2rgo9nAS69sHEoS1tAb8SDPYNW
    1D62bwfz4uXc5Rie67P3hZNagCiGb3Lt71
    19goZ8KEimPKGYEUUSwPrzvQowjCjXyjGA
    1C1GtktpKJu5RyGV9ZqeViheZ3XLrv26gM
    15vm9koqBZAiW3QKk5QisP6n4N5dAHLucc

Or if you have a secret legacy wallet with the passphrase of "do not
show my wife", then you can get the addresses like this:

    $ ./bip39.py <<EOF | ./seed2xprv.py | ./xprv2xprv-hardened.py 44 | ./xprv2xprv-hardened.py 0 | ./xprv2xprv-hardened.py 0 | ./xprv2xpub.py | ./xpub2xpub.py 0 | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2btc.py ; done ; }
      nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst
      do not show my wife
      EOF
    1Hvv8XyMtT8QGAXLTRE1bgEYbpfj7bZmN9
    1JiWHCAHmzsfJcag78339H1UNbkgb7cyTz
    1DjbR8ZizFBoBViZDk5iXbaEU8YtqAuWNw
    1ALXTBp5dV7nEZebmig4ETvobfYPamieWB
    13dNfFZ5ReWA3nos7GnxPRA3HZ5XUv1ZxN
    1L3LGJ7Vas4Vb4WSsgMaAdiF2LQCXNE1Vn
    1L4rJFerp3bG76ympeSsdRGPcJrvCiXcik
    1CvXMexun4G5GpnUeFKffQaSAeSQrksYPo
    1LonnqZgT3gaZEEoTq5u1CsdzSKWTBxKWA
    1NeALQJ98tBcGSdBshifDAWhVkznB3W2XC
    1EHghkLLt4YbMTkvDwJKEcf6uZX3SfYg5y
    1K8swNeXUt5kyMspz1fF26MCsHF569MwfZ
    17HfqZVNN1pvaM2YcBDxqPSut6xLdEUNDm
    1N768NSuJxBDtGFs86NR6SzPPceNHe7q3p
    1EhakrsvU1Z6RaG14SAbAG8vmpGCmEGyuY
    1LkGpNR21fJC2qinYuNamGenfuKdA1up1p
    1BS22xsWta5zmDEDuFvmKqNe3BMAj7fxto
    1NUTAByxXJSKudHtPr6XWGCNKGXefBUxoA
    1FoMfD416QkwimA2agKjVnc57Z8y1LAdyt
    12uWNV2cYAALUtbLPDU93QjQ9z6JKLsTXL

Or if you want to have your non-legacy, shiny new, segwit ready
addresses for this secret wallet:

    $ ./bip39.py <<EOF | ./seed2xprv.py | ./xprv2xprv-hardened.py 49 | ./xprv2xprv-hardened.py 0 | ./xprv2xprv-hardened.py 0 | ./xprv2xpub.py | ./xpub2xpub.py 0 | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2btc.py p2wpkh-p2sh ; done ; }
      nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst
      do not show my wife
      EOF
    3FdXjsy32tZdrma6WvApUvFwFv8oNhPnp1
    3AuVfCnp19R8Eoa5CZXeGJjU1TQDy6fW58
    3A8QJCZbBpKYTgySAdDeQRHZPtAdSgnPkS
    3J1X3Xnjux8mgs5tuwdsxJ65LxmT7Uta4Q
    3DtZm9HJvMg2k2RPEd2BoRDEDjjei9a4Ku
    3FH4zbzQhaXuseUUTJwkQt5qRqok3gC5ep
    3PqBo2oAHAQGFdZTFvZRy3MoAA79KmTWmN
    3Dh3UtAi8ApA8xEiRox8mFyk6geMwjmCXq
    3M4gnJJPnLSuzCGQZpDtHCMr9j5RamMZfg
    3HxrUwxViuEb3NvBJbvYWAx6UYPyEKSsqY
    3M388FKxwkFkkuG8Mu56jUK9pbJxYWRhVS
    3HsYbGsGd4qdfrkniojR6hwxLY2wobZZbh
    3EM6skqkgKWTFcpeFHevFtGtFtno85FAw2
    3EQu4kFKSNu71nZq8U3f2VLaifFnEsbq8P
    3Eui7EsJfV4t2LhYEByjZ6n87PsMSWFsAQ
    3QvZxt7j2BRvLz5gJGPKHbrtr3U3pKk6x1
    3GxauUPhXZjZ3gaQzoU5trbRChBKXJroFE
    32cLMpV9K5RsK4PADbULKoZjmjjSvRVBCQ
    3DbyfNg5GrfqT6r9BXxykrRFGZQ5mhcUnR
    39muZPwWd219cxVDB7gkwmxKJWDozKN8nZ

All 4 modes have been checked for compatility with a real Trezor on 2017-10-19:

  - legacy + no passphrase,
  - legacy + passphrase,
  - segwit + no passphrase,
  - segwit + passphrase,

# A full example of Trezor+ETH/ETC

First 20 private keys for Ethereum:

    $ ./bip39.py <<EOF | ./seed2xprv.py | ./xprv2xprv-hardened.py 44 | ./xprv2xprv-hardened.py 60 | ./xprv2xprv-hardened.py 0 | ./xprv2xprv.py 0 | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xprv2xprv.py $i | ./xprv2eth.py ; done ; }
      nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst
      EOF
    bb36972e4db24cffd1dba3342c4c801c3344fe429500bdba192e2f49673f9139
    6a72d0345f06270cabe20f8f218f25073108586bc81c985eaa02a27533949a35
    7d728996e76f8399684a03438da6d8d65b2ab0c7a6be6681197fe8e9c7935698
    6a6a07b1567bbe6125e2a8e158af9cbd1ca30c2507589e1af5116d7dadd243f2
    5f643792ca3237e69821d3e0584c83961a33e7157361468edd21b97024baed94
    9ae16f6777a7ab6f851ddae747eb423a1f2df6eed86c35528cf068f73f3c15f5
    98454487c4e677a635268e243000b6cb9f7c11b0012d7b74de827ecae2d82b6e
    053141f20f7d3d7ea45ceb6a2931bdc66ead3c2e82b129a30bbc6ef6fb148893
    feba0bd2b97d6d13564088aa09d6d2a494fc349da2d024e1d59bd00e7dd2e460
    3fb3951c760d743a7f893126bbbba5e3308f1f0a00cfb54cde18ad439da13a0c
    42b4e1280fecbe697d064a628ba8391a3180d01ebf0f2896f371b2fa8310a483
    15c7bcab93503ad3d35eb40da0f914addc6a235f6f26b31787b61d443b0d6692
    ef7280b7351eb909ff68085daa39e154973cdc6b79f1d0305e39b667b4c0ca0f
    7618f8f095920f23454f2f5ab3d48acf1a58b62009ec4820e2e92c38249ed4b3
    69a433c4fc0a3e2b492750e5b564d82ecdac93b55e10337689a0f2a38c36adc4
    a2bed6e156f703eaf891a89078f036d6f4435b3406610e79fe2cc27227821625
    a5b0f46af6470089851cb1db4714beda035178ae01674ac10c3d6af6907bc82c
    1cc6c86a15473042546db43dfd6ea89b272e7bfff5b87d9bd1cf3dc86fab7af1
    dbbb9ec5995da3b1e604fdc32d22016a7ca170898e245b1fd2fb3a930d82ed53
    0856114b9db8859f8e47e8b014b88d795579033b2388d90f27ad7ba38139f10b

First 20 public keys for Ethereum Classic:

    $ ./bip39.py <<EOF | ./seed2xprv.py | ./xprv2xprv-hardened.py 44 | ./xprv2xprv-hardened.py 61 | ./xprv2xprv-hardened.py 0 | ./xprv2xpub.py | ./xpub2xpub.py 0 | { read xpub ; for i in `seq 0 19` ; do echo $xpub | ./xpub2xpub.py $i | ./xpub2eth.py ; done ; }
      nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst
      EOF
    0x919903583020fb1dc543284bcd75d4737bad415a
    0x3e605cd53a01cbe4604f4c750855874cc90d6116
    0x43936814ee89fe166df960a451324e077b4cf79c
    0x56ec92fd4bb2ee4e0893d637fa79d5596290ca18
    0xb081d3f32abd01426d9e710126332a4b7467194c
    0x7dd72f776e88d5e59f13973209b25afd54e0bb58
    0xb8641b1584d9c4b7195c1d20c4d55bff8f7a7f6d
    0x1e405ce231bbc16745f6508a7e9751cc4e22c89d
    0x5324857446f039402a88fd935aa0c20d5556dd3a
    0x74df8755d0ebaa1966f0b5dee0806ab6a95aaa51
    0xf963971c69d0b8f07b2556729d6e3dcd92c07012
    0xe9cb9c70d63cb3270bf3e924472e2baa530c1a4e
    0x7c1a2b5e88f616263881224fb79cc5a23b3a8179
    0x16da04dd8efe266c6b8c3aec348c2e6e629659b9
    0x52253f77bfd91473f254ea9e333618156a685318
    0x4eee19e660202047fab5c7d3adcd7fba728eb6f9
    0x5f7096db5f20fdcd70075cec4b6ef09bf77603cd
    0xf8392ca25f0bf666a4c9ce112eb5c32b166c74fb
    0x6c62e296f28bd5eda8ec93d98d595f4cb305e6de
    0x902162f7899076d1572796dac29cf117086bfe1e

Compatibility with trezor has been checked both for ETH and ETC.

# Generating the last word in the passphrase.

In bip39 the passphrase checksum should be valid. After choosing the first n-1
words randomly the last can be chosen only from a subset of words. Generate
the list like this:

    $ ./bip39-last-word/last_word.py <<EOF
      scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress
      EOF
    Good last words:
    alcohol
    another
    ball
    brother
    cherry
    clump
    ...

For reading words interactively in shuffled order (against keylogger):

    $ ./bip39-last-word/interactive_input.py 23 | ./bip39-last-word/last_word.py
