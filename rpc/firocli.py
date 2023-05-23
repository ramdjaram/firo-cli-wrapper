import json
import subprocess
from time import sleep
from util.logger import logger
from util.helper import is_valid_dict_string, print_command_title, is_process_running

FIROD_PROCESS_NAME = 'firod'


def create_method(call, network, firo_src_dir, datadir=''):
    def method(*args, **kwargs):
        """A dynamically created method"""

        assert is_process_running(FIROD_PROCESS_NAME), 'Firo Core should be running. Start Firo Core(firod) process `firo_cli.run_firo_core()`'

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

        print_command_title(call, command, "@")

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
            logger.error(error_message)
            raise Exception(error_message)

    return method


class FiroCli:

    DEFAULT_RPC_CALLS = [
        'getrawtransaction',
        'sendrawtransaction',
        'getblockcount',
        'generate',
        'gettransaction',
    ]

    def __init__(self, rpc_calls=None, network='-regtest', firo_src_path=None, datadir=''):

        if firo_src_path is None:
            raise AttributeError('Path to the ./firo-cli must be set')

        if rpc_calls is None:
            raise AttributeError('List of names for rpc calls aren`t provided')

        self._rpc_calls = set(self.DEFAULT_RPC_CALLS + [item.strip() for item in rpc_calls.split(',')])
        self._network = network
        self._firo_src = firo_src_path
        self._datadir = f'-datadir={datadir}' if datadir else ''
        self._methods = {}

        for call in self._rpc_calls:
            self._methods[call] = create_method(call, self._network, self._firo_src, self._datadir)

        self.info()

    def run_firo_core(self, wait=5):
        command = [f'./{FIROD_PROCESS_NAME}', self._network]
        if self._datadir:
            command.append(self._datadir)
        try:
            firod = is_process_running(FIROD_PROCESS_NAME)
            if firod:
                logger.warning('Firo Core is already running.')
                return firod
            else:
                logger.warning('Firo Core is not running. Starting Firo Core...')
                counter = 0

                # start Firo Core as a separate process
                firod = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=self._firo_src)

                # Wait for the Firo Core process to start running
                firod_finished = None
                while firod_finished is None and counter is not wait:
                    logger.info(f'Polling Firo Core - attempt: {counter + 1}')
                    firod_finished = firod.poll()
                    if firod_finished is not None:
                        error = 'Firo Core stopped for unknown reason!'
                        logger.error(error)
                        raise Exception(error)
                    sleep(1)  # Adjust the sleep duration as needed
                    counter += 1
                logger.info('Firo Core is running.')
                return firod
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            logger.error(error_message)
            raise Exception(error_message)

    def stop_firo_core(self):
        logger.warning('Stopping Firo Core...')
        firod = is_process_running(FIROD_PROCESS_NAME)
        if firod:
            logger.warning('Terminating Firo Core process...')
            firod.terminate()
            firod.wait()
            logger.info('Firo Core process terminated successfully!')
            return
        logger.warning('Firo Core is not running. Noting to stop!')

    def info(self):
        print_command_title(
            'FIRO-CLI TESTING TOOL',
            ['[firo-cli]', '<network>', '<datadir>', '<rpc_call>', '<input>'],
            '%'
        )
        logger.info(f'Firo src directory path: {self._firo_src}')
        logger.info(f'Network used for testing: {self._network}')
        logger.info(f'List of supported rpc calls: {self._rpc_calls}\n')

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
