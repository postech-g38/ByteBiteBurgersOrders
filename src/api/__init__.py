from src.api.pagamento.settings import PagamentoApi
from src.api.user.settings import UsuarioApi
from src.settings import get_settings


def usuario_api_facade() -> UsuarioApi:
    return UsuarioApi(get_settings().api_settings.usuario_api_host)


def pagamento_api_facade() -> PagamentoApi:
    return PagamentoApi(get_settings().api_settings.pagamento_api_host)
