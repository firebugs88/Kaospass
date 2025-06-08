# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python password generator application called "Kaospass" with a Tkinter GUI interface. The application generates cryptographically secure passwords and saves them to a default file location.

## Architecture

The codebase consists of two main modules:

- `pass.py`: Main application containing password generation logic, GUI components, and utility functions
- `colors.py`: Color scheme definitions for the UI theme

### Core Components

- **Password Generation**: Uses Python's `secrets` module for cryptographic randomness with configurable character type requirements (lowercase, uppercase, digits, punctuation)
- **GUI Framework**: Built with Tkinter featuring a compact interface with icon buttons, tooltips, and notification banners
- **File Management**: Automatically saves generated passwords to `~/Desktop/kaospass_passwords.txt`

### Key Classes and Functions

- `generate_password_and_save()`: Core password generation with secure shuffling
- `NotificationBanner`: Toast-style notifications for user feedback
- `ToolTip`: Hover tooltips for icon buttons
- GUI handlers: `gui_handle_generate_password_compact()`, `copy_to_clipboard_compact()`

## Development Commands

Since this is a standalone Python application with no external dependencies beyond the standard library:

- **Run the application**: `python pass.py`
- **Test basic functionality**: Run the main script and verify password generation and GUI interaction

## File Locations

- Generated passwords are saved to: `~/Desktop/kaospass_passwords.txt`
- UI color scheme is centralized in `colors.py` for easy theming modifications