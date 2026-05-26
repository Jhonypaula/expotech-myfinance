"""Card de indicador financeiro com um gráfico pequeno."""
from __future__ import annotations
import tkinter as tk
from app import config as C
from app.utils import formatar_brl, clarear


class MetricCard(tk.Frame):
    """Mostra um KPI do dashboard com sua tendência visual."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        value: float,
        trend_text: str,
        trend_up: bool,
        spark_data: list[float],
        accent: str = C.GREEN,
        **kwargs,
    ) -> None:
        kwargs.setdefault('bg', C.SURFACE)
        super().__init__(
            parent,
            highlightthickness=1,
            highlightbackground=C.HAIRLINE,
            **kwargs,
        )
        self._accent = accent
        self._spark_data = spark_data
        self._montar(label, value, trend_text, trend_up)

    def _montar(self, label: str, value: float, trend_text: str, trend_up: bool) -> None:
        bg = self.cget('bg')
        pad = tk.Frame(self, bg=bg)
        pad.pack(fill='both', expand=True, padx=16, pady=14)

        # Cabeçalho do card.
        top = tk.Frame(pad, bg=bg)
        top.pack(fill='x')
        tk.Label(top, text=label, bg=bg, fg=C.INK_3,
                 font=(C.FONT_BODY, 10)).pack(side='left', anchor='w')

        tile = tk.Frame(top, bg=clarear(self._accent, 0.85), width=36, height=36)
        tile.pack_propagate(False)
        tile.pack(side='right')
        icon = '↑' if trend_up else '↓'
        tk.Label(tile, text=icon, bg=clarear(self._accent, 0.85), fg=self._accent,
                 font=(C.FONT_BODY, 14, 'bold')).pack(expand=True)

        # Valor principal.
        tk.Label(pad, text=formatar_brl(value), bg=bg, fg=C.INK,
                 font=(C.FONT_MONO, 20, 'bold')).pack(anchor='w', pady=(6, 2))

        # Texto curto da tendência.
        trend_fg = C.GREEN_700 if trend_up else C.RED
        trend_icon = '↗' if trend_up else '↘'
        tk.Label(pad, text=f'{trend_icon}  {trend_text}', bg=bg, fg=trend_fg,
                 font=(C.FONT_BODY, 9)).pack(anchor='w')

        # Mini gráfico no rodapé do card.
        self._canvas = tk.Canvas(self, bg=bg, height=52, highlightthickness=0, bd=0)
        self._canvas.pack(fill='x', side='bottom')
        self._canvas.bind('<Configure>', lambda e: self._desenhar_sparkline(e.width, 52))

    def _desenhar_sparkline(self, W: int, H: int) -> None:
        self._canvas.delete('all')
        data = self._spark_data
        if len(data) < 2 or W < 4:
            return

        mn, mx = min(data), max(data)
        rng = mx - mn or 1
        step = W / (len(data) - 1)
        margin = 6

        pts = [
            (i * step, H - margin - ((v - mn) / rng) * (H - margin * 2))
            for i, v in enumerate(data)
        ]

        # Preenchimento abaixo da linha para dar corpo ao gráfico.
        area = [(0, H)] + pts + [(W, H)]
        fill_color = clarear(self._accent, 0.78)
        flat = [coord for pt in area for coord in pt]
        self._canvas.create_polygon(flat, fill=fill_color, outline='')

        # Linha principal da sparkline.
        line_pts = [coord for pt in pts for coord in pt]
        self._canvas.create_line(*line_pts, fill=self._accent, width=2,
                                 smooth=True, capstyle='round', joinstyle='round')