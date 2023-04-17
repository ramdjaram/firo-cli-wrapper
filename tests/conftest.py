from pytest import fixture

from rpc import *


@fixture(scope='module')
def rpc_calls():
    return [
        'listsparkminds',
        'mintspark',
        'spentspark',
    ]


@fixture(scope='module')
def rpc(rpc_calls):
    return Rpc(rpc_calls)
