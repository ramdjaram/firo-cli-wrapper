import subprocess
from util.helper import json_str_to_dict


def create_method(call, network, firo_cli_dir):
    def method(*args, **kwargs):
        """A dynamically created method"""

        invalid_arguments_message = f'Firo-cli command arguments must be key/value pair with "value" as a key. ' \
                                    f'For example: firo_cli.{call}(value=<command_argument_value>)'

        assert not args, invalid_arguments_message

        command = ['./firo-cli', network, call]

        if kwargs:
            invalid_key_arguments = [key for key in kwargs.keys() if key != 'value']
            assert 'value' in kwargs.keys(), f'Invalid command keys: {invalid_key_arguments}. {invalid_arguments_message}'
            command.append(kwargs['value'])  # append the values to command

        print(f"\nExecuting command: '{' '.join(command)}'")

        try:
            # execute the command with firo-cli
            result = subprocess.run(command, stdout=subprocess.PIPE, cwd=firo_cli_dir, check=True)

            # decode the result to string
            decoded = result.stdout.decode()
            print(f'Decoded result:\n {decoded}')

            return json_str_to_dict(decoded)
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            raise Exception(error_message)

    return method


class FiroCli:

    def __init__(self, firo_cli_path=None, rpc_calls=None, network='-regtest'):

        if firo_cli_path is None:
            raise AttributeError('Path to the ./firo-cli must be set')

        if rpc_calls is None:
            raise AttributeError('List of names for rpc calls aren`t provided')

        self._firo_cli_directory_path = firo_cli_path
        self._rpc_calls = ['getrawtransaction', 'sendrawtransaction'] + rpc_calls
        self._network = network
        self._methods = {}

        for call in self._rpc_calls:
            self._methods[call] = create_method(call, self._network, self._firo_cli_directory_path)

    def __getattr__(self, attr):
        if attr in self._methods:
            return self._methods[attr]
        else:
            raise AttributeError(
                f"'Rpc' object has no attribute '{attr}'\nAvailable RPC calls: {list(self._methods.keys())}")

    def rebroadcast_transaction(self, txid):
        raw_tx = self.getrawtransaction(txid)
        self.sendrawtransaction(raw_tx)


if __name__ == "__main__":
    # ./firod must be started
    rpc = FiroCli(['getbalance', 'listaccounts', 'mintspark'])
    spark_balance = rpc.getbalance()
    print(spark_balance.availableBalance)