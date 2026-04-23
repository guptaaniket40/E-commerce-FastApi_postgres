from sqlalchemy.orm import Session
from . import models, schemas


# PRODUCT CRUD

def get_all_products(db: Session):
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.ProductCreate):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        return None

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price

    db.commit()
    db.refresh(existing_product)
    return existing_product


def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        return None

    db.delete(product)
    db.commit()
    return True


# CART

def create_cart(db: Session):
    cart = models.Cart()
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_to_cart(db: Session, data: schemas.AddToCartSchema):
    cart = db.query(models.Cart).filter(models.Cart.id == data.cart_id).first()
    product = db.query(models.Product).filter(models.Product.id == data.product_id).first()

    if not cart or not product:
        return None, "Cart or Product not found"

    item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product.id
    ).first()

    if item:
        item.quantity += data.quantity
    else:
        item = models.CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=data.quantity
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return item, None


def view_cart(db: Session, cart_id: int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        return None

    items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).all()

    data = []
    for item in items:
        data.append({
            "item_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "product_price": item.product.price,
            "quantity": item.quantity
        })

    return {
        "cart_id": cart.id,
        "items": data
    }


def remove_from_cart(db: Session, item_id: int):
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not item:
        return None

    if item.quantity > 1:
        item.quantity -= 1
        db.commit()
        db.refresh(item)
        return "Quantity decreased"

    db.delete(item)
    db.commit()
    return "Item removed"


# CHECKOUT

def checkout(db: Session, cart_id: int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        return None, "Cart not found"

    items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).all()

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    order = models.Order(
        cart_id=cart.id,
        total_amount=total
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # ✅ FIXED PART
    payment = models.Payment(
        order_id=order.id,
        amount=total,
        payment_status="success"
    )
    db.add(payment)
    db.commit()

    return {
        "order_id": order.id,
        "total": total,
        "payment": "success"
    }, None