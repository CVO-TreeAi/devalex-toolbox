"""DevAlex configuration and constants"""

import os
from pathlib import Path

class DevAlexConfig:
    """DevAlex configuration constants and settings"""
    
    VERSION = "1.0.0"
    
    ASCII_ART = """
    ████████▄     ▄████████  ▄█    █▄       ▄████████  ▄█          ▄████████ ▀████    ▐████▀ 
    ███   ▀███   ███    ███ ███    ███     ███    ███ ███         ███    ███   ███▌   ████▀  
    ███    ███   ███    █▀  ███    ███     ███    ███ ███         ███    █▀     ███  ▐███    
    ███    ███  ▄███▄▄▄     ███    ███     ███    ███ ███        ▄███▄▄▄        ▀███▄███▀    
    ███    ███ ▀▀███▀▀▀     ███    ███   ▀███████████ ███       ▀▀███▀▀▀        ████▀██▄     
    ███    ███   ███    █▄  ███    ███     ███    ███ ███         ███    █▄    ▐███  ▀███    
    ███   ▄███   ███    ███ ███    ███     ███    ███ ███▌    ▄   ███    ███  ▄███     ███▄  
    ████████▀    ██████████  ▀██████▀      ███    █▀  █████▄▄██   ██████████ ████       ███▄ 
                                                      ▀                                      

    🤖 Your Personal Claude Code Supercharger - Always Ready, Always Learning, Always Improving
    """
    
    # Paths
    TOOLBOX_ROOT = Path(__file__).parent.parent.parent.parent  # /path/to/devalex-toolbox
    HOME_DIR = Path.home()
    DEVALEX_DIR = HOME_DIR / ".devalex"
    CONFIG_DIR = DEVALEX_DIR / "config"
    TEMPLATES_DIR = DEVALEX_DIR / "templates"
    CACHE_DIR = DEVALEX_DIR / "cache"
    LOGS_DIR = DEVALEX_DIR / "logs"
    
    # Project configuration
    PROJECT_DEFAULTS = {
        "architecture": "vertical_slice",
        "testing": "comprehensive", 
        "security": "enabled",
        "ai_integration": "full"
    }
    
    # Activation triggers
    TRIGGERS = [
        "devalex", "DevAlex", "DEVALEX",
        "devalx", "devlex",  # Common typos
        "dev alex"  # Spaced version
    ]
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all DevAlex directories exist"""
        dirs = [cls.DEVALEX_DIR, cls.CONFIG_DIR, cls.TEMPLATES_DIR, cls.CACHE_DIR, cls.LOGS_DIR]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    @classmethod 
    def is_devalex_project(cls, path=None):
        """Check if current/given directory is a DevAlex project"""
        if path is None:
            path = Path.cwd()
        else:
            path = Path(path)
        return (path / "devalex.json").exists()
        
    @classmethod
    def is_installed(cls):
        """Check if DevAlex is installed"""
        return cls.DEVALEX_DIR.exists() and (cls.CONFIG_DIR / "devalex.json").exists()