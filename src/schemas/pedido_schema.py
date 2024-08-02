from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProdudoPedidoSchema(BaseModel):
    produto_id: int
    quantidade: int

    
class CreatePedidoPayload(BaseModel):
    produtos: list[ProdudoPedidoSchema]


class CheckoutPedidoPayload(CreatePedidoPayload):
    usuario_documento: Optional[str] = None
    produtos: list[ProdudoPedidoSchema]
    


class ResponsePedidoPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    status_pedido: Optional[str]
    status_pagamento: Optional[str]
    pagamento_id: Optional[str]


class ResponsePagination(BaseModel):
    items: list[ResponsePedidoPayload]
    quantidade: int


class PedidoStatusQuery(BaseModel):
    status: str


class UpdatePedidoPagamentoPayload(BaseModel):
    status: str
    