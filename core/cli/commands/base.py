"""Base command class for DevAlex CLI commands"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser, _SubParsersAction

class BaseCommand(ABC):
    """Base class for all DevAlex commands"""
    
    @classmethod
    @abstractmethod
    def register(cls, subparsers: _SubParsersAction) -> ArgumentParser:
        """Register command with argument parser"""
        pass
    
    @abstractmethod
    def execute(self, args) -> None:
        """Execute the command with parsed arguments"""
        pass