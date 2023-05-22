import json
import subprocess
from util.logger import logger
from util.helper import is_valid_dict_string, print_command_title


def create_method(call, network, firo_src_dir, datadir=''):
    def method(*args, **kwargs):
        """A dynamically created method"""

        invalid_arguments_message = f'Firo-cli command arguments must be key/value pair with "input" as a key. ' \
                                    f'For example: firo_cli.{call}(input=<command_argument_value>)'

        assert not args, invalid_arguments_message

        if not datadir:
            command = ['./firo-cli', network, call]
        else:
            command = ['./firo-cli', network, datadir, call]

        if kwargs:
            invalid_key_arguments = [key for key in kwargs.keys() if key != 'input']
            assert 'input' in kwargs.keys(), f'Invalid command keys: {invalid_key_arguments}. {invalid_arguments_message}'
            command.append(str(kwargs['input']))  # append the arg value to command and parse the arg to string

        print_command_title(call, command, "|")

        try:
            # execute the command with firo-cli
            result = subprocess.run(command, stdout=subprocess.PIPE, cwd=firo_src_dir, check=True)

            # decode the result to string
            decoded = result.stdout.decode('utf-8')
            logger.debug(f'Result:\n{decoded}')

            if is_valid_dict_string(decoded):  # parse if json string
                return json.loads(decoded)
            return decoded.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            raise Exception(error_message)

    return method


class FiroCli:

    def __init__(self, rpc_calls=None, network='-regtest', firo_src_path=None, datadir=''):

        if firo_src_path is None:
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

        self._rpc_calls = set(self._default_rpc_calls + [item.strip() for item in rpc_calls.split(',')])
        self._network = network
        self._firo_src = firo_src_path
        self._datadir = f'-datadir={datadir}' if datadir else ''
        self._methods = {}

        for call in self._rpc_calls:
            self._methods[call] = create_method(call, self._network, self._firo_src, self._datadir)

        self.info()

    def run_firod(self, datadir=''):
        command = ['./firod', self._network, datadir]
        logger.warning(self._firo_src)
        subprocess.run(command, stdout=subprocess.PIPE, cwd=self._firo_src, check=True)

    def info(self):
        print_command_title('Firo-Cli Testing Tool', ['[firo-cli]', '<network>', '<rpc_call>', '<input>'], '%')
        logger.info(f'[firo/src] directory path: {self._firo_src}')
        logger.info(f'[network] used for testing: {self._network}')
        logger.info(f'[list of supported rpc calls]: {self._rpc_calls}')

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
    import os

    logger.info(os.getcwd())
    logger.info(os.path.expanduser('-'))
    logger.info(os.environ)
    user_profile = os.environ['HOME']
    logger.info("USERPROFILE: ", user_profile)
    # ./firod must be started
    rpc = FiroCli(['getbalance', 'listaccounts', 'mintspark'], firo_src_path=os.getcwd())
    spark_balance = rpc.getbalance()
    logger.info(spark_balance.availableBalance)
