"""Formatação de dinheiro, datas e cores."""
from __future__ import annotations
from datetime import datetime
import tkinter as tk


def formatar_brl(amount: float) -> str:
    """Formata um valor no padrão brasileiro."""
    sign = '−' if amount < 0 else ''
    formatted = f'{abs(amount):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'{sign}R$ {formatted}'


def formatar_brl_com_sinal(amount: float) -> str:
    sign = '+' if amount >= 0 else '−'
    formatted = f'{abs(amount):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'{sign}R$ {formatted}'


def formatar_data(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return iso_str


def formatar_data_curta(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime('%d/%m')
    except ValueError:
        return iso_str


def aplicar_mascara_data(var: tk.StringVar) -> None:
    """Mantém o conteúdo de *var* no formato dd/mm/aaaa enquanto o usuário digita.

    Aceita só dígitos (até 8) e insere as barras nas posições corretas.
    Letras e caracteres inválidos são descartados silenciosamente.
    Pode ser passada como callback de ``trace_add``::

        var.trace_add('write', lambda *_: aplicar_mascara_data(var))
    """
    raw    = var.get()
    digits = ''.join(c for c in raw if c.isdigit())[:8]

    partes: list[str] = []
    if digits[:2]:
        partes.append(digits[:2])
    if digits[2:4]:
        partes.append(digits[2:4])
    if digits[4:8]:
        partes.append(digits[4:8])
    formatado = '/'.join(partes)

    # Só atualiza se mudou, evitando recursão infinita no trace.
    if formatado != raw:
        var.set(formatado)


def parsear_data(value: str) -> tuple['datetime | None', bool]:
    """Converte *value* (dd/mm/aaaa) em datetime.

    Devolve ``(datetime, True)`` se válido, ``(None, True)`` se vazio,
    ou ``(None, False)`` se o texto não bate com o formato esperado.
    """
    v = value.strip()
    if not v:
        return None, True
    try:
        return datetime.strptime(v, '%d/%m/%Y'), True
    except ValueError:
        return None, False


def clarear(hex_color: str, amount: float) -> str:
    """Mistura a cor com branco; 0 mantém, 1 vira branco."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    return f'#{r:02x}{g:02x}{b:02x}'


def escurecer(hex_color: str, amount: float) -> str:
    """Mistura a cor com preto; 0 mantém, 1 vira preto."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return f'#{r:02x}{g:02x}{b:02x}'