from fastapi import APIRouter

router = APIRouter()

products_list= ["producto 1","producto 2","producto 3","producto 4",]

@router.get("/products")
async def porductos():
    return products_list
