from pytest import fixture
from rpc import *

firo_cli_directory_path = '/Users/milanranisavljevic/Workspace/arcadia/firo_spark/src'


@fixture(scope='module')
def rpc_calls():
    return [
        'listunspentsparkmints',
        'listsparkmints',
        'listsparkspends',
        'getsparkdefaultaddress',
        'getallsparkaddresses',
        'getnewsparkaddress',
        'getsparkbalance',
        'getsparkaddressbalance',
        'resetsparkmints',
        'setsparkmintstatus',
        'resetsparkmints',
        'mintspark',
        'spendspark',
        'lelantustospark',
    ]


@fixture(scope='module')
def firo_cli(rpc_calls):
    return FiroCli(firo_cli_directory_path, rpc_calls)
