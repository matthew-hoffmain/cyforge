class Block:
    block_id: float
    name: any
    in_groups: list[any]
    join: bool

    def __init__(self,
                 block_id: float = -1,
                 name: any = None,
                 in_groups: list[any] = None,
                 join: bool = False
                 ) -> None:
        assert (block_id >= 0), f"block_id ({block_id}) must be greater than or 0"
        self.block_id = block_id
        self.name = name
        self.in_groups = in_groups if in_groups is not None else ['public']  # List of groups the participant belongs to
        assert isinstance(self.in_groups, list)
        self.join = join
        assert isinstance(self.join, bool)

    def is_responder(self
                     ) -> bool:
        return False

    def is_switch(self
                  ) -> bool:
        return False

    def is_schema(self
                  ) -> bool:
        return False

    def is_join(self
                ) -> bool:
        return self.join is True

    def is_prepared(self
                    ) -> bool:
        return True
