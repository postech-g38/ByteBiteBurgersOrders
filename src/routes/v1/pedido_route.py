from fastapi import APIRouter, Depends, Response, Request, Query, Body, Path

from src.services.pedido_service import PedidoService
from src.adapters.repositories import PedidoRepository
from src.schemas.pedido_schema import CreatePedidoPayload, ResponsePedidoPayload, ResponsePagination, CheckoutPedidoPayload, PedidoStatusQuery
from src.schemas.base_schema import QueryPaginate
from src.api import UsuarioApi, PagamentoApi, usuario_api_facade, pagamento_api_facade

router = APIRouter(prefix='/pedido', tags=['Pedido'])


@router.get(
    path='/', 
    response_model=ResponsePagination, 
    summary='Pegar todos os Pedidos'
)
def get_all(repository: PedidoRepository = Depends()):
    response = PedidoService(repository).get_all()
    return {
        'items': response,
        'quantidade': len(response)
    }


@router.get(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Pegar Pedido'
)
def get(pedido_id: int = Path(...), repository: PedidoRepository = Depends()):
    return PedidoService(repository).get_by_id(pedido_id)


@router.put(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Atualizar Pedido'
)
def update(pedido_id: int = Path(...), data: CreatePedidoPayload = Body(...), repository: PedidoRepository = Depends()):
    return PedidoService(repository).update(pedido_id, data)


@router.delete(
    path='/{pedido_id}', 
    response_model=ResponsePedidoPayload, 
    summary='Deletar Pedido'
)
def delete(pedido_id: int = Path(...), repository: PedidoRepository = Depends()):
    return PedidoService(repository).delete(pedido_id)


@router.get(
    path='/status', 
    response_model=ResponsePagination, 
    summary='Pegar Pedido por Status'
)
def pedido_get_by_status(status: str = Query(...), repository: PedidoRepository = Depends()):
    return PedidoService(repository).get_by_status(status)


@router.get(
    path='/pendente', 
    response_model=ResponsePagination, 
    summary='Listagem de pedidos nao finalizados'
)
def pending_orders(repository: PedidoRepository = Depends()):
    return PedidoService(repository).pending_orders()


@router.post(
    path='/checkout', 
    response_model=ResponsePedidoPayload, 
    summary='Efetuar pagamento do Pedido'
)
def checkout(
    payload: CheckoutPedidoPayload, 
    repository: PedidoRepository = Depends(),
    usuario: UsuarioApi = Depends(usuario_api_facade),
    pagamento: PagamentoApi = Depends(pagamento_api_facade)
    ):
    return PedidoService(repository).checkout(payload, usuario, pagamento)
