import pytest
from time import sleep
from util.helper import stringify


def test_getsparkbalance(firo_cli):
    spark_balance = firo_cli.getsparkbalance()
    print(spark_balance['availableBalance'])
    print(spark_balance['unconfirmedBalance'])
    print(spark_balance['fullBalance'])


def test_getsparkbalance_invalid_key(firo_cli):
    with pytest.raises(AssertionError):
        firo_cli.getsparkbalance(bad_key='invalid')


def test_getsparkbalance_valid_and_invalid_key(firo_cli):
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
    print(spark_mints_list[1]['amount'])


def test_get_block_count(firo_cli):
    firo_cli.getblockcount()


@pytest.mark.spark
def test_gettransaction(firo_cli):
    firo_cli.gettransaction(input='560b2baf97441814cbdb3cbf23e643b2776a7eed67bab96d00c7fb110eb26e2a')


@pytest.mark.spark
def test_mintspark_and_generate(firo_cli):

    amount = "0.0000123"

    spark_balance_initial = firo_cli.getsparkbalance()['availableBalance']

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(input=value)

    firo_cli.getblockcount()

    mint_trasaction = {
        'sr1rjrgek8hka2x2nhuhlw2ptxatryv0mfmp6qy9yehhnlrnzhdpjewg5tdvtwq7upycx78tf9xp09jchgwzzrrmne5k626qrp30kkrt5aluzns2l3cmh7dajlymtrzxf4wujl8tyc9yuqrz': {
            'amount': amount, 'memo': 'test_memo'
        }
    }
    txids_list = firo_cli.mintspark(input=stringify(mint_trasaction))
    for txid in txids_list:
        firo_cli.rebroadcast_transaction(txid)

    firo_cli.generate(input=1)

    firo_cli.getblockcount()

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(input=value)

    spark_balance_after_transaction = firo_cli.getsparkbalance()['availableBalance']
    difference = spark_balance_after_transaction - spark_balance_initial
    print('Difference: ', difference)
    assert difference == int(float(amount) * 100000000)
