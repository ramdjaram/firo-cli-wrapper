import json
import subprocess
from time import sleep
from util.config_loader import config
from util.logger import logger
from util.helper import is_valid_dict_string, print_command_title, is_process_running, dir_exists

FIROD_PROCESS_NAME = 'firod'
FIRO_CLI_EXE = 'firo-cli'


class FiroCli:

    def __init__(self, rpc_calls=None, firo_src_path=None, *args, **kwargs):

        if rpc_calls is None:
            raise AttributeError('List of names for rpc calls aren`t provided')

        if firo_src_path is None:
            raise AttributeError('Path to the ./firo-cli must be set')

        self._options = []
        self._methods = {}
        self._rpc_calls = set([item.strip() for item in rpc_calls.split(',')])
        self._firo_src = firo_src_path
        self._datadir = None

        try:
            self._datadir = kwargs['datadir']
        except KeyError as e:
            logger.warning('-datadir isn`t set. Using default.')

        if args:
            for value in args:
                self._options.append(f'-{value}')

        if kwargs:
            for key, value in kwargs.items():
                self._options.append(f'-{key}={value}')

        for call in self._rpc_calls:
            self._methods[call] = self._create_method(call)

        self._info()

    def __getattr__(self, attr):
        if attr in self._methods:
            return self._methods[attr]
        else:
            raise AttributeError(
                f"No such command as '{attr}' in 'FiroCli'\nAvailable RPC calls: {list(self._methods.keys())}")

    def _info(self):
        logger.info('======= FIRO TESTING TOOL =======\n')
        logger.info(f'Firo src directory path: {self._firo_src}')
        logger.info(f'List of supported rpc calls: {self._rpc_calls}')
        logger.info(f'Command options: {self._options}\n')

    def _generate_command(self, exe, options):
        command = [f'./{exe}'] + options
        return command

    def _firo_cli(self, command):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, cwd=self._firo_src, check=True)
            # decode the result to string
            decoded = result.stdout.decode('utf-8')
            logger.debug(f'Result:\n{decoded}')
            # parse if json string
            if is_valid_dict_string(decoded):
                return json.loads(decoded)
            return decoded.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            logger.error(error_message)
            raise Exception(error_message)

    def _create_method(self, call):
        def method(command_argument=None):
            """A dynamically created method"""

            assert is_process_running(
                FIROD_PROCESS_NAME), 'Firo Core should be running. Start Firo Core(firod) process `firo_cli.run_firo_core()`'

            logger.debug(f'Adding {call}() method to firo-cli')
            method_options = self._options + [f'{call}'] # add call to command options

            if command_argument:
                # append the arg value to command and parse the arg to string
                method_options.append(str(command_argument))

            print_command_title(call, method_options, "@")
            command = self._generate_command(FIRO_CLI_EXE, method_options)
            self._firo_cli(command)

        return method

    def run_firo_core(self, wait=5):

        blockchain_check = True
        if self._datadir:
            if not dir_exists(f'{self._datadir}/regtest'):
                logger.warning('Firo Core is starting without existing datadir for blockchain. '
                               'Need some time to generate it!')
                blockchain_check = False
        try:
            firod = is_process_running(FIROD_PROCESS_NAME)
            if firod:
                logger.warning('Firo Core is already running.')
                return firod
            else:
                logger.warning('Firo Core is not running. Starting Firo Core...')
                print_command_title(FIROD_PROCESS_NAME, self._options, '%')
                # start Firo Core as a separate process
                command = self._generate_command(FIROD_PROCESS_NAME, self._options)
                firod = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=self._firo_src)
                # Wait for the Firo Core process to start running
                counter = 0
                firod_finished = None
                while firod_finished is None and counter is not wait:
                    logger.debug(f'Polling Firo Core - attempt: {counter + 1}')
                    firod_finished = firod.poll()
                    if firod_finished is not None:
                        error = 'Firo Core stopped due to error!'
                        logger.error(error)
                        raise Exception(error)
                    sleep(1)  # Adjust the sleep duration as needed
                    counter += 1
                logger.info('Firo Core is running.')
                if not blockchain_check:
                    sleep(wait + 80)
                return firod
        except subprocess.CalledProcessError as e:
            error_message = f"Command failed with return code {e.returncode}: {e.output.decode()}"
            logger.error(error_message)
            raise Exception(error_message)

    def stop_firo_core(self):
        logger.warning('Stopping Firo Core...')
        firod = is_process_running(FIROD_PROCESS_NAME)
        if firod:
            pid = str(firod.pid)
            logger.warning(f'Terminating Firo Core process...')
            logger.debug(f'Firod process PID: {pid}')
            firod.terminate()
            firod.wait()
            logger.info('Firo Core process terminated successfully!')
            return
        logger.warning('Firo Core is not running. Noting to stop!')

    def rebroadcast_transaction(self, txid):
        raw_tx = self.getrawtransaction(input=txid.strip())
        self.sendrawtransaction(input=raw_tx.strip())


if __name__ == "__main__":
    firo_cli = FiroCli(
        config.get('FIRO', 'spark_calls'),
        config.get('FIRO', 'firo_src'),
        'regtest',
        datadir=config.get('FIRO', 'blockchain_datadir'))
    firo_cli.run_firo_core()
    count = firo_cli.getblockcount()
    logger.error(count)
    logger.error(count-1)
    firo_cli.getsparkdefaultaddress()
    firo_cli.getbalance()
    firo_cli.getsparkaddressbalance('sr17k6c6e576vhj3rvtmdq8lg3uze8s9zj98j2e6zuzj7dlcfslxha7ghh2sdpj8chvm3mhe5ap5nwl4cwcmra29wqtyskp7luhqxxe0xek4s6ct8hz8ytug9p3mamw5yed9083n8q886k6x')
    firo_cli.stop_firo_core()
