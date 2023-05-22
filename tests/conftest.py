from rpc import *
from pytest import fixture
from util import load_json_file, stringify, config


RPC_CALLS = [
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
    'lelantustospark'
]


# FIRO-CLI
@fixture(scope='module')
def firo_cli():
    return FiroCli(rpc_calls=RPC_CALLS, firo_cli_path=config['FIRO']['cli_path'])


# TEST DATA
@fixture(scope='module')
def test_data():
    return load_json_file(r'/Users/milanranisavljevic/Workspace/firo-cli/data/data.json')


# INPUTS
@fixture(scope='module')
def input_mintspark(test_data):
    return stringify({
        test_data['p_address']: {
            'amount': test_data['amount'], 'memo': 'test_memo'
        }
    })


# DONO WHAT FOR, MAYBE USEFUll
@fixture(scope='module')
def spark_addresses():
    return {
        "0": "sr1dssfjfu0cy2xj3yjxyxvlfcur493f6ar5d2k46qqst453h6uavcqt9l57607we5uu7zd3wy7vkss7h59rgn4txp5wn0kt5x3y3w2xy2fzjhstlvze4tjugx9lrfp6ffrv8r4w3q7m2pcf",
        "1": "sr1jdq5f3kfdut63dwtqslpn9wq8g0hwuecvcl4j8dulu8tl4ant6kcvmlc0a6yas0gxdwdnjr9cuwggjgzqr3vyzrefvfn9fx46kx22s9stl9rs0gcdw4ee5j54u3q2zw9q8ynf0g4uyntz",
        "2": "sr1cxpx6a0q27uaglj5cyam6wtla7axw8wv3apd0y6nw490rnr7vnfmvd64d74p3hffh9877ypwpp2frvnejzrwhlp3n2cwhdkauny0vacjcasgum2v47k7dd2sv0wrtqyeaehnrlqd92q98",
        "3": "sr1rjrgek8hka2x2nhuhlw2ptxatryv0mfmp6qy9yehhnlrnzhdpjewg5tdvtwq7upycx78tf9xp09jchgwzzrrmne5k626qrp30kkrt5aluzns2l3cmh7dajlymtrzxf4wujl8tyc9yuqrz",
        "4": "sr19mn38zh79zupkeatgqmanethp4zda8e7w6hal7cyvczxyrruutdym7x6z5xj0evuajcvc0p496zatj8rfg38hg2u4wvvcgm2hd4h4y8qmc4s4stw849r3jh4v3ca6ac22jn5lcca5kxty"
    }
