from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter()


# PRODUCT CRUD

@router.get("/products/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@router.post("/products/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated_product = crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Deleted"}


# CREATE CART

@router.post("/cart/create", response_model=schemas.CartCreateResponse, status_code=status.HTTP_201_CREATED)
def create_cart(db: Session = Depends(get_db)):
    cart = crud.create_cart(db)
    return {
        "message": "Cart created",
        "cart_id": cart.id
    }


# ADD TO CART

@router.post("/cart/add", status_code=status.HTTP_201_CREATED)
def add_to_cart(data: schemas.AddToCartSchema, db: Session = Depends(get_db)):
    item, error = crud.add_to_cart(db, data)
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {"message": "Added to cart"}


# VIEW CART

@router.get("/cart/{cart_id}", response_model=schemas.ViewCartResponse)
def view_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_data = crud.view_cart(db, cart_id)
    if not cart_data:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart_data


# REMOVE FROM CART

@router.delete("/cart/remove/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    result = crud.remove_from_cart(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": result}


# CHECKOUT

@router.post("/checkout", response_model=schemas.CheckoutResponse)
def checkout(data: schemas.CheckoutSchema, db: Session = Depends(get_db)):
    result, error = crud.checkout(db, data.cart_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return result