from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

TxType = Literal['entrada', 'saida']


@dataclass
class Transaction:
    """Movimentação financeira exibida nas telas."""
    id_transacoes: int
    conta_id: int              # conta vinculada
    categoria_id: Optional[int]  # o banco aceita nulo, mesmo que o service restrinja
    tipo_transacoes: TxType
    valor_transacoes: float
    descricao_transacoes: str
    data_transacao: str        # ISO, ex.: '2026-05-05T09:00'