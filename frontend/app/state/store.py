from __future__ import annotations

from datetime import date
from typing import Callable, List, Optional, Tuple

from app.models.account import Account
from app.models.category import Category
from app.models.monthly import MonthlyTotal
from app.models.transaction import Transaction
from app.models.user import User
from app.services import backend


_MONTHLY_WINDOW = 12  # janela usada nos gráficos do dashboard


_PLACEHOLDER_USER = User(
    id_usuarios=0,
    nome_usuarios="",
    email_usuarios="",
)


class AppStore:
    def __init__(self) -> None:
        self._user: User = _PLACEHOLDER_USER
        self._accounts: List[Account] = []
        self._transactions: List[Transaction] = []
        self._categories: List[Category] = []
        self._monthly: List[MonthlyTotal] = []
        self._listeners: List[Callable[[], None]] = []

    # Assinaturas das telas
    def inscrever(self, callback: Callable[[], None]) -> None:
        self._listeners.append(callback)

    def desinscrever(self, callback: Callable[[], None]) -> None:
        self._listeners = [l for l in self._listeners if l is not callback]

    def _notificar(self) -> None:
        for cb in self._listeners:
            try:
                cb()
            except Exception:
                pass

    # Sessão
    def esta_autenticado(self) -> bool:
        return self._user.id_usuarios > 0

    def inicializar(self, user: User) -> str:
        """Guarda o usuário logado e faz a primeira carga de dados."""
        self._user = user

        accounts, err_a = backend.listar_contas(user.id_usuarios)
        categories, err_c = backend.listar_categorias()
        transactions, err_t = backend.listar_todas_transacoes(user.id_usuarios)
        monthly, err_m = backend.buscar_evolucao_mensal(
            user.id_usuarios, _MONTHLY_WINDOW
        )

        self._accounts = accounts
        self._categories = categories
        self._transactions = transactions
        self._monthly = monthly
        self._notificar()

        return err_a or err_c or err_t or err_m

    def sair(self) -> None:
        self._user = _PLACEHOLDER_USER
        self._accounts = []
        self._transactions = []
        self._categories = []
        self._monthly = []
        self._notificar()

    # Leitura
    @property
    def user(self) -> User:
        return self._user

    @property
    def accounts(self) -> List[Account]:
        return list(self._accounts)

    @property
    def transactions(self) -> List[Transaction]:
        return list(self._transactions)

    @property
    def categories(self) -> List[Category]:
        return list(self._categories)

    @property
    def monthly(self) -> List[MonthlyTotal]:
        """Série mensal contínua, pronta para o gráfico."""
        return self._preencher_serie_mensal(_MONTHLY_WINDOW)

    @property
    def totals(self) -> dict:
        entradas = sum(
            t.valor_transacoes for t in self._transactions
            if t.tipo_transacoes == 'entrada'
        )
        saidas = sum(
            t.valor_transacoes for t in self._transactions
            if t.tipo_transacoes == 'saida'
        )
        saldo = sum(a.saldo_contas for a in self._accounts)
        return {'entradas': entradas, 'saidas': saidas, 'saldo': saldo}

    # Buscas rápidas em memória
    def buscar_conta(self, id_contas: int) -> Optional[Account]:
        return next(
            (a for a in self._accounts if a.id_contas == id_contas),
            None,
        )

    def buscar_categoria(self, id_categorias: Optional[int]) -> Optional[Category]:
        if id_categorias is None:
            return None
        return next(
            (c for c in self._categories if c.id_categorias == id_categorias),
            None,
        )

    def nome_categoria(self, id_categorias: Optional[int]) -> str:
        cat = self.buscar_categoria(id_categorias)
        return cat.nome_categorias if cat else '—'

    # Recargas pontuais
    def _recarregar_contas(self) -> None:
        rows, _ = backend.listar_contas(self._user.id_usuarios)
        self._accounts = rows

    def _recarregar_transacoes(self) -> None:
        rows, _ = backend.listar_todas_transacoes(self._user.id_usuarios)
        self._transactions = rows
        # Qualquer transação mexe no gráfico mensal.
        monthly, _ = backend.buscar_evolucao_mensal(
            self._user.id_usuarios, _MONTHLY_WINDOW
        )
        self._monthly = monthly

    def _preencher_serie_mensal(self, n_months: int) -> List[MonthlyTotal]:
        """Completa os meses que o backend não retorna porque não tiveram movimento."""
        today = date.today()
        by_key = {(m.ano, m.mes): m for m in self._monthly}

        series: List[MonthlyTotal] = []
        for i in range(n_months - 1, -1, -1):
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
            series.append(
                by_key.get(
                    (year, month),
                    MonthlyTotal(
                        ano=year,
                        mes=month,
                        total_entradas=0.0,
                        total_saidas=0.0,
                    ),
                )
            )
        return series

    # Contas
    def criar_conta(
        self,
        nome: str,
        tipo: str,
        saldo_inicial: float,
    ) -> Tuple[bool, str]:
        ok, msg = backend.criar_conta(
            self._user.id_usuarios,
            nome,
            tipo,
            saldo_inicial,
        )
        if ok:
            self._recarregar_contas()
            self._notificar()
        return ok, msg

    def excluir_conta(self, id_contas: int) -> Tuple[bool, str]:
        ok, msg = backend.excluir_conta(self._user.id_usuarios, id_contas)
        if ok:
            self._recarregar_contas()
            self._notificar()
        return ok, msg

    # Transações
    def criar_transacao(
        self,
        conta_id: int,
        categoria_id: Optional[int],
        tipo: str,
        valor: float,
        descricao: str,
    ) -> Tuple[bool, str]:
        ok, msg = backend.criar_transacao(
            self._user.id_usuarios,
            conta_id,
            categoria_id,
            tipo,
            valor,
            descricao,
        )
        if ok:
            # O saldo é recalculado no backend, então trazemos contas de novo.
            self._recarregar_transacoes()
            self._recarregar_contas()
            self._notificar()
        return ok, msg

    def atualizar_transacao(
        self,
        id_transacao: int,
        conta_id: int,
        categoria_id: Optional[int],
        tipo: str,
        valor: float,
        descricao: str,
    ) -> Tuple[bool, str]:
        ok, msg = backend.editar_transacao(
            self._user.id_usuarios,
            conta_id,
            id_transacao,
            categoria_id,
            tipo,
            valor,
            descricao,
        )
        if ok:
            self._recarregar_transacoes()
            self._recarregar_contas()
            self._notificar()
        return ok, msg

    def excluir_transacao(
        self,
        id_transacao: int,
        conta_id: int,
    ) -> Tuple[bool, str]:
        ok, msg = backend.excluir_transacao(
            self._user.id_usuarios,
            conta_id,
            id_transacao,
        )
        if ok:
            self._recarregar_transacoes()
            self._recarregar_contas()
            self._notificar()
        return ok, msg