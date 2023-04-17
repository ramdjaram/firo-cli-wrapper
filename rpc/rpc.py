import inspect


class Rpc:

    def __init__(self, rpc_calls=None):

        if rpc_calls is None:
            raise ValueError('Rpc calls aren`t provided')

        for call in rpc_calls:
            def method(self, *args, **kwargs):
                """A dynamically created method"""
                print(f'args={args} kwargs={kwargs}')
                return args, kwargs

            setattr(Rpc, call, method)

    def __getattr__(self, attr):
        class_instance = self.__class__.__name__
        available_rpc_calls = [key for key, value in inspect.getmembers(Rpc) if not key.startswith('__')]
        raise AttributeError(f'<{class_instance}> class has no attribute "{attr}".\nAvailable RPC calls:\n{available_rpc_calls}')

