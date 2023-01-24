from brownie import GuessTheNumberChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = GuessTheNumberChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})

    contract.guess(42, {'from': player, 'value': '1 ether'})

    assert contract.isComplete() == True
