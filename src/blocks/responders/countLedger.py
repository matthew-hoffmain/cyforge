from message import Message
from blocks.responders.responseGenerator import ResponseGenerator


class CountLedger(ResponseGenerator):
    """
    A ResponseGenerator is a function object whose sole purpose is to be able to take the ledgers,
    i.e. a list of messages, and produce a string response.
    """

    def __init__(self) -> None:
        super().__init__()

    def generate_response(self,
                          ledger: list[Message],
                          *kwargs
                          ) -> str:
        return f"{len(ledger)}"
