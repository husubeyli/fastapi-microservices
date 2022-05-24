import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True,
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk=pk)
    
    return {
        'id': product.pk,
        'name': product.name,
        'quantity': product.quantity,
    }

@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete_product(pk: str):
    return Product.delete(pk)