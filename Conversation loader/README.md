# Dialog Manager MCP Server

A Model Context Protocol (MCP) server for saving, managing, and loading AI conversation dialogs.

> 💡 **Save your conversations and give AI context from previous sessions!**

This MCP server allows you to persist conversation history locally, search through past discussions, and load context into new AI sessions. Perfect for maintaining continuity across multiple work sessions or building a knowledge base of important conversations.

## Quick Start

1. **Configure** the server in `.cursor/mcp.json` (see [Configuration](#configuration))
2. **Restart** Cursor to load the MCP server
3. **Start using** the dialog tools in your AI conversations:
   - "Save this conversation"
   - "Load my last dialog"
   - "Search my dialogs for Python tutorials"

For more detailed examples, see [DIALOG_MANAGER_README.md](DIALOG_MANAGER_README.md).

## Features

### Save Conversations
- **Save dialogs** with title, tags, and metadata
- **Save current context** as structured messages
- **Quick save** text without extra parameters
- **Auto-timestamped** storage with unique IDs

### Load & Search
- **Load specific dialogs** by ID
- **Load last dialog** for quick access
- **Search dialogs** by content
- **Filter by tags** for organization
- **Get recent dialogs** for quick reference

### Management
- **List dialogs** with filtering options
- **Delete dialogs** when no longer needed
- **Update tags** for better organization
- **Rename dialogs** to update titles
- **Export as Markdown** for sharing
- **Storage info** to track usage

## Installation

1. Ensure you have Python 3.8+ installed

2. Activate the virtual environment:
```bash
source devenv/bin/activate
```

3. Install dependencies (if not already installed):
```bash
pip install mcp
```

## Configuration

Add to your MCP settings file (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "dialog-manager": {
      "command": "/Users/zhongwu/Documents/GitHub/Jasper/MCP/Conversation loader/devenv/bin/python",
      "args": [
        "/Users/zhongwu/Documents/GitHub/Jasper/MCP/Conversation loader/dialog_manager.py"
      ]
    }
  }
}
```

**Note**: Replace the paths above with your actual installation paths.

### Storage Location

Dialogs are automatically saved to:
```
~/Documents/saved_dialogs/
```

This directory is created automatically when you first use the server. You can check storage info at any time using the `get_storage_info()` tool.

**After configuring**: Restart Cursor for the changes to take effect.

## Usage

### Running via Cursor

Once configured in `mcp.json`, Cursor will automatically start the server when needed. You can use the tools directly from Cursor's AI interface.

### Running Standalone (for testing)

```bash
cd "/Users/zhongwu/Documents/GitHub/Jasper/MCP/Conversation loader"
source devenv/bin/activate
python dialog_manager.py
```

### Available Tools

**15 tools organized into 5 categories:**

#### Saving (3 tools)
- `save_dialog(content, title, tags, metadata)` - Save with full metadata
- `save_current_context(messages, title, tags)` - Save structured conversation
- `quick_save(text)` - Quick save without extras

#### Loading (3 tools)
- `load_dialog(dialog_id)` - Load specific dialog
- `load_last_dialog()` - Load most recent
- `load_dialog_content(dialog_id)` - Get content for AI to read

#### Browsing (4 tools)
- `list_dialogs(limit, tags, search)` - List with filtering
- `search_dialogs(query, limit)` - Search by keyword
- `get_dialogs_by_tag(tag)` - Filter by tag
- `get_recent_dialogs(count)` - Get recent dialogs

#### Managing (3 tools)
- `delete_dialog(dialog_id)` - Delete a dialog
- `update_dialog_tags(dialog_id, tags)` - Update tags
- `rename_dialog(dialog_id, new_title)` - Rename dialog

#### Exporting (2 tools)
- `export_dialog_as_markdown(dialog_id, output_path)` - Export to Markdown
- `get_storage_info()` - Get storage statistics

## Examples

### Save a conversation
```python
save_dialog(
    content="User asked about Python. I explained functions.",
    title="Python Functions Discussion",
    tags=["python", "programming", "tutorial"]
)
```

### Save structured messages
```python
save_current_context(
    messages=[
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language..."}
    ],
    title="Introduction to Python",
    tags=["python", "beginner"]
)
```

### Quick save
```python
quick_save("Remember to check authentication flow tomorrow")
```

### Load the last conversation
```python
load_last_dialog()
```

### Search dialogs
```python
search_dialogs(query="python functions", limit=5)
```

### List dialogs with tags
```python
list_dialogs(limit=10, tags=["python", "tutorial"])
```

### Export to Markdown
```python
export_dialog_as_markdown(
    dialog_id="20251016_092634",
    output_path="./exports/python_discussion.md"
)
```

## Storage

Dialogs are stored in `~/Documents/saved_dialogs/` by default. Each dialog is saved as a JSON file with:
- Unique timestamped ID
- Title and tags
- Full content and messages
- Metadata (timestamp, word count, etc.)

## MCP Resources

The server provides MCP resources for accessing dialogs:

- `dialog://{dialog_id}` - Access a specific dialog by ID
- `dialogs://recent` - Access the 10 most recent dialogs

Resources allow other MCP clients to retrieve dialog content directly.

## Troubleshooting

### Server not appearing in Cursor

1. Check that the paths in `mcp.json` are correct and absolute
2. Ensure the Python virtual environment exists at the specified path
3. Restart Cursor completely
4. Check Cursor's MCP logs for errors

### Permission errors

Make sure the `~/Documents/saved_dialogs/` directory is writable. The server will try to create it automatically on first use.

### Dependencies missing

Activate the virtual environment and install dependencies:
```bash
cd "/Users/zhongwu/Documents/GitHub/Jasper/MCP/Conversation loader"
source devenv/bin/activate
pip install mcp
```

## Additional Documentation

- **[DIALOG_MANAGER_README.md](DIALOG_MANAGER_README.md)** - Comprehensive guide with detailed examples and use cases
- **[dialog_manager.py](dialog_manager.py)** - Source code with inline documentation

## License

This is an open-source MCP server for dialog management.

## Contributing

Feel free to add more features or improve existing functionality!
