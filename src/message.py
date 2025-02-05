import datetime


class Message:
    message_id: int
    block_id: int
    timestamp: datetime
    message_type: str
    content: str
    groups: list[str]

    def __init__(self,
                 message_id: int,
                 block_id: int,
                 timestamp: datetime,
                 message_type: str,
                 content: str,
                 groups: list[str] = None,
                 ) -> None:
        if groups is None:
            groups = []
        self.message_id = message_id
        self.timestamp = timestamp
        self.block_id = block_id
        self.content = content
        self.message_type = message_type
        self.groups = groups  # List of groups that can access this message

    def get(self
            ) -> str:
        return f"ID#{self.message_id}:BLOCK#{self.block_id}:{self.content}"

    def read(self
             ) -> None:
        print(f"ID#{self.message_id}:BLOCK#{self.block_id}:{self.content}")

    def dict(self
             ) -> dict:
        return {"message_id": self.message_id,
                "block_id": self.block_id,
                "timestamp": self.timestamp,
                "message_type": self.message_type,
                "content": self.content,
                "groups": self.groups}
