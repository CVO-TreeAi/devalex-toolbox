"""DevAlex banner and branding utilities"""

from .config import DevAlexConfig

def print_banner():
    """Print DevAlex banner"""
    print(DevAlexConfig.ASCII_ART)
    print(f"    Version {DevAlexConfig.VERSION} - The Three Amigos: You, DevAlex, Claude Code")
    print("    " + "="*80)