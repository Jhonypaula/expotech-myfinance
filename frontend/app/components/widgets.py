"""Pequeno kit visual usado pelas telas."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from app import config as C


def card(parent: tk.Widget, padx: int = 0, pady: int = 0, **kwargs) -> tk.Frame:
    """Frame branco com a borda padrão do app."""
    kwargs.setdefault('bg', C.SURFACE)
    f = tk.Frame(
        parent,
        highlightthickness=1,
        highlightbackground=C.HAIRLINE,
        **kwargs,
    )
    if padx or pady:
        f.configure(padx=padx, pady=pady)
    return f


def label(parent: tk.Widget, text: str = '', font_key: str = 'body',
          fg: str = C.INK, bg: str = C.SURFACE, **kwargs) -> tk.Label:
    _fonts = {
        'display_xl':  (C.FONT_DISPLAY, 20, 'bold'),
        'display_lg':  (C.FONT_DISPLAY, 16, 'bold'),
        'display':     (C.FONT_DISPLAY, 14, 'bold'),
        'display_sm':  (C.FONT_DISPLAY, 12, 'bold'),
        'body_lg':     (C.FONT_BODY, 13),
        'body':        (C.FONT_BODY, 11),
        'body_sm':     (C.FONT_BODY, 10),
        'body_bold':   (C.FONT_BODY, 11, 'bold'),
        'body_sm_bold':(C.FONT_BODY, 10, 'bold'),
        'mono':        (C.FONT_MONO, 11),
        'mono_sm':     (C.FONT_MONO, 10),
    }
    return tk.Label(parent, text=text, font=_fonts.get(font_key, (C.FONT_BODY, 11)),
                    fg=fg, bg=bg, **kwargs)


def entry(parent: tk.Widget, textvariable: tk.Variable | None = None,
          width: int = 0, **kwargs) -> tk.Entry:
    """Entry já com cores, fonte e foco do MyFinance."""
    kw = dict(
        bg=C.SURFACE, fg=C.INK,
        insertbackground=C.INK,
        highlightthickness=1,
        highlightbackground=C.HAIRLINE,
        highlightcolor=C.GREEN,
        relief='flat', bd=4,
        font=(C.FONT_BODY, 11),
    )
    kw.update(kwargs)
    e = tk.Entry(parent, textvariable=textvariable, **kw)
    if width:
        e.configure(width=width)
    return e


def button(parent: tk.Widget, text: str, command=None,
           variant: str = 'primary', size: str = 'md', **kwargs) -> tk.Button:
    """Botão padronizado; ``variant`` escolhe a intenção visual."""
    styles = {
        'primary':   {'bg': C.GREEN,    'fg': '#ffffff', 'abg': C.GREEN_700, 'afg': '#ffffff'},
        'secondary': {'bg': C.BG_2,     'fg': C.INK_2,  'abg': C.HAIRLINE,  'afg': C.INK},
        'ghost':     {'bg': C.SURFACE,  'fg': C.INK_3,  'abg': C.BG_2,      'afg': C.INK_2},
        'danger':    {'bg': C.RED_50,   'fg': C.RED,    'abg': C.RED,        'afg': '#ffffff'},
    }
    paddings = {'sm': (8, 4), 'md': (14, 7), 'lg': (18, 9)}
    s = styles.get(variant, styles['primary'])
    px, py = paddings.get(size, paddings['md'])
    font_size = {'sm': 10, 'md': 11, 'lg': 12}.get(size, 11)
    btn = tk.Button(
        parent, text=text, command=command,
        bg=s['bg'], fg=s['fg'],
        activebackground=s['abg'], activeforeground=s['afg'],
        font=(C.FONT_BODY, font_size),
        relief='flat', bd=0, cursor='hand2',
        padx=px, pady=py,
        **kwargs,
    )
    btn.bind('<Enter>', lambda e: btn.config(bg=s['abg'], fg=s['afg']))
    btn.bind('<Leave>', lambda e: btn.config(bg=s['bg'],  fg=s['fg']))
    return btn


def field_label(parent: tk.Widget, text: str, bg: str = C.SURFACE) -> tk.Label:
    lbl = tk.Label(parent, text=text, bg=bg, fg=C.INK_3,
                   font=(C.FONT_BODY, 9, 'bold'), anchor='w')
    lbl.pack(fill='x', pady=(0, 3))
    return lbl


def separator(parent: tk.Widget, bg: str = C.HAIRLINE, **kwargs) -> tk.Frame:
    return tk.Frame(parent, bg=bg, height=1, **kwargs)


def scrollable_frame(parent: tk.Widget, bg: str = C.BG) -> tuple[tk.Canvas, tk.Frame]:
    """Devolve o canvas e o frame interno para telas com listas longas."""
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0, bd=0)
    sb = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    win = canvas.create_window((0, 0), window=inner, anchor='nw')

    def _on_inner(e):
        canvas.configure(scrollregion=canvas.bbox('all'))

    def _on_canvas(e):
        canvas.itemconfig(win, width=e.width)

    def _on_wheel(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')

    inner.bind('<Configure>', _on_inner)
    canvas.bind('<Configure>', _on_canvas)
    canvas.bind_all('<MouseWheel>', _on_wheel, add='+')

    sb.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    return canvas, inner


def combobox(parent: tk.Widget, values: list, textvariable: tk.Variable | None = None,
             **kwargs) -> ttk.Combobox:
    style = ttk.Style()
    style.configure('Finance.TCombobox',
                    fieldbackground=C.SURFACE,
                    background=C.SURFACE,
                    foreground=C.INK,
                    selectbackground=C.GREEN_50,
                    selectforeground=C.INK)
    cb = ttk.Combobox(parent, values=values, textvariable=textvariable,
                      style='Finance.TCombobox', state='readonly',
                      font=(C.FONT_BODY, 11), **kwargs)
    return cb