# Dialog Manager MCP Server

A Model Context Protocol (MCP) server for saving, managing, and loading AI conversation dialogs.

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
      "command": "/path/to/ipapi-mcp-server/devenv/bin/python",
      "args": ["/path/to/ipapi-mcp-server/dialog_manager.py"]
    }
  }
}
```

### Environment Variables

Copy the `env.template` file to `.env` and customize as needed:

```bash
cp env.template .env
```

Key configuration options:

- **MCP_SERVER_NAME**: Server display name
- **MCP_LOG_LEVEL**: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- **DIALOG_STORAGE_PATH**: Where dialogs are saved (default: ~/Documents/saved_dialogs/)
- **MAX_DIALOGS_IN_LIST**: Maximum number of dialogs to return in list operations

## Usage

### Running the Server

```bash
python dialog_manager.py
```

### Available Tools

#### 1. save_dialog(content, title, tags, metadata)
Save a dialog/conversation with optional metadata.

#### 2. save_current_context(messages, title, tags)
Save the current conversation context as structured messages.

#### 3. quick_save(text)
Quick save text without extra parameters.

#### 4. load_dialog(dialog_id)
Load a specific dialog by ID.

#### 5. load_last_dialog()
Load the most recently saved dialog.

#### 6. load_dialog_content(dialog_id)
Load just the content of a dialog (for AI to read).

#### 7. list_dialogs(limit, tags, search)
List saved dialogs with optional filtering.

#### 8. search_dialogs(query, limit)
Search through saved dialogs.

#### 9. get_dialogs_by_tag(tag)
Get all dialogs with a specific tag.

#### 10. get_recent_dialogs(count)
Get the most recent dialogs.

#### 11. delete_dialog(dialog_id)
Delete a saved dialog.

#### 12. update_dialog_tags(dialog_id, tags)
Update tags for a dialog.

#### 13. rename_dialog(dialog_id, new_title)
Rename a dialog.

#### 14. export_dialog_as_markdown(dialog_id, output_path)
Export a dialog as a Markdown file.

#### 15. get_storage_info()
Get information about dialog storage.

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

## License

This is an open-source MCP server for dialog management.

## Contributing

Feel free to add more features or improve existing functionality!
