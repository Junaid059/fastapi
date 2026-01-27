from typing import Optional
from fastapi import FastAPI, HTTPException,responses
from pydantic import BaseModel  
from psycopg2.extras import psycopg2,RealDictCursor

app = FastAPI()

class post(BaseModel):
    name: str
    price: int
    on_sale: bool = True
    inventory: Optional[int] = None

while True:
    
   try:
     conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="junaid", cursor_factory=psycopg2.extras.DictCursor)
     cursor = conn.cursor()
     print("Database connection was successful!")
     break
   except Exception as error:
     print("Connection to database failed!")
     print("Error:", error)
     
# my_posts = [{
#     "title": "First Post",
#     "content": "This is the content of the first post",
#     "id": 1,
    
#     "title": "second Post",
#     "content": "This is the content of the second post",
#     "id": 2
# }]


@app.get("/")
async def home():
    return "Hello, FastAPI!"

@app.get("/products")
def getProducts():
    cursor.execute("""select * from products""")
    products = cursor.fetchall()
    return {"data":products}

@app.post("/newProducts")
def createProduct(new_product: post):
    cursor.execute("""INSERT INTO products (name, price, on_sale, inventory) VALUES (%s, %s, %s, %s) RETURNING *""",
                   (new_product.name, new_product.price, new_product.on_sale, new_product.inventory))
    new_product = cursor.fetchone()
    conn.commit()
    return {"created_product": new_product}

@app.get("/productbyid/{id}")
async def getProductbyId(id: int):
    cursor.execute("""select * from products where id  = %s""", (str(id),))
    product = cursor.fetchone() 
    if not  product:
        raise HTTPException(status_code=404, detail={"message": "Product not found"})
    return {"productdetail":product}    
        
@app.delete("/deleteProduct/{id}")
def deletePProductbyId(id:int):
    cursor.execute("""delete from products where id = %s returning *""", (str(id),))
    deletedProduct = cursor.fetchone()
    conn.commit()
    if deletedProduct == None:
        raise HTTPException(status_code = 404,detail={"message": "Product not found"})
    
    return {"deleted_product": deletedProduct}
        
@app.put("/updateProduct/{id}")
def updateProduct(id:int, updated_product: post):
   
    cursor.execute("""update products set name = %s, price = %s, on_sale = %s, inventory = %s where id = %s returning *""",
                   (updated_product.name, updated_product.price, updated_product.on_sale, updated_product.inventory, str(id)))
    updatedProduct = cursor.fetchone()
    conn.commit()
    if updatedProduct == None:
        raise HTTPException(status_code = 404,detail={"message": "Product not found"})
    return {"updated_product": updatedProduct}