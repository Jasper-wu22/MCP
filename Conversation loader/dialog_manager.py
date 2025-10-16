"""
Dialog Manager MCP Server
Save and load conversation history for AI context

Features:
- Save current conversations
- Load previous dialogs
- Search through saved conversations
- Organize by date, topic, or tags
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from mcp.server.fastmcp import FastMCP

# instantiate an MCP server for dialog management
mcp = FastMCP("Dialog Manager")

# Default storage directory
DIALOGS_DIR = Path.home() / "Documents" / "saved_dialogs"
DIALOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_dialog_path(dialog_id: str) -> Path:
    """Get the path for a dialog file"""
    return DIALOGS_DIR / f"{dialog_id}.json"


def generate_dialog_id() -> str:
    """Generate a unique dialog ID based on timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ==================== SAVE DIALOGS ====================

@mcp.tool()
def save_dialog(
    content: str,
    title: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Save the current dialog/conversation
    
    Args:
        content: The dialog content to save
        title: Optional title for the dialog
        tags: Optional list of tags for categorization
        metadata: Optional additional metadata
    
    Returns:
        Information about the saved dialog
    """
    try:
        dialog_id = generate_dialog_id()
        
        dialog_data = {
            "id": dialog_id,
            "title": title or f"Dialog {dialog_id}",
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or [],
            "metadata": metadata or {},
            "word_count": len(content.split()),
            "char_count": len(content)
        }
        
        file_path = get_dialog_path(dialog_id)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Dialog saved successfully",
            "dialog_id": dialog_id,
            "title": dialog_data["title"],
            "file_path": str(file_path),
            "word_count": dialog_data["word_count"],
            "timestamp": dialog_data["timestamp"]
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def save_current_context(
    messages: List[Dict[str, str]],
    title: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Save the current conversation context as structured messages
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        title: Optional title for the conversation
        tags: Optional tags for categorization
    
    Returns:
        Information about the saved conversation
    """
    try:
        dialog_id = generate_dialog_id()
        
        # Format messages nicely
        formatted_content = []
        for msg in messages:
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            formatted_content.append(f"[{role}]: {content}")
        
        full_content = "\n\n".join(formatted_content)
        
        dialog_data = {
            "id": dialog_id,
            "title": title or f"Conversation {dialog_id}",
            "messages": messages,
            "formatted_content": full_content,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or [],
            "message_count": len(messages),
            "total_words": len(full_content.split())
        }
        
        file_path = get_dialog_path(dialog_id)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Conversation context saved",
            "dialog_id": dialog_id,
            "title": dialog_data["title"],
            "file_path": str(file_path),
            "message_count": len(messages),
            "timestamp": dialog_data["timestamp"]
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def quick_save(text: str) -> Dict[str, Any]:
    """Quick save text without extra parameters
    
    Args:
        text: The text to save
    
    Returns:
        Saved dialog information
    """
    return save_dialog(
        content=text,
        title=f"Quick Save {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


# ==================== LOAD DIALOGS ====================

@mcp.tool()
def load_dialog(dialog_id: str) -> Dict[str, Any]:
    """Load a specific dialog by ID
    
    Args:
        dialog_id: The ID of the dialog to load
    
    Returns:
        The dialog data
    """
    try:
        file_path = get_dialog_path(dialog_id)
        
        if not file_path.exists():
            return {"error": f"Dialog {dialog_id} not found"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            dialog_data = json.load(f)
        
        return {
            "success": True,
            "dialog": dialog_data
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def load_last_dialog() -> Dict[str, Any]:
    """Load the most recently saved dialog
    
    Returns:
        The most recent dialog data
    """
    try:
        dialogs = list_dialogs()
        
        if not dialogs.get('dialogs'):
            return {"error": "No saved dialogs found"}
        
        # Get the most recent (first in the sorted list)
        latest_id = dialogs['dialogs'][0]['id']
        
        return load_dialog(latest_id)
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def load_dialog_content(dialog_id: str) -> str:
    """Load just the content of a dialog (for AI to read)
    
    Args:
        dialog_id: The ID of the dialog to load
    
    Returns:
        The dialog content as a string
    """
    try:
        result = load_dialog(dialog_id)
        
        if result.get('error'):
            return f"Error: {result['error']}"
        
        dialog = result['dialog']
        
        # Format nicely for AI to read
        output = []
        output.append(f"=== {dialog['title']} ===")
        output.append(f"Saved: {dialog['timestamp']}")
        output.append(f"Tags: {', '.join(dialog.get('tags', []))}")
        output.append("\n--- Content ---\n")
        
        if 'messages' in dialog:
            # Structured conversation
            output.append(dialog.get('formatted_content', ''))
        else:
            # Plain content
            output.append(dialog['content'])
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error loading dialog: {str(e)}"


# ==================== LIST & SEARCH ====================

@mcp.tool()
def list_dialogs(
    limit: int = 20,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None
) -> Dict[str, Any]:
    """List saved dialogs
    
    Args:
        limit: Maximum number of dialogs to return
        tags: Filter by tags
        search: Search in titles and content
    
    Returns:
        List of dialogs with metadata
    """
    try:
        dialog_files = sorted(
            DIALOGS_DIR.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        dialogs = []
        
        for file_path in dialog_files[:limit]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Apply filters
                if tags:
                    if not any(tag in data.get('tags', []) for tag in tags):
                        continue
                
                if search:
                    search_lower = search.lower()
                    if search_lower not in data.get('title', '').lower() and \
                       search_lower not in data.get('content', '').lower():
                        continue
                
                dialogs.append({
                    "id": data['id'],
                    "title": data['title'],
                    "timestamp": data['timestamp'],
                    "tags": data.get('tags', []),
                    "word_count": data.get('word_count', 0),
                    "file_path": str(file_path)
                })
            
            except Exception:
                continue
        
        return {
            "success": True,
            "dialogs": dialogs,
            "total": len(dialogs),
            "storage_path": str(DIALOGS_DIR)
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_dialogs(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search through saved dialogs
    
    Args:
        query: Search query
        limit: Maximum results to return
    
    Returns:
        Matching dialogs
    """
    return list_dialogs(limit=limit, search=query)


@mcp.tool()
def get_dialogs_by_tag(tag: str) -> Dict[str, Any]:
    """Get all dialogs with a specific tag
    
    Args:
        tag: Tag to filter by
    
    Returns:
        List of matching dialogs
    """
    return list_dialogs(tags=[tag], limit=100)


@mcp.tool()
def get_recent_dialogs(count: int = 5) -> Dict[str, Any]:
    """Get the most recent dialogs
    
    Args:
        count: Number of recent dialogs to retrieve
    
    Returns:
        List of recent dialogs
    """
    return list_dialogs(limit=count)


# ==================== MANAGE DIALOGS ====================

@mcp.tool()
def delete_dialog(dialog_id: str) -> Dict[str, Any]:
    """Delete a saved dialog
    
    Args:
        dialog_id: ID of the dialog to delete
    
    Returns:
        Deletion result
    """
    try:
        file_path = get_dialog_path(dialog_id)
        
        if not file_path.exists():
            return {"error": f"Dialog {dialog_id} not found"}
        
        file_path.unlink()
        
        return {
            "success": True,
            "message": f"Dialog {dialog_id} deleted"
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def update_dialog_tags(dialog_id: str, tags: List[str]) -> Dict[str, Any]:
    """Update tags for a dialog
    
    Args:
        dialog_id: ID of the dialog
        tags: New tags to set
    
    Returns:
        Update result
    """
    try:
        result = load_dialog(dialog_id)
        if result.get('error'):
            return result
        
        dialog_data = result['dialog']
        dialog_data['tags'] = tags
        
        file_path = get_dialog_path(dialog_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Tags updated",
            "dialog_id": dialog_id,
            "tags": tags
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def rename_dialog(dialog_id: str, new_title: str) -> Dict[str, Any]:
    """Rename a dialog
    
    Args:
        dialog_id: ID of the dialog
        new_title: New title for the dialog
    
    Returns:
        Rename result
    """
    try:
        result = load_dialog(dialog_id)
        if result.get('error'):
            return result
        
        dialog_data = result['dialog']
        old_title = dialog_data['title']
        dialog_data['title'] = new_title
        
        file_path = get_dialog_path(dialog_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Dialog renamed",
            "dialog_id": dialog_id,
            "old_title": old_title,
            "new_title": new_title
        }
    
    except Exception as e:
        return {"error": str(e)}


# ==================== EXPORT & IMPORT ====================

@mcp.tool()
def export_dialog_as_markdown(dialog_id: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Export a dialog as a Markdown file
    
    Args:
        dialog_id: ID of the dialog to export
        output_path: Optional custom output path
    
    Returns:
        Export result with file path
    """
    try:
        result = load_dialog(dialog_id)
        if result.get('error'):
            return result
        
        dialog = result['dialog']
        
        if not output_path:
            output_path = DIALOGS_DIR / f"{dialog_id}.md"
        else:
            output_path = Path(output_path)
        
        # Create markdown content
        markdown = []
        markdown.append(f"# {dialog['title']}\n")
        markdown.append(f"**Saved:** {dialog['timestamp']}")
        markdown.append(f"**Tags:** {', '.join(dialog.get('tags', []))}\n")
        markdown.append("---\n")
        
        if 'messages' in dialog:
            for msg in dialog['messages']:
                role = msg.get('role', 'unknown').upper()
                content = msg.get('content', '')
                markdown.append(f"## {role}\n")
                markdown.append(f"{content}\n")
        else:
            markdown.append(dialog['content'])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown))
        
        return {
            "success": True,
            "message": "Dialog exported as Markdown",
            "file_path": str(output_path)
        }
    
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_storage_info() -> Dict[str, Any]:
    """Get information about dialog storage
    
    Returns:
        Storage statistics
    """
    try:
        dialog_files = list(DIALOGS_DIR.glob("*.json"))
        
        total_size = sum(f.stat().st_size for f in dialog_files)
        
        return {
            "storage_path": str(DIALOGS_DIR),
            "total_dialogs": len(dialog_files),
            "total_size_mb": f"{total_size / (1024*1024):.2f}",
            "total_size_bytes": total_size
        }
    
    except Exception as e:
        return {"error": str(e)}


# ==================== RESOURCES ====================

@mcp.resource("dialog://{dialog_id}")
def get_dialog_resource(dialog_id: str) -> str:
    """Get a dialog as a resource
    
    Args:
        dialog_id: ID of the dialog
    
    Returns:
        Dialog content
    """
    return load_dialog_content(dialog_id)


@mcp.resource("dialogs://recent")
def get_recent_dialogs_resource() -> str:
    """Get recent dialogs as a resource
    
    Returns:
        List of recent dialogs
    """
    result = get_recent_dialogs(10)
    return json.dumps(result, indent=2)


# execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")

