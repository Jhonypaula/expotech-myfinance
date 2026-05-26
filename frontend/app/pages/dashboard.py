"""Dashboard principal do usuário."""
from __future__ import annotations
import tkinter as tk
from typing import Callable

from app import config as C
from app.pages.base import BasePage
from app.state.store import AppStore
from app.components.metric_card import MetricCard
from app.components.tx_table import TxTable
from app.components.widgets import card, button, scrollable_frame
from app.utils import formatar_brl

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


_MONTH_LABELS = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',
]


def _texto_tendencia(curr: float, prev: float, label_prev: str) -> tuple[str, bool]:
    """Monta o texto de comparação com o mês anterior."""
    if prev == 0:
        if curr == 0:
            return f'sem variacao vs. {label_prev}', True
        return f'novo este mes vs. {label_prev}', curr > 0
    delta = (curr - prev) / abs(prev) * 100
    sign = '+' if delta >= 0 else '−'
    return f'{sign}{abs(delta):.1f}% vs. {label_prev}', delta >= 0


def _serie_saldo(monthly, saldo_atual: float) -> list[float]:
    """Reconstrói uma série aproximada de saldo olhando para trás."""
    nets = [m.total_entradas - m.total_saidas for m in monthly]
    series = [0.0] * len(nets)
    if not nets:
        return series
    # Aproximação: tratamos o saldo atual como o fechamento do mês corrente.
    series[-1] = saldo_atual
    for i in range(len(nets) - 2, -1, -1):
        # Para voltar um mês, desfazemos o movimento líquido do mês seguinte.
        series[i] = series[i + 1] - nets[i + 1]
    return series


