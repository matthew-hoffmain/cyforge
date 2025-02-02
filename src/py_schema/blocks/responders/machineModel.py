"""
SUPPORT FOR EVERY MODEL GOES HERE
"""
from openai import OpenAI
from blocks.responders.responseGenerator import ResponseGenerator


class MachineModel(ResponseGenerator):
    make: str
    model: str
    api_key: str

    def __init__(self,
                 make: str,
                 model: str,
                 api_key: str
                 ) -> None:

        super().__init__()
        self.make = make
        self.model = model
        self.api_key = api_key

    def generate_response(self,
                          ledger,
                          **kwargs,
                          ) -> str:
        match self.make:
            case "openai":
                openai_textmodels = ["gpt-4o", "gpt-4o-mini"]
                if self.model in openai_textmodels:
                    # todo: check roles
                    history = [{"role": "assistant", "content": message.content} for message in ledger]
                    client = OpenAI(api_key=self.api_key)
                    response = client.chat.completions.create(
                        model=self.model,
                        messages=history,
                        temperature=0
                    )
                    return response.choices[0].message.content
            case _:
                raise NotImplementedError(f"Unsupported machine model: make={self.make}, model={self.model}")
