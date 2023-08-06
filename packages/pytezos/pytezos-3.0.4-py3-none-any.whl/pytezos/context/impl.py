from datetime import datetime
from inspect import Parameter
from typing import Optional
from typing import Tuple

from pytezos.context.abstract import AbstractContext  # type: ignore
from pytezos.context.abstract import get_originated_address
from pytezos.crypto.encoding import base58_encode
from pytezos.crypto.key import Key
from pytezos.michelson.micheline import get_script_section
from pytezos.rpc.errors import RpcError
from pytezos.rpc.shell import ShellQuery


class ExecutionContext(AbstractContext):

    def __init__(self, amount=None, chain_id=None, source=None, sender=None, balance=None,
                 block_id=None, now=None, level=None, voting_power=None, total_voting_power=None,
                 key=None, shell=None, address=None, counter=None, script=None, tzt=False, mode=None):
        self.key: Optional[Key] = key
        self.shell: Optional[ShellQuery] = shell
        self.counter = counter
        self.mode = mode or 'readable'
        self.block_id = block_id or 'head'
        self.address = address
        self.balance = balance
        self.amount = amount
        self.now = now
        self.level = level
        self.sender = sender
        self.source = source
        self.chain_id = chain_id
        self.voting_power = voting_power
        self.total_voting_power = total_voting_power
        self.parameter_expr = get_script_section(script, name='parameter') if script and not tzt else None
        self.storage_expr = get_script_section(script,  name='storage') if script and not tzt else None
        self.code_expr = get_script_section(script, name='code') if script else None
        self.input_expr = get_script_section(script, name='input') if script and tzt else None
        self.output_expr = get_script_section(script,  name='output') if script and tzt else None
        self.sender_expr = get_script_section(script, name='sender') if script and tzt else None
        self.balance_expr = get_script_section(script, name='balance') if script and tzt else None
        self.amount_expr = get_script_section(script, name='amount') if script and tzt else None
        self.self_expr = get_script_section(script,  name='self') if script and tzt else None
        self.now_expr = get_script_section(script, name='now') if script and tzt else None
        self.source_expr = get_script_section(script, name='source') if script and tzt else None
        self.chain_id_expr = get_script_section(script, name='chain_id') if script and tzt else None
        self.origination_index = 1
        self.tmp_big_map_index = 0
        self.tmp_sapling_index = 0
        self.alloc_big_map_index = 0
        self.alloc_sapling_index = 0
        self.balance_update = 0
        self.big_maps = {}

    def reset(self):
        self.counter = None
        self.origination_index = 1
        self.tmp_big_map_index = 0
        self.tmp_sapling_index = 0
        self.alloc_big_map_index = 0
        self.alloc_sapling_index = 0
        self.balance_update = 0
        self.big_maps.clear()

    def __copy__(self):
        raise ValueError("It's not allowed to copy context")

    def __deepcopy__(self, memodict={}):
        raise ValueError("It's not allowed to copy context")

    @property
    def script(self) -> Optional[dict]:
        if self.parameter_expr and self.storage_expr and self.code_expr:
            return dict(code=[self.parameter_expr, self.storage_expr, self.code_expr])
        else:
            return None

    def set_counter(self, counter: int):
        self.counter = counter

    def get_counter(self) -> int:
        if self.counter is None:
            assert self.key, f'key is undefined'
            self.counter = int(self.shell.contracts[self.key.public_key_hash()]()['counter'])  # type: ignore
        self.counter += 1
        return self.counter

    def register_big_map(self, ptr: int, copy=False) -> int:
        if copy:
            tmp_ptr = self.get_tmp_big_map_id()
            self.big_maps[tmp_ptr] = (ptr, True)
            return tmp_ptr
        else:
            self.big_maps[ptr] = (ptr, False)
            return ptr

    def get_tmp_big_map_id(self) -> int:
        self.tmp_big_map_index += 1
        return -self.tmp_big_map_index

    def get_big_map_diff(self, ptr: int) -> Tuple[Optional[int], int, str]:
        if ptr in self.big_maps:
            src_big_map, copy = self.big_maps[ptr]
            if copy:
                dst_big_map = self.alloc_big_map_index
                self.alloc_big_map_index += 1
                return src_big_map, dst_big_map, 'copy'
            else:
                return src_big_map, src_big_map, 'update'
        else:
            big_map = self.alloc_big_map_index
            self.alloc_big_map_index += 1
            return None, big_map, 'alloc'

    def get_originated_address(self) -> str:
        res = get_originated_address(self.origination_index)
        self.origination_index += 1
        return res

    def spend_balance(self, amount: int):
        balance = self.get_balance()
        assert amount <= balance, f'cannot spend {amount} tez, {balance} tez left'
        self.balance_update -= amount

    def get_parameter_expr(self, address=None):
        if self.shell and address:
            if address == get_originated_address(0):
                return None  # dummy callback
            else:
                script = self.shell.contracts[address].script()
                return get_script_section(script, 'parameter')
        return None if address else self.parameter_expr

    def get_storage_expr(self):
        return self.storage_expr

    def get_code_expr(self):
        return self.code_expr

    def get_input_expr(self):
        return self.input_expr

    def get_output_expr(self):
        return self.output_expr

    def get_sender_expr(self):
        return self.sender_expr

    def get_balance_expr(self):
        return self.balance_expr

    def get_amount_expr(self):
        return self.amount_expr

    def get_self_expr(self):
        return self.self_expr

    def get_now_expr(self):
        return self.now_expr

    def get_source_expr(self):
        return self.source_expr

    def get_chain_id_expr(self):
        return self.chain_id_expr

    def set_storage_expr(self, expr):
        self.storage_expr = expr

    def set_parameter_expr(self, expr):
        self.parameter_expr = expr

    def set_code_expr(self, expr):
        self.code_expr = expr

    def set_input_expr(self, expr):
        self.input_expr = expr

    def set_output_expr(self, expr):
        self.output_expr = expr

    def set_source_expr(self, expr):
        self.source_expr = expr

    def set_chain_id_expr(self, expr):
        self.chain_id_expr = expr

    def get_big_map_value(self, ptr: int, key_hash: str):
        if ptr < 0:
            return None
        assert self.shell, f'shell is undefined'
        try:
            return self.shell.blocks[self.block_id].context.big_maps[ptr][key_hash]()
        except RpcError:
            return None

    def register_sapling_state(self, ptr: int):
        raise NotImplementedError

    def get_tmp_sapling_state_id(self) -> int:
        self.tmp_sapling_index += 1
        return -self.tmp_sapling_index

    def get_sapling_state_diff(self, offset_commitment=0, offset_nullifier=0) -> Tuple[int, list]:
        ptr = self.alloc_sapling_index
        self.alloc_sapling_index += 1
        return ptr, []

    def get_self_address(self) -> str:
        return self.address or get_originated_address(0)

    def get_amount(self) -> int:
        return self.amount or 0

    def get_sender(self) -> str:
        return self.sender or self.get_dummy_key_hash()

    def get_source(self) -> str:
        return self.source or self.get_dummy_key_hash()

    def get_now(self) -> int:
        if self.now is not None:
            return self.now
        elif self.shell:
            # NOTE: cached
            constants = self.shell.block.context.constants()  # type: ignore
            ts = self.shell.head.header()['timestamp']
            dt = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
            first_delay = constants['time_between_blocks'][0]
            return int((dt - datetime(1970, 1, 1)).total_seconds()) + int(first_delay)
        else:
            return 0

    def get_level(self) -> int:
        if self.level is not None:
            return self.level
        elif self.shell:
            header = self.shell.blocks[self.block_id].header()
            return int(header['level'])
        else:
            return 1

    def get_balance(self) -> int:
        if self.balance is not None:
            balance = self.balance
        elif self.shell:
            contract = self.shell.contracts[self.get_self_address()]()
            balance = int(contract['balance'])
        else:
            balance = 0
        return balance + self.balance_update

    def get_voting_power(self, address: str) -> int:
        if self.voting_power is not None:
            return self.voting_power.get(address, 0)
        elif self.shell:
            raise NotImplementedError
        else:
            return 0

    def get_total_voting_power(self) -> int:
        if self.total_voting_power is not None:
            return self.total_voting_power
        elif self.shell:
            raise NotImplementedError
        else:
            return 0

    def get_chain_id(self) -> str:
        if self.chain_id:
            return self.chain_id
        elif self.shell:
            return self.shell.chains.main.chain_id()
        else:
            return self.get_dummy_chain_id()

    def get_dummy_address(self) -> str:
        if self.key:
            return self.key.public_key_hash()
        else:
            return base58_encode(b'\x00' * 20, b'KT1').decode()

    def get_dummy_public_key(self) -> str:
        if self.key:
            return self.key.public_key()
        else:
            return base58_encode(b'\x00' * 32, b'edpk').decode()

    def get_dummy_key_hash(self) -> str:
        if self.key:
            return self.key.public_key_hash()
        else:
            return base58_encode(b'\x00' * 20, b'tz1').decode()

    def get_dummy_signature(self) -> str:
        return base58_encode(b'\x00' * 64, b'sig').decode()

    def get_dummy_chain_id(self) -> str:
        return base58_encode(b'\x00' * 4, b'Net').decode()

    def get_dummy_lambda(self):
        return {'prim': 'FAILWITH'}

    def set_total_voting_power(self, total_voting_power: int):
        self.total_voting_power = total_voting_power

    def set_voting_power(self, address: str, voting_power: int):
        self.voting_power[address] = voting_power
