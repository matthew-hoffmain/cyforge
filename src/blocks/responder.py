from datetime import datetime
from message import Message
from block import Block
from blocks.responders.responseGenerator import ResponseGenerator


class Responder(Block):
    block_id: int
    name: str
    in_groups: list[str]
    join: bool
    responder_type: str
    output_type: str
    out_groups: list[str]
    rg_ref: ResponseGenerator

    def __init__(self,
                 block_id: int = -1,
                 output_type: str = None,
                 name: str = None,
                 in_groups: list[str] = None,
                 join: bool = False,
                 out_groups: list[str] = None,
                 rg_ref: ResponseGenerator = None
                 ) -> None:

        super().__init__(block_id, name, in_groups, join)
        if rg_ref is None:
            self.rg_ref = ResponseGenerator()
        else:
            self.rg_ref = rg_ref

        self.output_type = output_type
        self.out_groups = out_groups if out_groups is not None else [
            'public']  # List of groups the participant will label messages for

    def generate_response(self,
                          message_id: int,
                          ledger: list[Message]
                          ) -> Message:

        message_id = message_id
        block_id = self.block_id
        message_type = self.output_type
        groups = self.out_groups

        ledger = self.ledger_filtered(ledger)

        if self.rg_ref.is_prepared():
            content = self.rg_ref.generate_response(ledger)
        else:
            raise RuntimeError("Response generator is unprepared")
        timestamp = datetime.now()

        return Message(message_id=message_id,
                       timestamp=timestamp,
                       block_id=block_id,
                       content=content,
                       message_type=message_type,
                       groups=groups)

    def ledger_filtered(self,
                        ledger: list[Message]
                        ) -> list[Message]:
        ledger_new = []
        for message in ledger:
            if self.validate_readable(message):
                ledger_new.append(message)
        return ledger_new

    def validate_readable(self,
                          message: Message
                          ) -> bool:
        """
        Return true if at least one of the message's groups belong to this responder's in_groups
        :param message:
        :return:
        """
        for my_group in self.in_groups:
            if my_group in message.groups:
                return True
        return False

    def is_responder(self
                     ) -> bool:
        return True

    def is_prepared(self
                    ) -> bool:
        return self.rg_ref.is_prepared()
