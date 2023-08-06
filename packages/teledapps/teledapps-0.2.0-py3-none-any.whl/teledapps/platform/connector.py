from web3 import Web3
import os


class SimpleConnector:
    def __init__(self):
        self.active_account = [
            os.environ.get('TELEDAPPS_ACCOUNT_ADDRESS', '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'),
            os.environ.get('TELEDAPPS_ACCOUNT_LABEL', 'Test account')
        ]

    def get_active_account(self, user_id):
        return self.active_account

    @property
    def web3(self):
        rpc = os.environ.get('TELEDAPPS_WEB3_RPC')

        if rpc is None:
            raise Exception('For local run, specify Web3 RPC in TELEDAPPS_WEB3_RPC')

        return Web3(Web3.HTTPProvider(rpc))
