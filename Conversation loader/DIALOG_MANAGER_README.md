# 💬 Dialog Manager MCP Server

Save and load conversation history to give AI context from previous discussions!

## 🎯 What It Does

The Dialog Manager lets you:
- **Save conversations** - "Save this dialog" or "Save these messages"
- **Load previous dialogs** - "Load the last dialog I saved"
- **Search history** - Find specific conversations by keyword or tag
- **Give AI context** - AI can read your saved conversations

## ⚡ Quick Start

### Save Your First Dialog

**Simple Save:**
```python
quick_save("This is my important conversation about Revit API integration")
```

**Save with Details:**
```python
save_dialog(
    content="Discussion about creating holes in Revit bed models...",
    title="Revit Bed Editing Session",
    tags=["revit", "geometry", "editing"]
)
```

**Save Structured Conversation:**
```python
save_current_context(
    messages=[
        {"role": "user", "content": "How do I edit Revit files?"},
        {"role": "assistant", "content": "You can use the Revit API..."},
        {"role": "user", "content": "Can you create a hole?"},
        {"role": "assistant", "content": "Yes! Here's how..."}
    ],
    title="Revit API Tutorial",
    tags=["tutorial", "revit"]
)
```

### Load Previous Dialogs

**Load the Most Recent:**
```python
load_last_dialog()
# Returns the complete dialog with all metadata
```

**Load Specific Dialog:**
```python
load_dialog("20251015_123456")
```

**Load for AI to Read:**
```python
content = load_dialog_content("20251015_123456")
# AI can now see the full conversation!
```

## 📚 All Available Tools

### Saving (3 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `quick_save(text)` | Quick save without extras | `quick_save("My notes")` |
| `save_dialog(content, title, tags, metadata)` | Save with details | See above |
| `save_current_context(messages, title, tags)` | Save structured conversation | See above |

### Loading (3 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `load_last_dialog()` | Load most recent | `load_last_dialog()` |
| `load_dialog(dialog_id)` | Load specific dialog | `load_dialog("20251015_123456")` |
| `load_dialog_content(dialog_id)` | Get content for AI | `load_dialog_content("20251015_123456")` |

### Browsing (4 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `list_dialogs(limit, tags, search)` | List saved dialogs | `list_dialogs(limit=10)` |
| `search_dialogs(query, limit)` | Search by keyword | `search_dialogs("revit")` |
| `get_dialogs_by_tag(tag)` | Filter by tag | `get_dialogs_by_tag("tutorial")` |
| `get_recent_dialogs(count)` | Get recent dialogs | `get_recent_dialogs(5)` |

### Managing (3 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `delete_dialog(dialog_id)` | Delete a dialog | `delete_dialog("20251015_123456")` |
| `update_dialog_tags(dialog_id, tags)` | Update tags | `update_dialog_tags("...", ["new", "tags"])` |
| `rename_dialog(dialog_id, new_title)` | Rename dialog | `rename_dialog("...", "New Title")` |

### Exporting (2 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `export_dialog_as_markdown(dialog_id, output_path)` | Export to Markdown | `export_dialog_as_markdown("...")` |
| `get_storage_info()` | Get storage stats | `get_storage_info()` |

## 💡 Use Cases

### 1. Save Context Between Sessions

```python
# End of session - save everything
save_current_context(
    messages=[...all messages...],
    title="Revit MCP Server Development",
    tags=["development", "revit", "mcp"]
)
```

Later:
```python
# Start new session - load context
content = load_dialog_content(last_dialog_id)
# Now AI knows what happened before!
```

### 2. Create Knowledge Base

```python
# Save tutorial
save_dialog(
    content="""
    Step 1: Install pyRevit
    Step 2: Run API server
    Step 3: Connect from MCP
    """,
    title="Revit Setup Tutorial",
    tags=["tutorial", "setup", "revit"]
)

# Later: Search for it
tutorials = get_dialogs_by_tag("tutorial")
```

### 3. Document Solutions

```python
# After solving a problem
save_dialog(
    content="Solution: The bug was caused by incorrect type hints...",
    title="Fixed Type Hints Bug",
    tags=["bugfix", "python", "types"]
)

# Find all bugfixes later
bugfixes = search_dialogs("bugfix")
```

### 4. Track Project Progress

```python
# Day 1
save_dialog("Created basic MCP server", title="Day 1", tags=["progress"])

# Day 2
save_dialog("Added Revit API integration", title="Day 2", tags=["progress"])

# View all progress
progress = get_dialogs_by_tag("progress")
```

## 📂 Storage

### Where Are Dialogs Saved?

**Default Location:**
```
~/Documents/saved_dialogs/
```

Each dialog is saved as a JSON file:
```
20251015_123456.json
20251015_134500.json
...
```

### Check Storage Info

```python
info = get_storage_info()
# Returns:
# {
#   "storage_path": "/Users/you/Documents/saved_dialogs",
#   "total_dialogs": 42,
#   "total_size_mb": "2.45"
# }
```

## 🔍 Searching & Filtering

### Search by Keyword

```python
# Search in titles and content
results = search_dialogs("revit api", limit=10)
```

