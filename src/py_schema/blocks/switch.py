import typing

from message import Message
from block import Block


class Switch(Block):
    """
    A switch is a block that must be given a callable function that takes.
     The result_id_map must be able to turn the func's output into a block_id.
     The switch will return on execute all the block_ids mapped from the func's results on the ledger
    """
    block_id: int
    name: str
    in_groups: list[str]
    join: bool
    func: callable(list[Message])
    static: bool
    result_id_map: {typing.Any: int}

    def __init__(self,
                 func: callable,
                 result_id_map: {typing.Any: int},
                 block_id: int = -1,
                 name: str = None,
                 in_groups: list[str] = None,
                 join: bool = False,
                 static: bool = False
                 ) -> None:

        super().__init__(block_id, name, in_groups, join)
        self.static = static
        self.func = func
        self.result_id_map = result_id_map

    def execute(self,
                ledger: list[Message],
                **kwargs
                ) -> list[int]:
        kwargs['ledger'] = ledger
        results = self.func(**kwargs)
        return [self.result_id_map[result] for result in results]

    def get_possible_flow(self
                          ):
        return self.result_id_map.values()

    def is_switch(self
                  ) -> bool:
        return True
