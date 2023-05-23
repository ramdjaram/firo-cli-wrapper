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
    firo_core = cli.run_firod(wait=5)
    yield cli
    logger.warning('Terminating Firo Core process...')
    firo_core.terminate()
    firo_core.wait()
    logger.info('Firo Core process terminated successfully!')


# TEST DATA
@fixture(scope='module')
def test_data():
    return load_json_file(config.get('TESTDATA', 'inputs'))


# INPUTS
@fixture(scope='module')
def input_mintspark(test_data):
    return stringify({
        test_data['p_address']: {
            'amount': test_data['amount'], 'memo': 'test_memo'
        }
    })
