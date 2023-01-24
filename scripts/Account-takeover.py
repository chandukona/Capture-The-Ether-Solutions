from brownie import AccountTakeoverChallenge, accounts
from rlp import encode
from ethereum.transactions import Transaction
from fastecdsa.curve import secp256k1
from eth_utils import keccak
from gmpy2 import invert


def calculate_hsh(tx):
    new_tx = Transaction(tx['nonce'], tx['gasPrice'], tx['gasLimit'],
                         tx['to'], tx['value'], tx['data'], tx['v'])
    data = Transaction.serialize(new_tx)
    z = int(keccak(encode(data)).hex(), 16)
    return z


def main():
    deployer = accounts[0]

    contract = AccountTakeoverChallenge.deploy({'from': deployer})

    # ropsten is depreciated, so i got this from other writeups online.
    reconstructed_tx_1 = {
        'nonce': 0x00,
        'gasPrice': 0x3b9aca00,
        'gasLimit': 0x5208,
        'to': '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
        'value': 0x1111d67bb1bb0000,
        'data': b'',
        'v': 0x03
    }
    reconstructed_tx_2 = {
        'nonce': 0x01,
        'gasPrice': 0x3b9aca00,
        'gasLimit': 0x5208,
        'to': '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
        'value': 0x1922e95bca330e00,
        'data': b'',
        'v': 0x03
    }

    # message hash values
    z1 = calculate_hsh(reconstructed_tx_1)
    z2 = calculate_hsh(reconstructed_tx_2)

    # r and s values from the writeups
    r = 0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166
    s1 = 0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8
    s2 = 0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de
    p = secp256k1.q

    def inv(x, p): return int(invert(x, p))

    k = ((z1 - z2) * inv(s1 - s2, p)) % p
    d = ((k*s1 - z1) * inv(r, p)) % p
    assert ((k*s2 - z2) * inv(r, p)) % p == d

    player = accounts.add(private_key=d)
    assert player.address == '0x6B477781b0e68031109f21887e6B5afEAaEB002b', player.address
    contract.authenticate({'from': player})

    assert contract.isComplete() == True
