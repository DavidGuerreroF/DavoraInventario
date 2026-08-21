from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db
from backend.app.schemas.inventory_group import InventoryGroupCreate, InventoryGroupUpdate
from backend.app.schemas.supplier import SupplierCreate, SupplierUpdate
from backend.app.crud.inventory_group import (
    create_group as crud_create_group,
    get_group as crud_get_group,
    list_groups as crud_list_groups,
    update_group as crud_update_group,
    delete_group as crud_delete_group,
)
from backend.app.crud.supplier import (
    create_supplier as crud_create_supplier,
    get_supplier as crud_get_supplier,
    list_suppliers as crud_list_suppliers,
    update_supplier as crud_update_supplier,
    delete_supplier as crud_delete_supplier,
)

router = APIRouter(tags=["inventory"], prefix="/inventory")


# --- Inventory groups ---
@router.post("/groups", status_code=status.HTTP_201_CREATED)
async def create_group(payload: InventoryGroupCreate, db: AsyncSession = Depends(get_db)):
    group = await crud_create_group(db, payload)
    return group

@router.get("/groups", response_model=List)
async def list_groups(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    groups = await crud_list_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/groups/{group_id}")
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    group = await crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/groups/{group_id}")
async def update_group(group_id: int, payload: InventoryGroupUpdate, db: AsyncSession = Depends(get_db)):
    g = await crud_update_group(db, group_id, payload)
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    return g

@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud_delete_group(db, group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Group not found")
    return None


# --- Suppliers ---
@router.post("/suppliers", status_code=status.HTTP_201_CREATED)
async def create_supplier(payload: SupplierCreate, db: AsyncSession = Depends(get_db)):
    s = await crud_create_supplier(db, payload)
    return s

@router.get("/suppliers", response_model=List)
async def list_suppliers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    suppliers = await crud_list_suppliers(db, skip=skip, limit=limit)
    return suppliers

@router.get("/suppliers/{supplier_id}")
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    supplier = await crud_get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/suppliers/{supplier_id}")
async def update_supplier(supplier_id: int, payload: SupplierUpdate, db: AsyncSession = Depends(get_db)):
    s = await crud_update_supplier(db, supplier_id, payload)
    if not s:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return s

@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud_delete_supplier(db, supplier_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return None
