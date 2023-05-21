import pytest


def test_getsparkbalance(firo_cli):
    spark_balance = firo_cli.getsparkbalance()
    print(spark_balance['availableBalance'])
    print(spark_balance['unconfirmedBalance'])
    print(spark_balance['fullBalance'])


def test_getsparkbalance(firo_cli):
    firo_cli.getsparkbalance(value='asd', bad_key='invalid')


def test_getsparkbalance_invalid_value(firo_cli):
    with pytest.raises(Exception):
        firo_cli.getsparkbalance(value='invalid value')


def test_spendspark_bad_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark(value='invalid value')


def test_spendspark_no_arguments(firo_cli):
    with pytest.raises(Exception):
        firo_cli.spendspark()
