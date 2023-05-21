import pytest


def test_getsparkbalance(rpc):
    spark_balance = rpc.getsparkbalance()
    print(spark_balance['availableBalance'])
    print(spark_balance['unconfirmedBalance'])
    print(spark_balance['fullBalance'])


def test_getsparkbalance_invalid_value(rpc):
    with pytest.raises(Exception):
        rpc.getsparkbalance(value='invalid value')


def test_spendspark_bad_arguments(rpc):
    with pytest.raises(Exception):
        rpc.spendspark(value='invalid value')


def test_spendspark_no_arguments(rpc):
    with pytest.raises(Exception):
        rpc.spendspark()
