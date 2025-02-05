class Block:
    block_id: int
    name: str
    in_groups: list[str]
    join: bool

    def __init__(self,
                 block_id: int = -1,
                 name: str = None,
                 in_groups: list[str] = None,
                 join: bool = False
                 ) -> None:
        self.block_id = block_id
        assert (block_id >= 0), f"block_id ({block_id}) must be greater than or 0"
        self.name = name
        self.in_groups = in_groups if in_groups is not None else ['public']  # List of groups the participant belongs to
        self.join = join

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
        return self.join

    def is_prepared(self
                    ) -> bool:
        return True
