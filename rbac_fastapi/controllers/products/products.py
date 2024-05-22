from fastapi import APIRouter, HTTPException, status, File, UploadFile
from libraries.validations import product_name_validation, float_number, currency_ron_euro
from configs.db import db
import shutil
import uuid


router = APIRouter(prefix='/products', tags=['products'])


@router.post('/create')
def create_products(product_name: str,
                    product_price: float,
                    currency_id: int,
                    product_photo: UploadFile = File(...)
                    ):
    """
    currency_id: \n
    1 = RON \n
    2 = EUR
    """
    if not product_name_validation(product_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The product name format is not valid")
    if not float_number(product_price):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The product price format is not valid.")
    if not currency_ron_euro(currency_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The currency_id should be 1 = RON or 2 = EURO. " +
            "Choose beetween them. Other values are not accepted."
        )
    db_check = db.select('''select product_id, product_name from rbac_fastapi.products where product_name='{0}' '''.format(product_name))
    if db_check is not None:
        product_name_in_db = db_check['product_name']
        if product_name == product_name_in_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The product already exists " +
                                "in the database")
    photo_uuid = str(uuid.uuid4().hex)
    file_extension = product_photo.filename.split(".")[-1]
    photo_renamed = f"{photo_uuid}.{file_extension}"
    path = f'files/{photo_renamed}'
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(product_photo.file, buffer)
    db.select(''' insert into rbac_fastapi.products (product_name, product_photo, product_price, currency_id) values ("{0}", "{1}", "{2}", "{3}")'''.format(product_name, photo_renamed, product_price, currency_id))
    product = db.select('''select * from rbac_fastapi.products where product_name='{0}' '''.format(product_name))
    return {
        "message": "The product has been created successfully " +
        "with the following data",
        "product_id": product['product_id'],
        "product_name": product['product_name'],
        "product_photo": product['product_photo'],
        "product_price": product['product_price'],
        "currency_id": product['currency_id']
        }


@router.get('/all',
            summary='Retrieve all the existent products from the database',
            description='Click on execute to get the data',
            response_description='All the products existent')
def get_all_products():
    all_products_data = db.select(
        ''' select p.product_id, p.product_name, p.product_photo, p.product_price, c.currency_name
        from rbac_fastapi.products p
        left join rbac_fastapi.currencies c
        on p.currency_id = c.currency_id; ''', selectOnce=False)
    if not all_products_data:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No products found")
    products_list = [
        {
            "product_id": product['product_id'],
            "product_name": product['product_name'],
            "product_photo": product['product_photo'],
            "product_price": product['product_price'],
            "currency_name": product['currency_name']
        }
        for product in all_products_data
    ]
    return {"products": products_list}


@router.get('/{product_id}')
def get_specific_product(product_id: int):

    check_product_existence = db.select('''select product_id from products
                                            where product_id = {0};'''.format(product_id))
    if check_product_existence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The with the product_id = {product_id}" +
                            " does not exist in the database")

    product = db.select('''select * from rbac_fastapi.products p
                            left join rbac_fastapi.currencies c
                            on p.currency_id = c.currency_id
                            where product_id={0} '''.format(product_id))
    return {
        "product_id": product['product_id'],
        "product_name": product['product_name'],
        "product_photo": product['product_photo'],
        "product_price": product['product_price'],
        "currency": product['currency_name']
    }


@router.put('/{product_id}')
def update_product(product_id: int,
                   product_name: str,
                   product_price: float,
                   currency_id: int,
                   product_photo: UploadFile = File(...)
                   ):
    '''
    currency_id: \n
    1 = RON \n
    2 = EUR
    '''
    if not product_name_validation(product_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The product name format is not valid")
    db_check = db.select('''select product_id, product_name from rbac_fastapi.products where product_name='{0}' '''.format(product_name))
    if db_check is not None:
        product_name_in_db = db_check['product_name']
        if product_name == product_name_in_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The product already exists " +
                                "in the database")
    photo_uuid = str(uuid.uuid4().hex)
    file_extension = product_photo.filename.split(".")[-1]
    photo_renamed = f"{photo_uuid}.{file_extension}"
    path = f'files/{photo_renamed}'
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(product_photo.file, buffer)
    db.update('''update rbac_fastapi.products set product_name ='{0}', product_photo='{1}', product_price='{2}', currency_id='{3}' where product_id='{4}' '''.format(product_name, photo_renamed, product_price, currency_id, product_id))
    updated_product = db.select('''select * from rbac_fastapi.products where product_id = {0}'''.format(product_id))
    return {
        "updated_product": {
                            "product_id": updated_product['product_id'],
                            "product_name": updated_product['product_name'],
                            "product_photo": updated_product['product_photo'],
                            "product_price": updated_product['product_price'],
                            "currency_id": updated_product['currency_id']
                            }
            }


@router.delete('/{product_id}')
def delete_product(product_id: int):
    check_product_existence = db.select('''select product_id from products
                                            where product_id = {0};'''.format(product_id))
    if check_product_existence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The product with the product_id= {product_id} " +
                                    "it's not in the database or it was already deleted")
    db.delete('''delete from rbac_fastapi.products where product_id='{0}'; '''.format(product_id))
    return {
            "data_info": f"The product with product_id = {product_id} has " +
            "been deleted successfully!"
    }
