from dataclasses import dataclass

@dataclass
class SceneTemplate:
    text: str
    required_positions: list[str]