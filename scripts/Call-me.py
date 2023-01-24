from brownie import CallMeChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = CallMeChallenge.deploy({'from': deployer})
    contract.callme({'from': player})

    assert contract.isComplete() == True
