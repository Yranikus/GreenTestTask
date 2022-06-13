from typing import List
from fastapi import File
from fastapi import APIRouter
from fastapi import Depends

from .secure import get_current_user
from ..DTO import tables
from ..service.del_and_get_img import DeleteAndGetService
from ..service.save_img import SaveService

router = APIRouter(
    prefix="/frames"
)

@router.post('/')
async def save(saveservice: SaveService = Depends(), user: tables.User = Depends(get_current_user),
         files: List[bytes] = File()):
    return saveservice.save(files)

@router.get('/{code}')
async def get(code: str, deleteAndGetService: DeleteAndGetService = Depends(), user: tables.User = Depends(get_current_user) ):
    return deleteAndGetService.get(code)

@router.delete('/{code}')
async def delete(code: str, deleteAndGetService: DeleteAndGetService = Depends(), user: tables.User = Depends(get_current_user) ):
    return deleteAndGetService.delete(code)