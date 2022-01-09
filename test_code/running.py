from typing import Any, Optional

class Runner:
    def __init__(self, loader: Any, optimizer: Optional[Any] = None):
        self.loader = loader
        self.optimizer = optimizer