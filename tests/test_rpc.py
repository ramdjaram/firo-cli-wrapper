def test_rpc_fixure(rpc):
    a = rpc.listsparkmindss(address='Gandijeva', value='130b')

    print('ARGUMENTI', a)

    rpc.spentspark(value='130b')
    rpc.mintsparki('mintspark', mint='mint')


def test_rpc_connection(rpc_connection):
    info = rpc_connection.getinfo()
    print(info)
