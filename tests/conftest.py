from pytest import fixture
from rpc import *
from util import load_json_file, stringify, config


# FIRO-CLI
@fixture(scope='module')
def firo_cli():
    cli = FiroCli(
        rpc_calls=config.get('FIRO', 'spark_calls'),
        firo_src_path=config.get('FIRO', 'cli_path'),
        datadir=config.get('FIRO', 'blockchain_datadir'))
    cli.run_firo_core(wait=5)
    yield cli
    cli.stop_firo_core()


# TEST DATA
@fixture(scope='module')
def test_data():
    return load_json_file(config.get('TESTDATA', 'inputs'))


# INPUTS
@fixture(scope='module')
def input_mintspark(test_data):
    return stringify({
        "sr1rjrgek8hka2x2nhuhlw2ptxatryv0mfmp6qy9yehhnlrnzhdpjewg5tdvtwq7upycx78tf9xp09jchgwzzrrmne5k626qrp30kkrt5aluzns2l3cmh7dajlymtrzxf4wujl8tyc9yuqrz": {
            'amount': test_data['amount'], 'memo': 'test_memo'
        }
    })
