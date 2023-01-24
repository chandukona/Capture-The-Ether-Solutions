from brownie import FuzzyIdentityChallenge, Fi_Exploit, accounts, ZERO_ADDRESS
from eth_utils import keccak, to_checksum_address
from rlp import encode


def get(addr, i):
    return 'badc0de' in to_checksum_address(keccak(encode([bytes.fromhex(addr[2:]), i]))[12:]).lower()


def find():
    hsh = get(accounts[0].address, i)
    while not hsh:
        i = 0
        while i < 1000000:
            hsh = get(accounts[0].address, i)
            i += 1
            if i % 100 == 0:
                print(i)
        accounts.remove(accounts[0])
        accounts.add()
    print(accounts[0])


def main():
    deployer = accounts[0]
    # find() got Private_key: '0xa376e6c4be605caa488ff90fd81c72a93b7917af0ec8da1c8b46c930246856f5' and address: '0x6C37d4bb51dc59D11aDfA5aA454422944060cfcD' at "i: 6"
    accounts.add(
        private_key='0xa376e6c4be605caa488ff90fd81c72a93b7917af0ec8da1c8b46c930246856f5')
    player = accounts[-1]

    for _ in range(6):
        player.transfer(to=ZERO_ADDRESS, amount=0)
    assert player.nonce == 6

    contract = FuzzyIdentityChallenge.deploy({'from': deployer})
    iName = Fi_Exploit.deploy(contract.address, {'from': player})
    iName.exploit()

    assert contract.isComplete() == True
