import subprocess
from util.helper import json_str_to_dict

directory = '/Users/milanranisavljevic/Workspace/arcadia/firo_spark/src'
network = '-regtest'


def create_method(call):
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
            result = subprocess.run(command, stdout=subprocess.PIPE, cwd=directory, check=True)

            # decode the result to string
            decoded = result.stdout.decode()
            print(f'Decoded result:\n {decoded}')

            return json_str_to_dict(decoded)
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            raise Exception(error_message)

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
            raise AttributeError(
                f"'Rpc' object has no attribute '{attr}'\nAvailable RPC calls: {list(self.methods.keys())}")


if __name__ == "__main__":
    # ./firod must be started
    rpc = Rpc(['getbalance', 'listaccounts', 'mintspark'])
    spark_balance = rpc.getbalance()
    print(spark_balance.availableBalance)
