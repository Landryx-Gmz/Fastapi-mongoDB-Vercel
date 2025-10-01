from fastapi import APIRouter

router = APIRouter(prefix="/products",# con prefix hacemos que todos los endpoint sean ("/")
                    tags=["products"],#con tags= despues del prefix o prefijo hacemos que en la documentación de fastAPI lo agrupe todo del prefix
                    responses={404:{"message":"No encontado"}})#Con responses definimos el codigo de error y mensaje

products_list= ["producto 1","producto 2","producto 3","producto 4",]

@router.get("/")
async def porductos():
    return products_list


@router.get("/{id}")
async def porductos(id:int):
    return products_list[id]