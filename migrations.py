from datetime import datetime
from json import dumps

from src.adapters.database.settings import sync_engine, get_session
from src.adapters.database.models.base_model import BaseModel
from src.adapters.database.models.pedido_model import PedidoModel
from src.adapters.database.models.produto_model import ProdutoModel
from src.adapters.database.models.checkout_model import CheckoutModel


if __name__ == '__main__':
    # Para rodar o import de dados, devemos setar o ENVIRONMENT=dev e colocar as predenciais
    # do banco no .env.dev
    # rodar noterminalcomo python db.py
    BaseModel.metadata.create_all(sync_engine)

    with get_session() as session:
        session.add_all(
            (
                ProdutoModel(
                    nome='X-Burger',
                    preco= 10.99,
                    imagens='pth/to/file.png',
                    categoria='Lanche'
                ),
                ProdutoModel(
                    nome='X-Egg-Burger',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Lanche'
                ),
                ProdutoModel(
                    nome='Batata Media',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Acompanhamento'
                ),
                ProdutoModel(
                    nome='Batata Grande',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Acompanhamento'
                ),
                ProdutoModel(
                    nome='Refrigerante',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Bebida'
                ),
                ProdutoModel(
                    nome='Suco',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Bebida'
                ),
                ProdutoModel(
                    nome='Sorvete',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Sobremesa'
                ),
                ProdutoModel(
                    nome='Cookies',
                    preco=10.99,
                    imagens='pth/to/file.png',
                    categoria='Sobremesa'
                ),
            )
        )

    with get_session() as session:
        session.add_all(
            (
                PedidoModel(
                    status_pedido='Pronto',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 5, "quantidade": 1}}),
                    pagamento_id=1
                ),
                PedidoModel(
                    status_pedido='Pronto',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 4, "quantidade": 2}}),
                    pagamento_id=2
                ),
                PedidoModel(
                    status_pedido='Em preparação',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 3, "quantidade": 3}}),
                    pagamento_id=3
                ),
                PedidoModel(
                    status_pedido='Em preparação',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 1, "quantidade": 4}}),
                    pagamento_id=4
                ),
                PedidoModel(
                    status_pedido='Recebido',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 1, "quantidade": 1}}),
                    pagamento_id=5
                ),
                PedidoModel(
                    status_pedido='Recebido',
                    status_pagamento='Efetuado',
                    valor=10.99,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 1, "quantidade": 1}}),
                    pagamento_id=6
                ),
                PedidoModel(
                    status_pedido='Finalizado',
                    status_pagamento='Efetuado',
                    valor=21.98,
                    data_mudanca_status=datetime.now(),
                    produtos=dumps({'data': {"produto_id": 1, "quantidade": 1}}),
                    pagamento_id=7
                )
            )
        )
