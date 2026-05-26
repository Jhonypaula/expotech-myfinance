from __future__ import annotations

import tkinter as tk

# Tem que rodar ANTES de qualquer "from app.services... import backend"
from app.services.backend_path import instalar as install_backend_path
install_backend_path()

from app.application import Application  # noqa: E402  (depende do sys.path acima)


def main() -> None:
    root = tk.Tk()

    # Melhora a nitidez em monitores HiDPI no Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()