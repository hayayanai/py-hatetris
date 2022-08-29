from dataclasses import dataclass


@dataclass
class Cell:
    landed: bool
    live: bool
