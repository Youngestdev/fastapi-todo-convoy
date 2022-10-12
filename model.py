from dataclasses import dataclass

@dataclass
class WebhookData:
    event: str
    description: str
