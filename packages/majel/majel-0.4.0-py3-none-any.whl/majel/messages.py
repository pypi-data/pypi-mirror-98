from dataclasses import dataclass


@dataclass
class Message:
    type: str
    data: dict
    context: dict
