from util.helper import json_str_to_dict


def test_getsparkbalance(rpc):
    spark_balance = rpc.getsparkbalance()
    print(json_str_to_dict(spark_balance)['availableBalance'])
    print(json_str_to_dict(spark_balance)['unconfirmedBalance'])
    print(json_str_to_dict(spark_balance)['fullBalance'])
