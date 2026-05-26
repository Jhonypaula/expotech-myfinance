"""Toasts rápidos no canto da janela."""
from __future__ import annotations
import tkinter as tk
from typing import Callable
from app import config as C


_KIND_STYLES = {
    'success': {'bg': C.GREEN_50,  'fg': C.GREEN_700, 'icon': '✓'},
    'error':   {'bg': C.RED_50,    'fg': C.RED,       'icon': '✕'},
    'warning': {'bg': C.AMBER_50,  'fg': '#a16207',   'icon': '⚠'},
    'info':    {'bg': C.BLUE_50,   'fg': C.BLUE,      'icon': 'ℹ'},
}


class FlashStack:
    """Mantém a pilha de mensagens temporárias."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        # O container fica fora do fluxo do layout principal.
        self._container = tk.Frame(root, bg=root.cget('bg'))
        self._flashes: list[tk.Frame] = []
        self._reposicionar()

    def _reposicionar(self) -> None:
        self._container.place(relx=1.0, rely=0.0, anchor='ne', x=-12, y=12)

    def show(self, kind: str, message: str, duration_ms: int = 3500) -> None:
        style = _KIND_STYLES.get(kind, _KIND_STYLES['info'])
        toast = self._montar_toast(style, message)
        toast.pack(fill='x', pady=(0, 6))
        self._flashes.append(toast)
        self._root.after(duration_ms, lambda t=toast: self._dispensar(t))

    def _montar_toast(self, style: dict, message: str) -> tk.Frame:
        f = tk.Frame(
            self._container,
            bg=style['bg'],
            highlightthickness=1,
            highlightbackground=C.HAIRLINE,
            padx=12, pady=9,
        )
        inner = tk.Frame(f, bg=style['bg'])
        inner.pack(fill='x')

        tk.Label(inner, text=style['icon'], bg=style['bg'], fg=style['fg'],
                 font=(C.FONT_BODY, 11, 'bold')).pack(side='left', padx=(0, 8))
        tk.Label(inner, text=message, bg=style['bg'], fg=style['fg'],
                 font=(C.FONT_BODY, 10), wraplength=260, justify='left').pack(side='left', fill='x', expand=True)

        close = tk.Button(inner, text='✕', bg=style['bg'], fg=style['fg'],
                          bd=0, cursor='hand2', font=(C.FONT_BODY, 9),
                          activebackground=style['bg'], activeforeground=style['fg'],
                          command=lambda: self._dispensar(f))
        close.pack(side='right', padx=(8, 0))
        return f

    def _dispensar(self, toast: tk.Frame) -> None:
        try:
            toast.destroy()
            self._flashes = [f for f in self._flashes if f.winfo_exists()]
        except Exception:
            pass