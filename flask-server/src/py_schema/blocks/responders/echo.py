from message import Message
from blocks.responders.responseGenerator import ResponseGenerator


class Echo(ResponseGenerator):
    prompt: str

    def __init__(self,
                 prompt: str = ""
                 ) -> None:
        super().__init__()
        self.prompt = prompt

    def generate_response(self,
                          ledger: list[Message],
                          *kwargs
                          ) -> str:
        return self.prompt
