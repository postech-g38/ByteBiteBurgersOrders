from http import HTTPStatus

from fastapi import APIRouter, Depends, Body, Path
from fastapi.responses import JSONResponse

from src.services.pedido_service import PedidoService
from src.adapters.repositories import PedidoRepository, ProdutoRepository
from src.schemas.pedido_schema import CreatePedidoPayload, ResponsePedidoPayload, ResponsePagination, CheckoutPedidoPayload, PedidoStatusQuery, UpdatePedidoPagamentoPayload
from src.schemas.base_schema import QueryPaginate
from src.api import UsuarioApi, usuario_api_facade
from src.adapters.broker import AwsSQS, aws_sqs_facade
from src.constants import HEADERS

router = APIRouter(prefix='/pedido', tags=['Pedido'])


@router.get(
    path='/', 
    response_model=ResponsePagination, 
    summary='Pegar todos os Pedidos'
)
def get_all(
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends(),
):
    response = PedidoService(pedido_repository, produto_repository).get_all()
    return {
        'items': response,
        'quantidade': len(response)
    }


@router.get(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Pegar Pedido'
)
def get(
    pedido_id: int = Path(...), 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends()
):
    data = PedidoService(pedido_repository, produto_repository).get_by_id(pedido_id)
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.OK, 
        headers=HEADERS
    )


@router.put(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Atualizar Pedido'
)
def update(
    pedido_id: int = Path(...), 
    data: CreatePedidoPayload = Body(...), 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends()
):
    data = PedidoService(pedido_repository, produto_repository).update(pedido_id, data)
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.ACCEPTED, 
        headers=HEADERS
    )


@router.delete(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Deletar Pedido'
)
def delete(
    pedido_id: int = Path(...), 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends(),
):
    data = PedidoService(pedido_repository, produto_repository).delete(pedido_id)
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.NO_CONTENT, 
        headers=HEADERS
    )


@router.get(
    path='/status/{status}', 
    response_model=ResponsePagination, 
    summary='Pegar Pedido por Status'
)
def pedido_get_by_status(
    status: str = Path(...), 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends()
):
    response = PedidoService(pedido_repository, produto_repository).get_by_status(status)
    return {
        'items': response,
        'quantidade': len(response)
    }


@router.get(
    path='/pendente', 
    response_model=ResponsePagination, 
    summary='Listagem de pedidos nao finalizados'
)
def pending_orders(
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends(),
):
    data = PedidoService(pedido_repository, produto_repository).pending_orders()
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.OK, 
        headers=HEADERS
    )


@router.post(
    path='/checkout', 
    response_model=ResponsePedidoPayload, 
    summary='Efetuar pagamento do Pedido'
)
def checkout(
    payload: CheckoutPedidoPayload, 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends(),
    usuario: UsuarioApi = Depends(usuario_api_facade),
    queue: AwsSQS = Depends(aws_sqs_facade)
):
    data = PedidoService(pedido_repository, produto_repository).checkout(payload, usuario, queue)
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.CREATED, 
        headers=HEADERS
    )


@router.put(
    path='/{pedido_id}/pagamento', 
    response_model=ResponsePedidoPayload, 
    summary='Atualizar Pedido'
)
def update_pagamento(
    pedido_id: int = Path(...), 
    data: UpdatePedidoPagamentoPayload = Body(...), 
    pedido_repository: PedidoRepository = Depends(),
    produto_repository: ProdutoRepository = Depends()
):
    data = PedidoService(pedido_repository, produto_repository).update_pagamento(pedido_id, data)
    return JSONResponse(
        content=data, 
        status_code=HTTPStatus.ACCEPTED, 
        headers=HEADERS
    )
