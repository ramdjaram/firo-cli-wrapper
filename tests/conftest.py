from bitcoinrpc.authproxy import AuthServiceProxy
from pytest import fixture

from rpc import *


@fixture(scope='module')
def rpc_calls():
    return [
        'getsparkbalance',
        'listsparkmints',
        'mintspark',
        'spentspark',
    ]


@fixture(scope='module')
def rpc(rpc_calls):
    return Rpc(rpc_calls)


@fixture(scope='module')
def rpc_connection():
    rpc_user = "your_rpc_user"
    rpc_password = "your_rpc_password"
    rpc_host = "127.0.0.1"
    rpc_port = 8395

    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")
    return rpc_connection.getinfo()