class DashboardPage(BasePage):
    def __init__(
        self,
        parent: tk.Widget,
        store: AppStore,
        ir_transacoes: Callable[[], None],
        ir_contas: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._store   = store
        self._ir_tx   = ir_transacoes
        self._ir_contas = ir_contas
        self._montar()
        store.inscrever(self._atualizar)

    def _montar(self) -> None:
        _, self._inner = scrollable_frame(self, bg=C.BG)
        self._inner.columnconfigure(0, weight=1)
        self._atualizar()

    def _atualizar(self) -> None:
        for w in self._inner.winfo_children():
            w.destroy()

        store        = self._store
        totals       = store.totals
        accounts     = store.accounts
        transactions = store.transactions
        categories   = store.categories
        monthly      = store.monthly
        pad          = C.CONTENT_PAD

        # Cards de indicadores.
        metrics_row = tk.Frame(self._inner, bg=C.BG)
        metrics_row.pack(fill='x', padx=pad, pady=(pad, 0))
        metrics_row.columnconfigure(0, weight=1)
        metrics_row.columnconfigure(1, weight=1)
        metrics_row.columnconfigure(2, weight=1)

        # Mini gráficos usando a série mensal real do backend.
        spark_entrada = [m.total_entradas for m in monthly]
        spark_saida   = [m.total_saidas for m in monthly]
        spark_saldo   = _serie_saldo(monthly, totals['saldo'])

        # Tendências comparando mês atual com mês anterior.
        if len(monthly) >= 2:
            cur, prev = monthly[-1], monthly[-2]
            label_prev = _MONTH_LABELS[prev.mes - 1].lower()
            trend_entradas, up_e = _texto_tendencia(
                cur.total_entradas, prev.total_entradas, label_prev,
            )
            trend_saidas, _ = _texto_tendencia(
                cur.total_saidas, prev.total_saidas, label_prev,
            )
            # Saldo compara contra a estimativa do fim do mês anterior.
            saldo_prev = spark_saldo[-2] if len(spark_saldo) >= 2 else 0.0
            trend_saldo, up_s = _texto_tendencia(
                totals['saldo'], saldo_prev, label_prev,
            )
            # Para saída, cair é uma boa notícia.
            up_sa = cur.total_saidas <= prev.total_saidas
        else:
            trend_entradas = trend_saidas = trend_saldo = 'sem historico suficiente'
            up_e = up_s = True
            up_sa = False

        for col, (lbl, val, trend, up, spark, accent) in enumerate([
            ('Saldo Atual',       totals['saldo'],    trend_saldo,    up_s,  spark_saldo,   C.GREEN),
            ('Total de Entradas', totals['entradas'], trend_entradas, up_e,  spark_entrada, C.GREEN),
            ('Total de Saidas',   totals['saidas'],   trend_saidas,   up_sa, spark_saida,   C.RED),
        ]):
            mc = MetricCard(metrics_row, label=lbl, value=val,
                            trend_text=trend, trend_up=up,
                            spark_data=spark, accent=accent)
            mc.grid(row=0, column=col, sticky='nsew',
                    padx=(0 if col == 0 else 8, 0))

        # Gráfico mensal e resumo das contas.
        mid = tk.Frame(self._inner, bg=C.BG)
        mid.pack(fill='x', padx=pad, pady=(16, 0))
        mid.columnconfigure(0, weight=3)
        mid.columnconfigure(1, weight=2)

        chart_card = card(mid)
        chart_card.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        self._montar_grafico(chart_card)

        acct_card = card(mid)
        acct_card.grid(row=0, column=1, sticky='nsew')
        self._montar_painel_contas(acct_card, accounts)

        # Gastos agrupados por categoria.
        cat_card = card(self._inner)
        cat_card.pack(fill='x', padx=pad, pady=(16, 0))
        self._montar_breakdown_categorias(cat_card, transactions, categories)

        # Últimas transações.
        tx_card = card(self._inner)
        tx_card.pack(fill='x', padx=pad, pady=(16, pad))
        self._montar_transacoes_recentes(tx_card, transactions[:8], accounts, categories)

    # Blocos internos do dashboard
    def _montar_grafico(self, parent: tk.Frame) -> None:
        # Mostramos só os últimos 6 meses para o gráfico respirar.
        monthly_6 = self._store.monthly[-6:]
        months   = [_MONTH_LABELS[m.mes - 1] for m in monthly_6]
        entradas = [m.total_entradas for m in monthly_6]
        saidas   = [m.total_saidas for m in monthly_6]

        hdr = tk.Frame(parent, bg=C.SURFACE)
        hdr.pack(fill='x', padx=16, pady=(14, 0))
        tk.Label(hdr, text='Evolucao dos ultimos 6 meses', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(side='left', anchor='w')

        legend = tk.Frame(hdr, bg=C.SURFACE)
        legend.pack(side='right')
        for color, lbl in [(C.GREEN, 'Entradas'), (C.RED, 'Saidas')]:
            tk.Frame(legend, bg=color, width=8, height=8).pack(side='left', padx=(0, 3))
            tk.Label(legend, text=lbl, bg=C.SURFACE, fg=C.INK_3,
                     font=(C.FONT_BODY, 9)).pack(side='left', padx=(0, 10))

        tk.Label(parent, text='Comparativo de entradas e saidas mensais',
                 bg=C.SURFACE, fg=C.INK_4, font=(C.FONT_BODY, 9)).pack(anchor='w', padx=16)

        if _HAS_MPL:
            self._montar_grafico_mpl(parent, months, entradas, saidas)
        else:
            self._montar_grafico_fallback(parent, months, entradas, saidas)

    def _montar_grafico_mpl(
        self,
        parent: tk.Frame,
        months: list[str],
        entradas: list[float],
        saidas: list[float],
    ) -> None:
        fig = Figure(figsize=(5, 2.6), dpi=90, facecolor=C.SURFACE)
        ax  = fig.add_subplot(111)
        fig.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.12)

        x, w = list(range(len(months))), 0.35
        ax.bar([i - w/2 for i in x], entradas, w, color=C.GREEN, edgecolor='none')
        ax.bar([i + w/2 for i in x], saidas,   w, color=C.RED,   edgecolor='none')
        ax.set_xticks(x)
        ax.set_xticklabels(months, fontsize=9, color=C.INK_3)
        ax.set_facecolor(C.SURFACE)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis='both', which='both', length=0, labelcolor=C.INK_3)
        ax.yaxis.set_tick_params(labelsize=8)
        ax.grid(axis='y', color=C.HAIRLINE_2, linewidth=0.6)
        # Se os valores forem grandes, o eixo Y fica em milhares.
        max_v = max(entradas + saidas + [0])
        if max_v >= 1000:
            ax.yaxis.set_major_formatter(
                __import__('matplotlib.ticker', fromlist=['FuncFormatter'])
                .FuncFormatter(lambda v, _: f'R$ {int(v/1000)}k'))
        else:
            ax.yaxis.set_major_formatter(
                __import__('matplotlib.ticker', fromlist=['FuncFormatter'])
                .FuncFormatter(lambda v, _: f'R$ {int(v)}'))

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=(4, 12))

    def _montar_grafico_fallback(
        self,
        parent: tk.Frame,
        months: list[str],
        entradas: list[float],
        saidas: list[float],
    ) -> None:
        cv = tk.Canvas(parent, bg=C.SURFACE, height=180, highlightthickness=0)
        cv.pack(fill='x', padx=16, pady=(8, 12))

        def draw(event=None):
            cv.delete('all')
            W = cv.winfo_width() or 400
            H = 160
            bar_w = max(8, (W - 60) // (len(months) * 3))
            gap   = bar_w // 2
            max_v = max(entradas + saidas) or 1
            for i, (e, s) in enumerate(zip(entradas, saidas)):
                x0  = 40 + i * (bar_w * 2 + gap * 2 + 6)
                e_h = int((e / max_v) * H)
                s_h = int((s / max_v) * H)
                cv.create_rectangle(x0, H - e_h, x0 + bar_w, H, fill=C.GREEN, outline='')
                cv.create_rectangle(x0 + bar_w + gap, H - s_h,
                                    x0 + bar_w * 2 + gap, H, fill=C.RED, outline='')
                cv.create_text(x0 + bar_w, H + 12, text=months[i],
                               fill=C.INK_3, font=(C.FONT_BODY, 8))
        cv.bind('<Configure>', draw)

    def _montar_painel_contas(self, parent: tk.Frame, accounts) -> None:
        hdr = tk.Frame(parent, bg=C.SURFACE)
        hdr.pack(fill='x', padx=16, pady=(14, 8))
        tk.Label(hdr, text='Minhas Contas', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(side='left')
        button(hdr, 'Gerenciar', command=self._ir_contas,
               variant='secondary', size='sm').pack(side='right')
        tk.Label(hdr, text=f'{len(accounts)} contas ativas', bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 9)).pack(side='left', padx=(6, 0))

        _ICON = {'corrente': '🏦', 'poupanca': '🐷', 'carteira': '👛'}
        for a in accounts:
            row = tk.Frame(parent, bg=C.SURFACE)
            row.pack(fill='x', padx=16, pady=4)

            icon_f = tk.Frame(row, bg=C.GREEN_50, width=36, height=36)
            icon_f.pack_propagate(False)
            icon_f.pack(side='left')
            tk.Label(icon_f, text=_ICON.get(a.tipo_contas, '💳'),
                     bg=C.GREEN_50, font=(C.FONT_BODY, 14)).pack(expand=True)

            meta = tk.Frame(row, bg=C.SURFACE)
            meta.pack(side='left', padx=(10, 0), fill='x', expand=True)
            tk.Label(meta, text=a.nome_contas, bg=C.SURFACE, fg=C.INK,
                     font=(C.FONT_BODY, 11, 'bold')).pack(anchor='w')
            tk.Label(meta, text=a.tipo_contas, bg=C.SURFACE, fg=C.INK_4,
                     font=(C.FONT_BODY, 9)).pack(anchor='w')

            bal_fg = C.GREEN_700 if a.saldo_contas >= 0 else C.RED
            tk.Label(row, text=formatar_brl(a.saldo_contas), bg=C.SURFACE, fg=bal_fg,
                     font=(C.FONT_MONO, 11, 'bold')).pack(side='right')

        tk.Frame(parent, bg=C.SURFACE, height=12).pack()

    def _montar_breakdown_categorias(self, parent: tk.Frame, transactions, categories) -> None:
        saidas = [t for t in transactions if t.tipo_transacoes == 'saida']

        totals: dict = {}
        for tx in saidas:
            key = tx.categoria_id
            totals[key] = totals.get(key, 0) + tx.valor_transacoes

        cat_map  = {c.id_categorias: c.nome_categorias for c in categories}
        ranked   = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:5]
        total_sp = sum(totals.values()) or 1
        max_val  = ranked[0][1] if ranked else 1

        hdr = tk.Frame(parent, bg=C.SURFACE)
        hdr.pack(fill='x', padx=16, pady=(14, 4))
        tk.Label(hdr, text='Gastos por categoria', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(side='left')
        tk.Label(hdr,
                 text=f'top {len(ranked)} · total {formatar_brl(sum(totals.values()))}',
                 bg=C.SURFACE, fg=C.INK_4, font=(C.FONT_BODY, 9)).pack(side='left', padx=(8, 0))

        if not ranked:
            tk.Label(parent, text='Nenhuma despesa registrada.',
                     bg=C.SURFACE, fg=C.INK_3,
                     font=(C.FONT_BODY, 10)).pack(anchor='w', padx=16, pady=(0, 16))
            return

        body = tk.Frame(parent, bg=C.SURFACE)
        body.pack(fill='x', padx=16, pady=(4, 16))

        _COLORS = [C.GREEN, C.BLUE, C.AMBER, '#8e44ad', '#1abc9c']

        for i, (cat_id, val) in enumerate(ranked):
            cat_name = cat_map.get(cat_id, 'Sem categoria') if cat_id else 'Sem categoria'
            pct      = val / total_sp * 100
            ratio    = val / max_val
            color    = _COLORS[i % len(_COLORS)]

            row = tk.Frame(body, bg=C.SURFACE)
            row.pack(fill='x', pady=(0, 8))

            tk.Label(row, text=cat_name, bg=C.SURFACE, fg=C.INK,
                     font=(C.FONT_BODY, 10), width=14, anchor='w').pack(side='left')

            bar_cv = tk.Canvas(row, bg=C.BG_2, height=10,
                               highlightthickness=0, bd=0)
            bar_cv.pack(side='left', fill='x', expand=True, padx=(0, 12))

            def _redraw(e, cv=bar_cv, r=ratio, c=color):
                cv.delete('all')
                w = max(1, cv.winfo_width())
                cv.create_rectangle(0, 1, max(4, int(w * r)), 9, fill=c, outline='')

            bar_cv.bind('<Configure>', _redraw)

            tk.Label(row, text=formatar_brl(val), bg=C.SURFACE, fg=C.INK,
                     font=(C.FONT_MONO, 10, 'bold'), anchor='e', width=13).pack(side='left')
            tk.Label(row, text=f'{pct:.0f}%', bg=C.SURFACE, fg=C.INK_4,
                     font=(C.FONT_BODY, 9), anchor='e', width=4).pack(side='left')

    def _montar_transacoes_recentes(self, parent, transactions, accounts, categories) -> None:
        hdr = tk.Frame(parent, bg=C.SURFACE)
        hdr.pack(fill='x', padx=16, pady=(14, 0))
        tk.Label(hdr, text='Últimas Transações', bg=C.SURFACE, fg=C.INK,
                 font=(C.FONT_DISPLAY, 13, 'bold')).pack(side='left')
        button(hdr, 'Ver todas →', command=self._ir_tx,
               variant='secondary', size='sm').pack(side='right')
        tk.Label(hdr, text='Atividade financeira mais recente (últimas 8 transações)', bg=C.SURFACE, fg=C.INK_4,
                 font=(C.FONT_BODY, 9)).pack(side='left', padx=(6, 0))

        tbl = TxTable(parent)
        tbl.pack(fill='both', expand=True, pady=(8, 0))
        tbl.load(transactions, accounts, categories)

    def ao_exibir(self) -> None:
        self._atualizar()