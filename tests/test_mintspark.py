import pytest
from util.logger import logger

txid = ''


@pytest.mark.wip
@pytest.mark.spark
def test_mintspark_to_private_that_global_balance_increased_by_sent_amount(firo_cli, input_mintspark, test_data):

    # get initial transparent balance
    initial_balance = float(firo_cli.getbalance())
    # get initial private balance
    initial_spark_balance = firo_cli.getsparkbalance()['availableBalance']

    # get block count number
    block_number = firo_cli.getblockcount()

    # mintspark private transaction
    # send spark to private addres
    list_of_txids = firo_cli.mintspark(input=input_mintspark)
    global txid
    txid = list_of_txids[0]

    # re-broadcast transactions
    for txid in list_of_txids:
        firo_cli.rebroadcast_transaction(txid)

    # generate 1 block
    firo_cli.generate(input=1)

    # assert that block count is incremented by 1
    next_block_number = firo_cli.getblockcount()
    assert int(block_number) + 1 == int(next_block_number)

    # get current transparent balance
    # assert that balance increased after mintspark
    current_balance = float(firo_cli.getbalance())
    delta_utxo = current_balance - initial_balance
    logger.warning(f'UTXO balance delta: {delta_utxo}')
    assert round(delta_utxo, 4) == 42.9999

    # get current private balance
    # assert that balance increased by the ammount sent in mintspark transaction
    current_spark_balance = firo_cli.getsparkbalance()['availableBalance']
    delta_spark = current_spark_balance - initial_spark_balance
    logger.warning(f'Spark balance delta: {delta_spark}')
    assert delta_spark == int(float(test_data['amount']) * 100000000)


@pytest.mark.wip
@pytest.mark.spark
def test_gettransaction(firo_cli):
    firo_cli.gettransaction(input=f'{txid}')
