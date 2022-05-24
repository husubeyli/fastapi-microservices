
import os
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# the should be different databse
redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True,
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, comleted, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, backgroud_task: BackgroundTasks):  # id, quantity
    body = await request.json()
    
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product_req = req.json()
    
    order = Order(
        product_id=body['id'],
        price=product_req['price'],
        fee=0.2 * product_req['price'],
        total=1.2 * product_req['price'],
        quantity=body['quantity'],
        status='pending',
    )
    order.save()

    # change order status with task
    backgroud_task.add_task(order_completed, order)
    # order_completed(order)
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')


@app.get('/orders')
async def all():
    return [format(pk) for pk in Order.all_pks()]


def format(pk: str):
    order = Order.get(pk=pk)

    return {
        'id': order.pk,
        'product_id': order.product_id,
        'price': order.price,
        'fee': order.fee,
        'total': order.total,
        'quantity': order.quantity,
        'status': order.status,
    }
