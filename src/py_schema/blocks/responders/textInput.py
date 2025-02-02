from message import Message
from blocks.responders.responseGenerator import ResponseGenerator
from queue import Queue


class TextInput(ResponseGenerator):
    """
    A ResponseGenerator is a function object whose sole purpose is to be able to take the ledgers,
    i.e. a list of messages, and produce a string response.
    """
    message_queue: Queue

    def __init__(self,
                 ) -> None:
        super().__init__()
        self.message_queue = Queue()

    def generate_response(self,
                          ledger: list[Message],
                          *kwargs
                          ) -> str:
        return self.message_queue.get()

    def prepare_response(self,
                         content: str,
                         ) -> None:
        self.message_queue.put(content)

    def is_prepared(self,
                    ) -> bool:
        return not self.message_queue.empty()
