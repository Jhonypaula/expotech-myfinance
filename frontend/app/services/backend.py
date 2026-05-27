from __future__ import annotations

import contextlib
import io
from datetime import datetime
from typing import Optional, Tuple

from app.models.account import Account
from app.models.category import Category
from app.models.monthly import MonthlyTotal
from app.models.transaction import Transaction
from app.models.user import User


# Funções pequenas para esconder as manias do backend antigo.


def _chamar(fn, *args, **kwargs):
    """Executa um service e transforma prints em mensagem de erro."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            return None, f"Erro interno: {e}"
    msg = buf.getvalue().strip()
    return result, msg


def _iso(value) -> str:
    """Normaliza datas do MySQL para o formato usado nas telas."""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat(timespec="minutes")
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _data_br(value) -> str:
    """Deixa a data curta o bastante para caber nos cards de conta."""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value)


# Autenticação


def login(email: str, senha: str) -> Tuple[Optional[User], str]:
    from services.auth_services import login_usuario_service

    row, msg = _chamar(login_usuario_service, email, senha)
    if not row:
        return None, msg or "Email ou senha invalidos"
    return User(
        id_usuarios=int(row[0]),
        nome_usuarios=row[1],
        email_usuarios=row[2],
    ), ""


def cadastrar(nome: str, email: str, senha: str) -> Tuple[Optional[User], str]:
    from services.auth_services import cadastrar_usuario_service

    row, msg = _chamar(cadastrar_usuario_service, nome, email, senha)
    if not row:
        return None, msg or "Nao foi possivel cadastrar"
    return User(
        id_usuarios=int(row[0]),
        nome_usuarios=row[1],
        email_usuarios=row[2],
    ), ""


# Contas


def listar_contas(usuario_id: int) -> Tuple[list[Account], str]:
    from services.conta_services import listar_contas_service

    rows, msg = _chamar(listar_contas_service, usuario_id)
    if rows is None:
        return [], msg
    return [
        Account(
            id_contas=int(r[0]),
            usuario_id=usuario_id,
            nome_contas=r[1],
            tipo_contas=r[2],
            saldo_contas=float(r[3]),
            data_criacao_contas=_data_br(r[4]) if len(r) > 4 else "",
        )
        for r in rows
    ], ""


def criar_conta(
    usuario_id: int,
    nome: str,
    tipo: str,
    saldo_inicial: float,
) -> Tuple[bool, str]:
    from services.conta_services import cadastrar_conta_service

    # O service antigo trata saldo como texto porque vinha da CLI.
    result, msg = _chamar(
        cadastrar_conta_service,
        usuario_id,
        nome,
        tipo,
        str(saldo_inicial),
    )
    if not result:
        return False, msg or "Nao foi possivel criar a conta"
    return True, ""


def editar_conta(
    usuario_id: int,
    id_conta: int,
    novo_nome: str,
    novo_tipo: str,
) -> Tuple[bool, str]:
    from services.conta_services import editar_conta_service

    result, msg = _chamar(
        editar_conta_service,
        usuario_id,
        id_conta,
        novo_nome,
        novo_tipo,
    )
    if not result:
        return False, msg or "Nao foi possivel editar a conta"
    return True, ""


def excluir_conta(usuario_id: int, id_conta: int) -> Tuple[bool, str]:
    from services.conta_services import excluir_conta_service

    result, msg = _chamar(excluir_conta_service, usuario_id, id_conta)
    if not result:
        return False, msg or "Nao foi possivel excluir a conta"
    return True, ""


# Categorias


def listar_categorias() -> Tuple[list[Category], str]:
    from services.categoria_services import listar_categorias_service

    rows, msg = _chamar(listar_categorias_service)
    if rows is None:
        return [], msg
    return [
        Category(
            id_categorias=int(r[0]),
            nome_categorias=r[1],
            descricao_categorias=r[2] or "",
        )
        for r in rows
    ], ""


# Transações


def _linha_para_transacao(row) -> Transaction:
    """Transforma a linha do SELECT no objeto usado pela interface."""
    return Transaction(
        id_transacoes=int(row[0]),
        conta_id=int(row[1]),
        categoria_id=int(row[2]) if row[2] is not None else None,
        tipo_transacoes=row[3],
        valor_transacoes=float(row[4]),
        descricao_transacoes=row[5] or "",
        data_transacao=_iso(row[6]),
    )


def listar_todas_transacoes(usuario_id: int) -> Tuple[list[Transaction], str]:
    from services.transacao_services import listar_todas_transacoes_service

    rows, msg = _chamar(listar_todas_transacoes_service, usuario_id)
    if rows is None:
        return [], msg
    return [_linha_para_transacao(r) for r in rows], ""


def criar_transacao(
    usuario_id: int,
    conta_id: int,
    categoria_id: Optional[int],
    tipo: str,
    valor: float,
    descricao: str,
) -> Tuple[bool, str]:
    from services.transacao_services import criar_transacao_service

    # A tabela aceita categoria nula, mas o service atual exige um id válido.
    # Melhor barrar aqui do que deixar o erro voltar confuso do backend.
    if categoria_id is None:
        return False, "Selecione uma categoria para a transacao"

    result, msg = _chamar(
        criar_transacao_service,
        usuario_id,
        conta_id,
        categoria_id,
        tipo,
        str(valor),
        descricao,
    )
    if not result:
        return False, msg or "Nao foi possivel criar a transacao"
    return True, ""


def editar_transacao(
    usuario_id: int,
    conta_id: int,
    id_transacao: int,
    categoria_id: Optional[int],
    tipo: str,
    valor: float,
    descricao: str,
) -> Tuple[bool, str]:
    from services.transacao_services import editar_transacao_service

    if categoria_id is None:
        return False, "Selecione uma categoria para a transacao"

    result, msg = _chamar(
        editar_transacao_service,
        usuario_id,
        conta_id,
        id_transacao,
        categoria_id,
        tipo,
        str(valor),
        descricao,
    )
    if not result:
        return False, msg or "Nao foi possivel editar a transacao"
    return True, ""


def excluir_transacao(
    usuario_id: int,
    conta_id: int,
    id_transacao: int,
) -> Tuple[bool, str]:
    from services.transacao_services import excluir_transacao_service

    result, msg = _chamar(
        excluir_transacao_service,
        usuario_id,
        conta_id,
        id_transacao,
    )
    if not result:
        return False, msg or "Nao foi possivel excluir a transacao"
    return True, ""


# Recuperação de senha


def requisicao_alterar_senha(email: str) -> Tuple[bool, str]:
    """Solicita o envio do e-mail com o token de redefinição."""
    from services.resetar_senha_service import requisicao_alterar_senha as _req

    result, msg = _chamar(_req, email)
    if result is None:
        # _chamar devolve None só em exceção; msg traz "Erro interno: ..."
        return False, msg or "Nao foi possivel enviar o e-mail"
    return True, ""


def resetar_senha(token: str, nova_senha: str) -> Tuple[bool, str]:
    """Aplica a nova senha usando o token recebido por e-mail."""
    from services.resetar_senha_service import resetar_senha as _reset

    result, msg = _chamar(_reset, token, nova_senha)
    if not result:
        return False, msg or "Token invalido ou expirado"
    return True, ""


# Dashboard


def buscar_evolucao_mensal(
    usuario_id: int,
    n_meses: int = 12,
) -> Tuple[list[MonthlyTotal], str]:
    """Busca a série mensal já agrupada; o store completa meses vazios."""
    from services.dashboard_services import buscar_evolucao_mensal_service

    rows, msg = _chamar(buscar_evolucao_mensal_service, usuario_id, n_meses)
    if rows is None:
        return [], msg
    return [
        MonthlyTotal(
            ano=int(r[0]),
            mes=int(r[1]),
            total_entradas=float(r[2] or 0),
            total_saidas=float(r[3] or 0),
        )
        for r in rows
    ], ""