"""Example resource endpoints. Reads are public; writes require JWT."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..deps import get_current_user

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class Item(ItemCreate):
    id: int
    created_by: str


_items: dict[int, Item] = {}
_next_id: int = 1


@router.get("", response_model=list[Item], summary="List items (public)")
def list_items() -> list[Item]:
    return list(_items.values())


@router.get("/{item_id}", response_model=Item, summary="Get one item (public)")
def get_item(item_id: int) -> Item:
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return item


@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create item (authenticated)",
)
def create_item(payload: ItemCreate, user: str = Depends(get_current_user)) -> Item:
    global _next_id
    item = Item(id=_next_id, created_by=user, **payload.model_dump())
    _items[_next_id] = item
    _next_id += 1
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item (authenticated)",
)
def delete_item(item_id: int, user: str = Depends(get_current_user)) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    del _items[item_id]
