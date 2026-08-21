from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db
from backend.app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from backend.app.crud.product import (
    create_product as crud_create_product,
    get_product as crud_get_product,
    get_product_by_code as crud_get_product_by_code,
    list_products as crud_list_products,
    update_product as crud_update_product,
    delete_product as crud_delete_product,
)

router = APIRouter(tags=["products"], prefix="/products")


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    exists = await crud_get_product_by_code(db, product_in.product_code)
    if exists:
        raise HTTPException(status_code=400, detail="product_code already exists")
    product = await crud_create_product(db, product_in)
    return product

@router.get("/", response_model=List[ProductRead])
async def list_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    products = await crud_list_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud_update_product(db, product_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud_delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
