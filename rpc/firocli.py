import json
import subprocess
from util.helper import is_valid_dict_string, print_command_title, stringify


def create_method(call, network, firo_cli_dir):
    def method(*args, **kwargs):
        """A dynamically created method"""

        invalid_arguments_message = f'Firo-cli command arguments must be key/value pair with "input" as a key. ' \
                                    f'For example: firo_cli.{call}(input=<command_argument_value>)'

        assert not args, invalid_arguments_message

        command = ['./firo-cli', network, call]

        if kwargs:
            invalid_key_arguments = [key for key in kwargs.keys() if key != 'input']
            assert 'input' in kwargs.keys(), f'Invalid command keys: {invalid_key_arguments}. {invalid_arguments_message}'
            command.append(str(kwargs['input']))  # append the arg value to command and parse the arg to string

        print_command_title(call, command, "|")

        try:
            # execute the command with firo-cli
            result = subprocess.run(command, stdout=subprocess.PIPE, cwd=firo_cli_dir, check=True)

            # decode the result to string
            decoded = result.stdout.decode('utf-8')
            print(f'Result:\n{decoded}')

            if is_valid_dict_string(decoded):  # parse if json string
                return json.loads(decoded)
            return decoded.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            raise Exception(error_message)

    return method


class FiroCli:

    def __init__(self, rpc_calls=None, network='-regtest', firo_cli_path=None):

        if firo_cli_path is None:
            raise AttributeError('Path to the ./firo-cli must be set')

        if rpc_calls is None:
            raise AttributeError('List of names for rpc calls aren`t provided')

        self._default_rpc_calls = [
            'getrawtransaction',
            'sendrawtransaction',
            'getblockcount',
            'generate',
            'gettransaction',
        ]
        self._rpc_calls = self._default_rpc_calls + rpc_calls
        self._network = network
        self._firo_cli_directory_path = firo_cli_path
        self._methods = {}

        for call in self._rpc_calls:
            self._methods[call] = create_method(call, self._network, self._firo_cli_directory_path)

        print_command_title('Firo-Cli Testing Tool', ['[firo-cli]', '<network>', '<rpc_call>', '<input>'], '%')
        print(f'[firo-cli] directory path:\t\t\t{firo_cli_path}')
        print(f'[network] used for testing:\t\t\t{network}')
        print(f'[list of integrated rpc calls]:\t\t{self._default_rpc_calls}')
        print(f'[list of rpc calls under test]:\t\t{rpc_calls}\n\n')

    def __getattr__(self, attr):
        if attr in self._methods:
            return self._methods[attr]
        else:
            raise AttributeError(
                f"No such command as '{attr}' in 'FiroCli'\nAvailable RPC calls: {list(self._methods.keys())}")

    def rebroadcast_transaction(self, txid):
        raw_tx = self.getrawtransaction(input=txid.strip())
        self.sendrawtransaction(input=raw_tx.strip())


if __name__ == "__main__":
    # ./firod must be started
    rpc = FiroCli(['getbalance', 'listaccounts', 'mintspark'])
    spark_balance = rpc.getbalance()
    print(spark_balance.availableBalance)
