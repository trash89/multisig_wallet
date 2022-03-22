from brownie import convert, accounts,  MultiSigWallet, TestContract
from web3 import Web3
import eth_abi


def main():
    deploy_contracts()
    print_values()
    fund_contract()
    print_values()
    tx = create_and_confirm_tx(567)
    execute_tx(tx, accounts[1])
    print_values()


def params_msw():
    owners = [accounts[0].address, accounts[1].address, accounts[2].address]
    numConfirm = len(owners)-1
    return owners, numConfirm


def get_msw():
    return MultiSigWallet[-1]


def get_t():
    return TestContract[-1]


def deploy_contracts():
    owners, numConfirm = params_msw()

    print("Deploying MultiSigWallet contract...")
    msw = MultiSigWallet.deploy(owners, numConfirm, {"from": accounts[0]})
    print(f"MultiSigWallet contract deployed at {msw}")

    print("Deploying TestContract contract...")
    t = TestContract.deploy({"from": accounts[0]})
    print(f"TestContract deployed at {t}")
    return msw, t


def fund_contract():
    msw = get_msw()
    print("Funding MultiSigWallet with 1 ether from a[0]...")
    accounts[0].transfer(msw.address, "1 ether")
    print("Funded")


def create_and_confirm_tx(tr_value):
    msw = get_msw()
    t = get_t()

    print("Create a transaction from a[0]...")
    tr_1_ether = Web3.toWei(1, "ether")

    func_signature = Web3.keccak(text="callMe(uint256,uint256)")[:4].hex()
    var1 = tr_value
    var2 = 10000
    params_encoded = eth_abi.encode_abi(
        ["uint256", "uint256"], [var1, var2]).hex()
    calldata_encoded = func_signature+params_encoded
    print(calldata_encoded)
    solidity_encoded = t.getData(var1, var2)
    print(solidity_encoded)
    assert solidity_encoded == calldata_encoded

    # in the case we want to test the encoding of string
    # func_signature = Web3.keccak(text="callMeString(string)")[:4].hex()
    # var1 = "test"
    # params_encoded = eth_abi.encode_abi(["string"], [var1]).hex()
    # calldata_encoded = func_signature+params_encoded
    # print(calldata_encoded)
    # solidity_encoded = t.getDataString(var1)
    # print(solidity_encoded)
    # assert solidity_encoded == calldata_encoded

    tx = msw.submitTransaction(
        t.address, tr_1_ether, calldata_encoded, {"from": accounts[0]})
    tx.wait(1)
    owners, numConfirm = params_msw()
    for i in range(0, numConfirm):
        print(f"Confirming transaction {tx.txid} from {owners[i]}...")
        tx_confirm = msw.confirmTransaction(0, {"from": owners[i]})
        tx_confirm.wait(1)
        print(f"Confirmed transaction {tx.txid}")
    return msw.getTransactionCount()-1


def execute_tx(tx_index, from_account):
    msw = get_msw()
    print(f"Executing transaction {tx_index} from a[1]...")
    tx = msw.executeTransaction(tx_index, {"from": from_account})
    tx.wait(1)
    print("Executed!")


def print_values():
    msw = get_msw()
    t = get_t()
    print(f"Now, TestContract.i is {t.i()}")
    print(f"Now, TestContract.balance is {t.balance()}")
    print(f"Now, MultiSigWallet.balance is {msw.balance()}")
    print(f"Now, accounts[0].balance is {accounts[0].balance()}")
