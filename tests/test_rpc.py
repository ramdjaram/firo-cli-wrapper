import subprocess


def test_rpc_fixure(rpc):
    a, k = rpc.listsparkminds('listsparkminds')
    print('ARGUMENTI', a)

    rpc.spentspark('spentspark')
    rpc.mintsparki('mintspark', mint='mint')


def test_send_firo():
    # Use firo-cli to send 1 Firo to a test address
    result = subprocess.run(['firo-cli', 'sendtoaddress', 'test_address', '1'], stdout=subprocess.PIPE)

    # Assert that the transaction was successful
    assert 'txid' in result.stdout.decode()


def test_rpc_connection(rpc_connection):
    info = rpc_connection.getinfo()
    print(info)
