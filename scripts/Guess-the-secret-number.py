from brownie import GuessTheSecretNumberChallenge, accounts, web3


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = GuessTheSecretNumberChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})

    for i in range(256):
        if web3.eth.get_storage_at(contract.address, 0) == web3.soliditySha3(abi_types=['uint8'], values=[i]):
            contract.guess(i, {'from': player, 'value': '1 ether'})
            print(f'[ ] got the Guess: {i} !!')
            break

    assert contract.isComplete() == True
