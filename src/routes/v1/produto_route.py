from typing import Any
import json

from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.services.produto_service import ProdutoService
from src.adapters.repositories import ProdutoRepository
from src.schemas.produto_schema import CreateProdutoPayload, ResponseProduto, ResponsePagination, ProdutoCategoriaParams

router = APIRouter(prefix='/produto', tags=['Produto'])

HEADERS = {
    'Content-Type': 'application/json',
    'X-Content-Type-Options': 'nosniff'
}


@router.get(
    path='/', 
    status_code=HTTPStatus.OK,
    response_model=ResponsePagination, 
    summary='Pegar todos os Produtos'
)
def paginate(repository: ProdutoRepository = Depends()):
    load = ProdutoService(repository).get_all()
    response = ResponsePagination(
        items=load,
        quantidade=len(load)
    )
    return JSONResponse(
        content=response.model_dump(),
        status_code=HTTPStatus.OK,
        headers=HEADERS
    )



@router.get(
    path='/{produto_id}',
    status_code=HTTPStatus.OK,
    response_model=ResponseProduto, 
    summary='Pegar Produto'
)
def get(produto_id: int = Path(...), repository: ProdutoRepository = Depends()):
    return ProdutoService(repository).get_by_id(produto_id)


@router.post(
    path='/', 
    status_code=HTTPStatus.CREATED,
    response_model=ResponseProduto, 
    summary='Criar Produto'
)
def create(data: CreateProdutoPayload, repository: ProdutoRepository = Depends()):
    return ProdutoService(repository).create(data=data)


@router.put(
    path='/{produto_id}',
    status_code=HTTPStatus.ACCEPTED,
    response_model=ResponseProduto, 
    summary='Atualizar Produto'
)
def update(produto_id: int = Path(...), data: CreateProdutoPayload = Body(...), repository: ProdutoRepository = Depends()):
    return ProdutoService(repository).update(produto_id, data)


@router.delete(
    path='/{produto_id}',
    status_code=HTTPStatus.ACCEPTED,
    response_model=ResponseProduto, 
    summary='Deletar Produto'
)
def delete(produto_id: int = Path(...), repository: ProdutoRepository = Depends()):
    return ProdutoService(repository).delete(produto_id)


@router.get(
    path='/categoria/{categoria}', 
    status_code=HTTPStatus.OK,
    response_model=ResponsePagination, 
    summary='Pegar Produtos por Categoria'
)
def get_by_category(
    categoria: str = Path(...), 
    repository: ProdutoRepository = Depends()
):
    return ProdutoService(repository).get_by_categoria(categoria)
