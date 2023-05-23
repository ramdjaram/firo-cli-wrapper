import pytest
from util.logger import logger


def test_getsparkbalance(firo_cli):
    spark_balance = firo_cli.getsparkbalance()
    logger.info(spark_balance['availableBalance'])
    logger.info(spark_balance['unconfirmedBalance'])
    logger.info(spark_balance['fullBalance'])


def test_getsparkbalance_invalid_key(firo_cli):
    with pytest.raises(AssertionError):
        firo_cli.getsparkbalance(bad_key='invalid')


def test_getsparkbalance_valid_and_invalid_key(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(input='valid key', bad_key='invalid')


def test_getsparkbalance_invalid_value(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(input='invalid value')


def test_spendspark_bad_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark(input='invalid value')


def test_spendspark_no_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark()


@pytest.mark.spark
def test_list_spark_mints(firo_cli):
    spark_mints_list = firo_cli.listsparkmints()
    logger.info(spark_mints_list[1]['amount'])


def test_get_block_count(firo_cli):
    firo_cli.getblockcount()


@pytest.mark.spark
def test_gettransaction(firo_cli):
    firo_cli.gettransaction(input='560b2baf97441814cbdb3cbf23e643b2776a7eed67bab96d00c7fb110eb26e2a')


@pytest.mark.spark
def test_mintspark_and_generate(firo_cli, input_mintspark, test_data):
    spark_balance_initial = firo_cli.getsparkbalance()['availableBalance']

    spark_addresses = firo_cli.getallsparkaddresses()
    for p_address in spark_addresses.values():
        firo_cli.getsparkaddressbalance(input=p_address)

    block_number = firo_cli.getblockcount()

    list_of_txids = firo_cli.mintspark(input=input_mintspark)
    for txid in list_of_txids:
        firo_cli.rebroadcast_transaction(txid)

    firo_cli.generate(input=1)

    next_block_number = firo_cli.getblockcount()
    assert int(block_number) + 1 == int(next_block_number)

    spark_addresses = firo_cli.getallsparkaddresses()
    for p_address in spark_addresses.values():
        firo_cli.getsparkaddressbalance(input=p_address)

    spark_balance_after_transaction = firo_cli.getsparkbalance()['availableBalance']
    difference = spark_balance_after_transaction - spark_balance_initial
    logger.info(f'Difference: {difference}')
    assert difference == int(float(test_data['amount']) * 100000000)
