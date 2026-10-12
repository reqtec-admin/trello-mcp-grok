import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trello")

TRELLO_KEY = os.environ["TRELLO_API_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]
BASE = "https://api.trello.com/1"

def trello(method: str, path: str, **params) -> Any:
    params = {**params, "key": TRELLO_KEY, "token": TRELLO_TOKEN}
    r = httpx.request(method, f"{BASE}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def list_boards() -> list[dict]:
    """List all boards the authenticated user can access."""
    return trello("GET", "/members/me/boards", fields="id,name,url,closed")

@mcp.tool()
def get_board(board_id: str) -> dict:
    """Get a board and its lists."""
    board = trello("GET", f"/boards/{board_id}", fields="id,name,url,desc")
    lists = trello("GET", f"/boards/{board_id}/lists", fields="id,name,closed")
    board["lists"] = lists
    return board

@mcp.tool()
def list_cards(list_id: str, include_closed: bool = False) -> list[dict]:
    """List cards in a list."""
    return trello(
        "GET",
        f"/lists/{list_id}/cards",
        fields="id,name,desc,due,closed,idList,labels,url",
        filter="all" if include_closed else "open",
    )

@mcp.tool()
def create_card(list_id: str, name: str, desc: str = "", due: str | None = None) -> dict:
    """Create a card in the given list."""
    params = {"idList": list_id, "name": name, "desc": desc}
    if due:
        params["due"] = due
    return trello("POST", "/cards", **params)

@mcp.tool()
def move_card(card_id: str, list_id: str) -> dict:
    """Move a card to another list."""
    return trello("PUT", f"/cards/{card_id}", idList=list_id)

@mcp.tool()
def add_comment(card_id: str, text: str) -> dict:
    """Add a comment to a card."""
    return trello("POST", f"/cards/{card_id}/actions/comments", text=text)

@mcp.tool()
def search(query: str, limit: int = 20) -> dict:
    """Search cards and boards."""
    return trello("GET", "/search", query=query, cards_limit=limit, boards_limit=5)

@mcp.tool()
def get_card(card_id: str) -> dict:
    """Get details of a specific card."""
    return trello("GET", f"/cards/{card_id}", fields="id,name,desc,due,closed,idList,labels,url,checklists")

@mcp.tool()
def archive_card(card_id: str) -> dict:
    """Archive (close) a card."""
    return trello("PUT", f"/cards/{card_id}", closed=True)

if __name__ == "__main__":
    # Streamable HTTP — required for Grok remote connectors
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
