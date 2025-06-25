from abc import ABC, abstractmethod


class PatcherInterface(ABC):
    @abstractmethod
    def apply(self) -> None:
        """Apply patches to the kernel source code."""
        ...
