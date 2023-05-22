from pytest import fixture
from rpc import *

firo_cli_directory_path = '/Users/milanranisavljevic/Workspace/arcadia/firo_spark/src'


@fixture(scope='module')
def rpc_calls():
    return [
        'listunspentsparkmints',
        'listsparkmints',
        'listsparkspends',
        'getsparkdefaultaddress',
        'getallsparkaddresses',
        'getnewsparkaddress',
        'getsparkbalance',
        'getsparkaddressbalance',
        'resetsparkmints',
        'setsparkmintstatus',
        'resetsparkmints',
        'mintspark',
        'spendspark',
        'lelantustospark'
    ]


@fixture(scope='module')
def firo_cli(rpc_calls):
    return FiroCli(firo_cli_directory_path, rpc_calls)


@fixture(scope='module')
def spark_addresses():
    return [
        "sr1dssfjfu0cy2xj3yjxyxvlfcur493f6ar5d2k46qqst453h6uavcqt9l57607we5uu7zd3wy7vkss7h59rgn4txp5wn0kt5x3y3w2xy2fzjhstlvze4tjugx9lrfp6ffrv8r4w3q7m2pcf",
        "sr1jdq5f3kfdut63dwtqslpn9wq8g0hwuecvcl4j8dulu8tl4ant6kcvmlc0a6yas0gxdwdnjr9cuwggjgzqr3vyzrefvfn9fx46kx22s9stl9rs0gcdw4ee5j54u3q2zw9q8ynf0g4uyntz",
        "sr1cxpx6a0q27uaglj5cyam6wtla7axw8wv3apd0y6nw490rnr7vnfmvd64d74p3hffh9877ypwpp2frvnejzrwhlp3n2cwhdkauny0vacjcasgum2v47k7dd2sv0wrtqyeaehnrlqd92q98",
        "sr1rjrgek8hka2x2nhuhlw2ptxatryv0mfmp6qy9yehhnlrnzhdpjewg5tdvtwq7upycx78tf9xp09jchgwzzrrmne5k626qrp30kkrt5aluzns2l3cmh7dajlymtrzxf4wujl8tyc9yuqrz",
        "sr19mn38zh79zupkeatgqmanethp4zda8e7w6hal7cyvczxyrruutdym7x6z5xj0evuajcvc0p496zatj8rfg38hg2u4wvvcgm2hd4h4y8qmc4s4stw849r3jh4v3ca6ac22jn5lcca5kxty"
    ]