### Filter by Tags

```python
# Get all tutorials
tutorials = get_dialogs_by_tag("tutorial")

# Get recent revit discussions
revit_dialogs = list_dialogs(tags=["revit"], limit=20)
```

### Combined Search

```python
# Search with filters
results = list_dialogs(
    limit=10,
    tags=["revit", "tutorial"],
    search="hole creation"
)
```

## 📤 Export Options

### Export as Markdown

```python
export_dialog_as_markdown(
    dialog_id="20251015_123456",
    output_path="~/Documents/my_tutorial.md"
)
```

The exported Markdown includes:
- Title and metadata
- Tags
- Formatted content
- Timestamp

## 🤖 AI Context Loading

### Give AI Previous Context

```python
# User: "Load the last dialog so you remember our discussion"

# In code:
last_dialog = load_last_dialog()
content = last_dialog['dialog']['content']

# AI can now reference that content!
```

### Example Workflow

```python
# Session 1: Save work
save_current_context(
    messages=[...conversation...],
    title="Revit API Integration Discussion"
)

# Session 2: Load and continue
recent = get_recent_dialogs(1)
dialog_id = recent['dialogs'][0]['id']
context = load_dialog_content(dialog_id)

# AI now has context from Session 1
```

## 🎨 Dialog Structure

### Saved Dialog Format

```json
{
  "id": "20251015_123456",
  "title": "My Dialog",
  "content": "The conversation text...",
  "timestamp": "2025-10-15T12:34:56",
  "tags": ["tag1", "tag2"],
  "metadata": {},
  "word_count": 150,
  "char_count": 890
}
```

### Conversation Format

```json
{
  "id": "20251015_123456",
  "title": "My Conversation",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ],
  "formatted_content": "[USER]: Hello\n\n[ASSISTANT]: Hi there!",
  "timestamp": "2025-10-15T12:34:56",
  "tags": ["chat"],
  "message_count": 2,
  "total_words": 5
}
```

## 🔐 Privacy & Security

- **Local Storage**: All dialogs stored locally on your machine
- **No Cloud**: Nothing sent to external servers
- **Full Control**: You own and manage all data
- **Easy Backup**: Just copy the `saved_dialogs` folder

## 🛠️ Advanced Usage

### Custom Metadata

```python
save_dialog(
    content="My content",
    title="Project Discussion",
    metadata={
        "project": "Revit MCP",
        "version": "1.0",
        "priority": "high",
        "custom_field": "any value"
    }
)
```

### Batch Operations

```python
# Get all dialogs
all_dialogs = list_dialogs(limit=1000)

# Process each
for dialog_info in all_dialogs['dialogs']:
    dialog = load_dialog(dialog_info['id'])
    # Do something with each dialog
```

## 📊 Examples

### Example 1: Daily Journal

```python
# End of each day
quick_save(f"Today I worked on: {today_summary}")

# View journal entries
journal = search_dialogs("Today I worked")
```

### Example 2: Code Snippets

```python
save_dialog(
    content='''
    def create_void(element_id, radius):
        connector.create_cylindrical_void(...)
    ''',
    title="Revit Void Creation Function",
    tags=["code", "revit", "python"]
)

# Find all code snippets
code_snippets = get_dialogs_by_tag("code")
```

### Example 3: Learning Notes

```python
save_current_context(
    messages=[
        {"role": "user", "content": "How does MCP work?"},
        {"role": "assistant", "content": "MCP is Model Context Protocol..."}
    ],
    title="Learning MCP Basics",
    tags=["learning", "mcp", "concepts"]
)

# Review learning notes
learning = get_dialogs_by_tag("learning")
```

## 🚀 Integration with Other Tools

### With Revit Manager

```python
# Save Revit workflow
save_dialog(
    content="""
    Workflow for editing bed model:
    1. revit_connect()
    2. revit_open_document(file_path)
    3. revit_get_elements("Furniture")
    4. revit_create_void_cylinder(...)
    5. revit_save_document()
    """,
    title="Bed Editing Workflow",
    tags=["workflow", "revit"]
)
```

### Resources

Use MCP resources to access dialogs:

```
dialog://20251015_123456     - Get specific dialog
dialogs://recent              - Get recent dialogs
```

## 🔄 Workflow Tips

1. **Save Often**: Save important discussions as they happen
2. **Use Tags**: Organize with consistent tagging
3. **Descriptive Titles**: Make dialogs easy to find later
4. **Search First**: Before asking repeated questions, search your history
5. **Export Important**: Export key dialogs as Markdown for safekeeping

## 📈 Benefits

✅ **Persistent Memory** - AI can remember previous conversations  
✅ **Knowledge Base** - Build up useful information over time  
✅ **Quick Reference** - Find past solutions instantly  
✅ **Context Continuity** - Seamless multi-session workflows  
✅ **Searchable History** - Never lose important discussions  

---

**Ready to start?** Just say:
- "Save this dialog"
- "Quick save these notes"
- "Load the last dialog"
- "Show me my recent conversations"

The Dialog Manager will handle the rest! 💬✨

