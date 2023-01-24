from brownie import CaptureTheEther, NicknameChallenge, accounts


def main():
    deployer = accounts[0]
    player = accounts[1]

    cte_contract = CaptureTheEther.deploy({'from': deployer})
    nc_contract = NicknameChallenge.deploy(
        player, cte_contract.address, {'from': deployer})

    # pyr0 is 4 bytes and 8 times pyr0 is 32 bytes
    cte_contract.setNickname(b'pyr0'*8, {'from': player})

    assert nc_contract.isComplete() == True
