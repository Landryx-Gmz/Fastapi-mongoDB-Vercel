from fastapi import APIRouter# en vez de importar a FastAPI, importamos APIRouter

router = APIRouter(prefix="/products",# con prefix hacemos que todos los endpoint sean ("/") por defecto
                    tags=["products"],#con tags= hacemos que en la documentación de fastAPI lo agrupe todo por el prefix
                    responses={404:{"message":"No encontado"}})#Con responses definimos el codigo de error y mensaje

products_list= ["producto 1","producto 2","producto 3","producto 4",]

@router.get("/")
async def porductos():
    return products_list


@router.get("/{id}")
async def porductos(id:int):
    return products_list[id]