from brownie import PublicKeyChallenge, accounts
from rlp import encode, decode
from ethereum.transactions import Transaction
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from sympy import sqrt_mod
from gmpy2 import invert
from eth_utils import keccak, to_checksum_address


def recover_publicKey(raw_tx, address):
    tx = decode(bytes.fromhex(raw_tx[2:]), Transaction)
    # print(tx.to_dict())
    # '''
    #      {'nonce': 0,
    #       'gasprice': 1000000000,
    #       'startgas': 90000,
    #       'to': '0x6b477781b0e68031109f21887e6b5afeaaeb002b',
    #       'value': 0,
    #       'data': '0x5468616e6b732c206d616e21',
    #       'v': 41,                                                                              # for some reason here chain id should is not 3
    #       'r': 74776771311019569939017621593480679160618399812524181808306514788568607828695,
    #       's': 39381076589634547203973423246354256320472887426210737547826636053693505964386,
    #       'sender': '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
    #       'hash': '0xabc467bedd1d17462fcc7942d0af7874d6f8bdefee2b299c9168a216d3ff0edb'}
    # '''
    new_tx = Transaction(tx.nonce, tx.gasprice, tx.startgas,
                         tx.to, tx.value, tx.data, 3)
    r, s, a, b, p, q, G = tx.r, tx.s, secp256k1.a, secp256k1.b, secp256k1.p, secp256k1.q, secp256k1.G
    data = Transaction.serialize(new_tx)
    z = int(keccak(encode(data)).hex(), 16) % p
    y = sqrt_mod((r**3 + a*r + b) % p, p, all_roots=True)
    R = Point(r, y[0], secp256k1)
    R_ = Point(r, y[1], secp256k1)
    ri = int(invert(r, q))
    #                                                                    s = k^-1 * ( h + r*d ) -> s*R = ( h + r*d )*k^-1*k*G = ( h+ r*d )*G
    #                                                                     -> (h*G + r*d*G)  -> s*R - zG = (h*G + r*d*G - h*G ) = r*d*G -> (s*R - zG)*ri = r*d*G*(r^-1) -> -> d*G
    k = ri * (s*R - z*G)
    k_ = ri * (s*R_ - z*G)
    addr = keccak(bytes.fromhex(hex(k.x)[2:]+hex(k.y)[2:]))[-20:].hex()
    addr_ = keccak(bytes.fromhex(hex(k_.x)[2:]+hex(k_.y)[2:]))[-20:].hex()
    assert address in [addr, addr_], f'address not found!!'

    # found publickey
    publicKey = [k if addr == address else k_][0]

    return publicKey


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = PublicKeyChallenge.deploy({'from': deployer})

    # ropsten is depreciated, so i got this from other writeups online.
    raw_tx = '0xf87080843b9aca0083015f90946b477781b0e68031109f21887e6b5afeaaeb002b808c5468616e6b732c206d616e2129a0a5522718c0f95dde27f0827f55de836342ceda594d20458523dd71a539d52ad7a05710e64311d481764b5ae8ca691b05d14054782c7d489f3511a7abf2f5078962'

    publickey = recover_publicKey(
        raw_tx, '92b28647ae1f3264661f72fb2eb9625a89d88a31')
    # after finding the publickey

    contract.authenticate(
        hex(publicKey.x)+hex(publicKey.y)[2:], {'from': player})

    assert contract.isComplete() == True
