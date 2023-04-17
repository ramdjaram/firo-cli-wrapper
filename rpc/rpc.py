import subprocess


def create_method(call):
    def method(**kwargs):
        """A dynamically created method"""
        assert kwargs['address'] is not None, '"Address" should be provided as a key/value argument'
        assert kwargs['value'] is not None, '"Value" should be provided as a key/value argument'
        address = kwargs['address']
        value = kwargs['value']
        print(f"Executing '{call}' with address '{address}' and value '{value}'")

        # result = subprocess.run( //todo
        #     ['firo-cli', call, address, value],
        #     stdout=subprocess.PIPE
        # )
        # # Assert that the transaction was successful
        # assert 'txid' in result.stdout.decode()

        return f'txid:{call}'  # result.stdout.decode() //todo
    return method


class Rpc:

    def __init__(self, rpc_calls=None):

        if rpc_calls is None:
            raise ValueError('Rpc calls aren`t provided')

        self.methods = {}

        for call in rpc_calls:
            self.methods[call] = create_method(call)

    def __getattr__(self, attr):
        if attr in self.methods:
            return self.methods[attr]
        else:
            raise AttributeError(f"'Rpc' object has no attribute '{attr}'\nAvailable RPC calls: {list(self.methods.keys())}")
