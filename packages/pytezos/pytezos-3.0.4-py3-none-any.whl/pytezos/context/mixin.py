from os.path import exists
from os.path import expanduser
from typing import Optional
from typing import Union

from pytezos.context.impl import ExecutionContext  # type: ignore
from pytezos.crypto.encoding import is_pkh
from pytezos.crypto.encoding import is_public_key
from pytezos.crypto.key import Key
from pytezos.crypto.key import is_installed
from pytezos.jupyter import InlineDocstring
from pytezos.rpc import RpcMultiNode
from pytezos.rpc import RpcNode
from pytezos.rpc import ShellQuery
from pytezos.rpc.errors import RpcError

default_network = 'edo2net'
default_key = 'edsk33N474hxzA4sKeWVM6iuGNGDpX2mGwHNxEA4UbWS8sW3Ta3NKH'  # please, use responsibly
default_key_hash = 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa'
alice_key = 'edsk3QoqBuvdamxouPhin7swCvkQNgq4jP5KZPbwWNnwdZpSpJiEbq'  # for flextesa sandbox
alice_key_hash = 'tz1VSUr8wwNhLAzempoch5d6hLRiTh8Cjcjb'

nodes = {
    'mainnet': ['https://mainnet-tezos.giganode.io/',
                'https://rpc.tzkt.io/mainnet/',
                'https://api.tez.ie/',
                'https://tezos-prod.cryptonomic-infra.tech/chains/main/blocks/head'],
    'sandboxnet': ['http://127.0.0.1:8732/'],
    'delphinet': ['https://rpc.tzkt.io/delphinet/'],
    'edonet': ['https://rpc.tzkt.io/edonet/'],
    'edo2net': ['https://rpc.tzkt.io/edo2net/']
}
keys = {
    'alice': alice_key
}


class KeyHash(Key):

    def __init__(self, public_key_hash):
        super(KeyHash, self).__init__(0)
        self._pkh = public_key_hash

    def __repr__(self):
        res = [
            super(Key, self).__repr__(),
            f'\nPublic key hash',
            self.public_key_hash()
        ]
        return '\n'.join(res)

    def public_key_hash(self):
        return self._pkh

    def public_key(self):
        raise NotImplementedError("Use private key instead of a public key hash")

    def secret_key(self, passphrase=None, ed25519_seed=True):
        raise NotImplementedError("Use private key instead of a public key hash")

    def sign(self, message, generic=False):
        raise NotImplementedError("Use private key instead of a public key hash")

    def verify(self, signature, message):
        raise NotImplementedError("Use private key instead of a public key hash")


class ContextMixin(metaclass=InlineDocstring):
    """ Mixin for blockchain interaction, stores node connection and key object.
    """

    def __init__(self, context: Optional[ExecutionContext] = None):
        super(ContextMixin, self).__init__()
        if context is None:
            context = ExecutionContext(
                shell=ShellQuery(RpcNode(nodes[default_network][0])),
                key=Key.from_encoded_key(default_key) if is_installed() else KeyHash(default_key_hash))
        self.context = context

    @property
    def shell(self) -> ShellQuery:
        assert self.context.shell, f'network is undefined'
        return self.context.shell

    @property
    def key(self) -> Key:
        assert self.context.key, f'key is undefined'
        return self.context.key

    @property
    def address(self) -> Optional[str]:
        return self.context.address

    @property
    def block_id(self) -> Union[str, int]:
        return self.context.block_id

    def __repr__(self):
        res = [
            super(ContextMixin, self).__repr__(),
            '\nProperties'
        ]
        if self.context.key is not None:
            res.append(f'.key  # {self.key.public_key_hash()}')
        if self.context.shell is not None:
            res.append(f'.shell  # {self.shell.node.uri}')
        if self.context.address is not None:
            res.append(f'.address  # {self.address}')
        if self.context.block_id is not None:
            res.append(f'.block_id  # {self.block_id}')
        return '\n'.join(res)

    def _spawn_context(self,
                       shell: Optional[Union[ShellQuery, str]] = None,
                       key: Optional[Union[Key, str]] = None,
                       address: Optional[str] = None,
                       block_id: Optional[Union[str, int]] = None,
                       mode: Optional[str] = None) -> ExecutionContext:
        if isinstance(shell, str):
            if shell.endswith('.pool'):
                shell = shell.split('.')[0]
                assert shell in nodes, f'unknown network {shell}'
                shell = ShellQuery(RpcMultiNode(nodes[shell]))
            elif shell in nodes:
                shell = ShellQuery(RpcNode(nodes[shell][0]))
            else:
                shell = ShellQuery(RpcNode(shell))
        else:
            assert shell is None or isinstance(shell, ShellQuery), f'unexpected shell {shell}'

        if isinstance(key, str):
            if key in keys:
                key = Key.from_encoded_key(keys[key])
            elif is_public_key(key):
                key = Key.from_encoded_key(key)
            elif is_pkh(key):
                key = KeyHash(key)
            elif exists(expanduser(key)):
                key = Key.from_faucet(key)
            else:
                key = Key.from_alias(key)
        else:
            assert key is None or isinstance(key, Key), f'unexpected key {key}'

        if isinstance(address, str):
            try:
                script = self.shell.contracts[address].script()
            except RpcError as e:
                raise RpcError(f'Contract {address} not found', *e.args)
        else:
            script = self.context.script

        return ExecutionContext(
            shell=shell or self.context.shell,
            key=key or self.context.key,
            address=address,
            block_id=block_id,
            script=script,
            mode=mode or self.context.mode)
