from util.helper import to_dict


def test_getsparkbalance(rpc):
    spark_balance = rpc.getsparkbalance()
    print(to_dict(spark_balance)['availableBalance'])
