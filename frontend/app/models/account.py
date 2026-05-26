from dataclasses import dataclass
from typing import Literal

AccountType = Literal['corrente', 'poupanca', 'carteira']


@dataclass
class Account:
    """Conta bancária vinda de tbl_contas."""
    id_contas: int
    usuario_id: int          # dono da conta
    nome_contas: str
    tipo_contas: AccountType
    saldo_contas: float
    data_criacao_contas: str  # já formatada para exibição