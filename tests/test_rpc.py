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
def test_mintspark_and_generate(firo_cli):

    amount = "0.0001"

    spark_balance_initial = firo_cli.getsparkbalance()['availableBalance']

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(value=value)

    firo_cli.getblockcount()

    mint_tx_argument = {
        'sr1rjrgek8hka2x2nhuhlw2ptxatryv0mfmp6qy9yehhnlrnzhdpjewg5tdvtwq7upycx78tf9xp09jchgwzzrrmne5k626qrp30kkrt5aluzns2l3cmh7dajlymtrzxf4wujl8tyc9yuqrz': {
            'amount': amount, 'memo': 'test_memo'
        }
    }
    txids_list = firo_cli.mintspark(value=stringify(mint_tx_argument))
    # txids_list = ['a6b844cea33ae4800c9557b3f80d888568ad0358c6c5f5b299f270ce8ba24463']

    for txid in txids_list:
        firo_cli.rebroadcast_transaction(txid)
    # firo_cli.sendrawtransaction(value='01000000013cb26312667b5e3bc873f3cbd44f30090977630fe8bc44ccb374ed5c69a0253c010000006a47304402202e49ced926eb7b0ff5bd7b872cdf24b416d6d3e9c1bf3095bfc2521f3a549cd2022071cc1c1b1461bca50f2611394e4deb487762a4dd89702ccb7790a90d67ab402501210309a7a76bc96d4caae50b3ef408f556caf0acd2f1e76487db72f74295e2f932acfeffffff0240771b0000000000fd3701d1004011d31e24518be4968d9c717eca3dab677b736f56ac3f3e5e2af3966ba98e1901007c459008f04a0ed24de28782a54d280ae811f181ee8a04d57baed81cb3ff7c290100611e7c185148b7c370f5244c4fe7550b8f292826e5a0fc6a19a1b15402837c810100527285d507ef40a008e689bda800145a76483310f8391c40ce38416500c72a4c422c8ca2d53e72b49fb0c10250e53d8147486f38b1bbb0f89b93c4fefccb6d64bb41a9a71e8b5e0bbbfb7f9406b614a8b58c9f107d30b6984de2aba8c8f2646be4682459208a93f7420211b9a10b4138c0f82c8c2918d667469d47107602383a1c506120a940771b0000000000a9cdfda7941a5a0a01df3ad8f86274656b592eb2b52460f05635a7b01432047701007cb0e1a5de5946cf8ff5b48e7cda68a3648bc912beb3778607b55c354428ad4542e830ee000000001976a9149ef01e4c5f5043f3c320cb0d17cb56f73f8b3f7f88ac15040000')

    firo_cli.generate(value=1)

    firo_cli.getblockcount()

    spark_addresses = firo_cli.getallsparkaddresses()
    for value in spark_addresses.values():
        firo_cli.getsparkaddressbalance(value=value)

    spark_balance_after_transaction = firo_cli.getsparkbalance()['availableBalance']
    difference = spark_balance_after_transaction - spark_balance_initial
    print('Difference: ', difference)
    assert difference == int(float(amount) * 100000000)
