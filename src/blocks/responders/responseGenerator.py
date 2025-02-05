from message import Message

class ResponseGenerator:
    """
    A ResponseGenerator is a function object whose sole purpose is to be able to take the ledgers,
    i.e. a list of messages, and produce a string response.
    """
    def __init__(self,
                 ) -> None:
        pass

    def generate_response(self,
                          ledger: list[Message],
                          *kwargs
                          ) -> str:
        return ""

    def prepare_response(self,
                         content: str
                         ) -> None:
        pass

    def is_prepared(self,
                    ) -> bool:
        return True
