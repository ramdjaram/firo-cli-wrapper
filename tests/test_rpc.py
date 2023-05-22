import json
import pytest
from time import sleep


def test_getsparkbalance(firo_cli):
    spark_balance = firo_cli.getsparkbalance()
    print(spark_balance['availableBalance'])
    print(spark_balance['unconfirmedBalance'])
    print(spark_balance['fullBalance'])


def test_getsparkbalance_invalid_key(firo_cli):
    with pytest.raises(AssertionError):
        firo_cli.getsparkbalance(bad_key='invalid')


def test_getsparkbalance_valid_and_invalid_key(firo_cli):
    firo_cli.getsparkbalance(value='valid key', bad_key='invalid')


def test_getsparkbalance_invalid_value(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(value='invalid value')


def test_spendspark_bad_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark(value='invalid value')


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
    firo_cli.gettransaction(value='560b2baf97441814cbdb3cbf23e643b2776a7eed67bab96d00c7fb110eb26e2a')


@pytest.mark.spark
def test_get_spark_balance(firo_cli):

    amount = "0.014"

    spark_balance_initial = firo_cli.getsparkbalance()['availableBalance']

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(value=value)

    firo_cli.getblockcount()

    mint_dict = {
        'sr1jdq5f3kfdut63dwtqslpn9wq8g0hwuecvcl4j8dulu8tl4ant6kcvmlc0a6yas0gxdwdnjr9cuwggjgzqr3vyzrefvfn9fx46kx22s9stl9rs0gcdw4ee5j54u3q2zw9q8ynf0g4uyntz': {
            'amount': amount, 'memo': 'test_memo'
        }
    }
    # txids_list = firo_cli.mintspark(value=json.dumps(mint_dict))
    #
    # for txid in txids_list:
    #     firo_cli.rebroadcast_transaction(txid)

    firo_cli.generate(value=1)

    firo_cli.getblockcount()

    spark_balance_after_transaction = firo_cli.getsparkbalance()['availableBalance']
    difference = spark_balance_after_transaction - spark_balance_initial
    print('DIFFERENCE: ', difference)
    assert difference == float(amount) * 100000000

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(value=value)
