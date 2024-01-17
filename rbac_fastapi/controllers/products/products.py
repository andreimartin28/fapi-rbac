from fastapi import APIRouter

router = APIRouter(prefix='/products', tags=['products'])


@router.post('/create')
def create_products(product_name:str, product_price: float, currency_id:str, )