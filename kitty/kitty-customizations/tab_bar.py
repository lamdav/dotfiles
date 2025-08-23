"""
Custom tab bar for Kitty terminal with process-based icons
Similar to iTerm2's automatic process icons
"""

import subprocess
from typing import List
from kitty.boss import get_boss
from kitty.fast_data_types import Screen, get_options
from kitty.tab_bar import DrawData, ExtraData, TabBarData, as_rgb, draw_title
from kitty.utils import color_as_int


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    """Draw a single tab with process icon"""
    
    # Get the current process name from the tab title
    title = tab.title or ""
    
    # Process to icon mapping
    process_icons = {
        # Editors
        'vim': '📝',
        'nvim': '📝',
        'nano': '📝',
        'emacs': '📝',
        'code': '💻',
        'subl': '💻',
        
        # AI Tools
        'claude': '🤖',
        'claude-code': '🤖',
        
        # Development tools
        'git': '🌿',
        'gh': '🐙',
        'docker': '🐳',
        'kubectl': '☸️',
        'helm': '⎈',
        
        # Language-specific
        'python': '🐍',
        'python3': '🐍',
        'pip': '🐍',
        'node': '🟢',
        'npm': '📦',
        'yarn': '📦',
        'go': '🐹',
        'ruby': '💎',
        'gem': '💎',
        'java': '☕',
        'javac': '☕',
        'cargo': '🦀',
        'rustc': '🦀',
        
        # Build tools
        'make': '🔨',
        'cmake': '🔨',
        'ninja': '🔨',
        'gradle': '🔨',
        'mvn': '🔨',
        
        # System tools
        'htop': '📊',
        'top': '📊',
        'ps': '📊',
        'kill': '⚡',
        'sudo': '🔐',
        'ssh': '🔑',
        'scp': '📂',
        'rsync': '🔄',
        'curl': '🌐',
        'wget': '🌐',
        'ping': '🏓',
        
        # File operations
        'ls': '📁',
        'cd': '📁',
        'pwd': '📁',
        'find': '🔍',
        'grep': '🔍',
        'rg': '🔍',
        'ack': '🔍',
        'cat': '📄',
        'less': '📄',
        'more': '📄',
        'tail': '📄',
        'head': '📄',
        'tar': '📦',
        'zip': '📦',
        'unzip': '📦',
        
        # Database
        'mysql': '🗄️',
        'psql': '🐘',
        'sqlite3': '🗄️',
        'redis-cli': '🔴',
        'mongo': '🍃',
        
        # Web servers
        'serve': '🌐',
        'http-server': '🌐',
        'nginx': '🌐',
        'apache2': '🌐',
        
        # Default shells
        'zsh': '🐚',
        'bash': '🐚',
        'fish': '🐠',
        'sh': '🐚',
    }
    
    # Extract process name from title
    icon = '🐚'  # Default shell icon
    
    # Try to extract process name from common patterns
    title_lower = title.lower()
    
    # Check for exact process matches
    for process, process_icon in process_icons.items():
        if process in title_lower:
            icon = process_icon
            break
    
    # Special cases for Go development
    if 'go run' in title_lower or 'go build' in title_lower or 'go test' in title_lower:
        icon = '🐹'
    elif 'go mod' in title_lower or 'go get' in title_lower:
        icon = '🐹'
    
    # Check if we're in a specific directory context
    if any(term in title_lower for term in ['~/go/', '/go/', 'golang', '.go']):
        if icon == '🐚':  # Only if no other process was detected
            icon = '🐹'
    
    # Python virtual environments
    if any(term in title_lower for term in ['venv', 'virtualenv', '.venv', 'conda']):
        icon = '🐍'
    
    # Node.js projects
    if any(term in title_lower for term in ['node_modules', 'package.json', '.js', '.ts']):
        if icon == '🐚':
            icon = '🟢'
    
    # Create the tab title with icon
    tab_title = f"{icon} {index + 1}: {tab.title}"
    
    # Ensure title fits within max length
    if len(tab_title) > max_title_length:
        # Truncate the title part, keep the icon and number
        prefix = f"{icon} {index + 1}: "
        available_space = max_title_length - len(prefix) - 3  # 3 for "..."
        if available_space > 0:
            truncated_title = tab.title[:available_space] + "..."
            tab_title = f"{prefix}{truncated_title}"
        else:
            tab_title = f"{icon} {index + 1}"
    
    # Use default drawing with our custom title
    fake_tab = tab._replace(title=tab_title)
    return draw_title(draw_data, screen, fake_tab, index, max_title_length)