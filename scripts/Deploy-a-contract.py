from brownie import DeployChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]
    contract = DeployChallenge.deploy({'from': deployer})
    assert contract.isComplete() == True
