import pytest
from util.logger import logger


@pytest.mark.wip
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


@pytest.mark.spark
def test_gettransaction(firo_cli):
    firo_cli.gettransaction(input='28aee2443dafeb1e584d334e2964d26252872063e66ac3d012894514478060f7')
