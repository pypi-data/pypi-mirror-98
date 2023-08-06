from web3 import Web3
import os


class Platform:
    def __init__(self):
        self.connector = None

    def get_active_account(self, user_id):
        if self.connector is None:
            return [
                # https://etherscan.io/address/0xbe0eb53f46cd790cd13851d5eff43d12404d33e8
                os.environ.get('TELEDAPPS_ACCOUNT_ADDRESS', '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'),
                os.environ.get('TELEDAPPS_ACCOUNT_LABEL', 'Binance 7')
            ]

        self.connector.get_active_account(user_id)

    @property
    def web3(self):
        if self.connector is None:
            rpc = os.environ.get('TELEDAPPS_WEB3_RPC')

            if rpc is None:
                raise Exception('Specify Web3 RPC in TELEDAPP_WEB3_RPC!')

            return Web3(Web3.HTTPProvider(rpc))

