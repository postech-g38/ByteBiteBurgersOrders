from datetime import datetime
from typing import List
import json

from src.adapters.repositories import PedidoRepository, ProdutoRepository
from src.adapters.database.models.pedido_model import PedidoModel
from src.schemas.pedido_schema import CreatePedidoPayload, ResponsePedidoPayload, CheckoutPedidoPayload, UpdatePedidoPagamentoPayload
from src.services.service_base import BaseService, try_except
from src.enums import PedidoStatus
from src.api import UsuarioApi, PagamentoApi
from src.adapters.broker.settings import AwsSQS


class PedidoService(BaseService):
    def __init__(self, pedido_repository: PedidoRepository, produto_repository: ProdutoRepository) -> None:
        self._pedido_repository = pedido_repository
        self._produto_repository = produto_repository

    def get_all(self) -> List[PedidoModel]:
        return self.query_result(self._pedido_repository.get_all())

    def get_by_id(self, pedido_id: int) -> PedidoModel:
        return self.query_result(self._pedido_repository.search_by_id(pedido_id))

    def get_by_status(self, status: str) -> PedidoModel:
        return self.query_result(self._pedido_repository.get_by_status(status.title()))

    def update(self, pedido_id: int, data: CreatePedidoPayload) -> PedidoModel:
        data_dump = data.model_dump()
        data_dump['produtos'] = json.dumps({'data': [i.model_dump() for i in data.produtos]})
        self._pedido_repository.update(pedido_id, data_dump)
        return self._pedido_repository.search_by_id(pedido_id)

    def delete(self, pedido_id: int) -> PedidoModel:
        data = self.query_result(self._pedido_repository.search_by_id(pedido_id))
        data.deleted_at = datetime.now()
        self._pedido_repository.delete(pedido_id)
        return data

    def pending_orders(self) -> List[PedidoModel]:
        rows = self.query_result(self._pedido_repository.get_pending_orders())
        return (
            sorted([i for i in rows if i.status_pedido == PedidoStatus.RECEBIDO], key=lambda x: x.created_at) +
            sorted([i for i in rows if i.status_pedido == PedidoStatus.EM_PREPARACAO], key=lambda x: x.created_at) +
            sorted([i for i in rows if i.status_pedido == PedidoStatus.PRONTO], key=lambda x: x.created_at)
        )

    @try_except
    def checkout(self, data: CheckoutPedidoPayload, usuario_api: UsuarioApi, queue: AwsSQS) -> PedidoModel:
        row = PedidoModel()
        total = 0
        usuario_id = None

        if data.usuario_documento:
            usuario = usuario_api.get_user(data.usuario_documento)
            usuario_id = usuario.get('id')

        for produto in data.produtos:
            produto_info = self.query_result(self._produto_repository.search_by_id(produto.produto_id))
            total += (produto_info.preco * produto.quantidade)

        produtos = {'data': [i.model_dump() for i in data.produtos]}

        row.valor = total
        row.status_pedido = PedidoStatus.RECEBIDO
        row.status_pagamento = 'Aguardando'
        row.data_mudanca_status = datetime.now()
        row.produtos = [i.model_dump() for i in data.produtos]

        self._pedido_repository.save(row)
        self._pedido_repository.commit()

        queue.publish({
            'metodo':'dinheiro',
            'valor': total,
            'pedido_id': row.id,
            'usuario_id': usuario_id
        })

        return ResponsePedidoPayload.model_validate(row).model_dump()
    
    def update_pagamento(self, order_id: int, payload: UpdatePedidoPagamentoPayload):
        self._pedido_repository.update(order_id, {'pagamento': payload.status})
        