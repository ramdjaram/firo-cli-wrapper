from pytest import fixture
from rpc import *
from util import load_json_file, stringify, config


# Firo Core not started
@fixture(scope='module')
def cli():
    firo_cli = FiroCli(
        rpc_calls=config.get('FIRO', 'spark_calls'),
        firo_src_path=config.get('FIRO', 'firo_src'),
        datadir=config.get('FIRO', 'blockchain_datadir'))
    return firo_cli


# firo-cli started Firo Core
@fixture(scope='module')
def firo_cli(cli):
    cli.run_firo_core()

    # generate blocks
    BLOCKS = 3
    block_count = int(cli.getblockcount())
    if block_count < BLOCKS:
        delta = BLOCKS-block_count
        logger.warning(f'Generating {delta} additional blocks...')
        cli.generate(input=delta)

    yield cli

    cli.stop_firo_core()  # comment in case you not want to stop Firo Core after test suite


# TEST DATA
@fixture(scope='module')
def test_data():
    return load_json_file(config.get('TESTDATA', 'inputs'))


# INPUTS
@fixture(scope='module')
def input_mintspark(test_data):
    return stringify({
        "sr1qd7k458jfhtsxvguzn09gl5gvkwfalendc0rsdl9fkt6hv8akzdu3h6fhm6w2tm79s30jm0n5lamel4y4jaeq7drzmrr4pme3cawmejqy2dz8wkuu5z5hvg5dnxg9cqu9jgr0nq2s3czv": {
            'amount': test_data['amount'], 'memo': 'test_memo'
        }
    })
