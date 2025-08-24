# Firewatch Color Scheme Reference

This directory contains the shared color definitions used across all dotfiles configurations to ensure perfect visual consistency.

## Color Palette

### Base Colors
- **Background**: `#1e2027` - Deep dark blue-gray
- **Foreground**: `#9ba2b2` - Light blue-gray text
- **Main**: `#1e2027` - Primary background
- **Main Alt**: `#2e3642` - Secondary backgrounds (widgets, inactive states)
- **Minor**: `#58606f` - Subtle elements, borders
- **Accent**: `#44a8b6` - Cyan accent (focused elements, links)

### Standard Colors
- **Red**: `#d9537a` - Error states, warnings
- **Green**: `#5ab977` - Success states, confirmations  
- **Yellow**: `#dfb563` - Caution, highlights
- **Orange**: `#dfb563` - Same as yellow for consistency
- **Blue**: `#4d89c4` - Information, links
- **Magenta**: `#d55119` - Special highlights
- **Cyan**: `#44a8b6` - Primary accent (matches accent)
- **White**: `#e6e5ff` - Bright text, active states
- **Black**: `#1e2027` - True black (matches background)

## Usage Across Tools

### Kitty Terminal
- Uses full 16-color palette
- Cursor: accent cyan (`#44a8b6`)
- Selection: main alt background with white foreground
- Active tab: accent background with white text

### Simple-bar
- Widget backgrounds: `rgba(46, 54, 66, 0.8)` (main_alt with transparency)
- Focused workspace: accent cyan (`#44a8b6`)
- Unfocused workspace: main alt (`#2e3642`)
- Text: foreground (`#9ba2b2`)

### Powerlevel10k
- Should use the same color codes for consistency
- Focused elements use accent cyan
- Secondary elements use main alt

### iTerm2 
- Uses the standard 16-color palette
- Profiles should reference these exact hex values

## Maintenance

When updating colors:
1. Update `firewatch.conf` with new values
2. Source the changes in each tool's configuration
3. Test across all applications for consistency
4. Update this README with any changes

## Color Testing

To test colors across all tools:
```bash
# Reload kitty configuration
cmd+shift+r in Kitty

# Refresh simple-bar
refreshbar

# Test terminal colors
for i in {0..15}; do echo -e "\e[38;5;${i}mColor $i\e[0m"; done
```

This ensures the Firewatch theme maintains perfect consistency across your entire development environment.