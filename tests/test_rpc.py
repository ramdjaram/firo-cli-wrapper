def test_rpc_fixure(rpc):
    a = rpc.listsparkminds(address='Gandijeva', value='130b')
    print('ARGUMENTI', a)

    a = rpc.spentspark(address='Gandijeva', value='130b')
    print('ARGUMENTI', a)

    a = rpc.mintsparki(address='Gandijeva', value='130b')
    print('ARGUMENTI', a)


def test_rpc_connection(rpc_connection):
    info = rpc_connection.getinfo()
    print(info)
