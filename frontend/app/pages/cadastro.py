"""Base comum das telas internas."""
from __future__ import annotations
import tkinter as tk
from app import config as C


class BasePage(tk.Frame):
    """Frame já com o fundo padrão da área de conteúdo."""

    def __init__(self, parent: tk.Widget, bg: str = C.BG, **kwargs) -> None:
        super().__init__(parent, bg=bg, **kwargs)

    def ao_exibir(self) -> None:
        """Hook chamado quando a página volta para a frente."""