from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Any
from scrap.parser import main, json_mng

app = FastAPI()
products_data = main()

@app.get("/")
def start_view():
    return JSONResponse(status_code=200, content={"status": "OK"})


@app.get("/all_products/")
def get_all_products() -> list[dict[str, Any]]:
    return JSONResponse(status_code=200, content=products_data)


@app.get("/products/{product_name}")
def get_product(
    product_name: str
) -> dict[str, Any]:
    for key, value in products_data.items():
        if product_name.lower() == key.lower():
            return JSONResponse(status_code=200, content={"item": value})
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
def get_product_field(
    product_name: str, 
    product_field: str
) -> dict[str, str]:
    for key, value in products_data.items():
        if product_name.lower() == key.lower():
            if product_field in value:
                return JSONResponse(status_code=200, content={"item": value[product_field]})
            raise HTTPException(status_code=404, detail="Field not found in product")
    raise HTTPException(status_code=404, detail="Product not found")