from brownie import network, Box, ProxyAdmin, TranparentUpgradeableProxy, Contract, BoxV2
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer = encode_function_data()
    proxy = TranparentUpgradeableProxy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer,
        {"from": account, "gas_limit": 1000000}
    )
    print(f"Proxy deployed to {proxy} you can now upgrade to v2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin_contract=proxy_admin)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("Box", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
