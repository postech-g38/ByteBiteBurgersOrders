from unittest.mock import Mock

import pytest

from src.services.pedido_service import PedidoService
from src.adapters.repositories.pedido_repository import PedidoRepository
from src.adapters.database.models.pedido_model import PedidoModel
from src.adapters.database.models.checkout_model import CheckoutModel
from src.services.service_base import NotFoundExcepition
from tests.resouces.database.pedido_model import PEDIDO_MODEL_LANCHE_MOCK


def test_pedido_service_get_all_then_return_pedido_list():
    # arrange
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.get_all.return_value = PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    service = PedidoService(pedido, produto)
    # act
    result = service.get_all()
    # assert
    pedido.get_all.assert_called_once()


def test_pedido_service_get_by_id_then_return_pedido_entity():
    # arrange
    pedido_id = 1
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.search_by_id.return_value = PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    service = PedidoService(pedido, produto)
    # act
    result = service.get_by_id(pedido_id)
    # assert
    pedido.search_by_id.assert_called_once_with(pedido_id)


def test_pedido_service_get_by_id_then_raise_not_found_exception():
    # arrange
    pedido_id = 1
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.search_by_id.return_value = None
    service = PedidoService(pedido, produto)
    # act
    with pytest.raises(NotFoundExcepition):
        result = service.get_by_id(pedido_id)
    # assert
    pedido.search_by_id.assert_called_once_with(pedido_id)


def test_pedido_service_get_by_status_then_return_pedido_list():
    # arrange
    pedido_status = ''
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.get_by_status.return_value = PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    service = PedidoService(pedido, produto)
    # act
    result = service.get_by_status(pedido_status)
    # assert
    pedido.get_by_status.assert_called_once_with(pedido_status)


@pytest.mark.skip
def test_pedido_service_update_then_return_pedido_entity():
    # arrange
    pedido_payload = Mock()
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.update.return_value = PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    service = PedidoService(pedido, produto)
    # act
    result = service.update(pedido_payload)
    # assert
    pedido.update.assert_called_once_with(pedido_payload)


def test_pedido_service_delete_then_return_pedido_entity():
    # arrange
    pedido_id = 1
    pedido = Mock(PedidoRepository)
    produto = Mock()
    pedido.delete.return_value = PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    service = PedidoService(pedido, produto)
    # act
    result = service.delete(pedido_id)
    # assert
    pedido.delete.assert_called_once_with(pedido_id)


def test_pedido_service_pending_orders_then_return_pedidos_list():
    # arrange
    produto = Mock()
    pedido = Mock(PedidoRepository)
    pedido.get_pending_orders.return_value = [ 
        PedidoModel(**PEDIDO_MODEL_LANCHE_MOCK)
    ]
    service = PedidoService(pedido, produto)
    # act
    result = service.pending_orders()
    # assert
    pedido.get_pending_orders.assert_called_once()


@pytest.mark.skip
def test_pedido_checkout_then_return():
    pass
