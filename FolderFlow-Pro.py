import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, funcionando no PyInstaller e no modo normal."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ============================
# CONFIGURAÇÕES
# ============================

APP_NAME = "FolderFlow Pro"
VERSION = "1.0"

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")

print(MODULES_DIR)

LOGO_PATH = resource_path("assets/logo.png")
ICON_PATH = resource_path("assets/logo.ico")

BG = "#141414"
CARD = "#1E1E1E"
ACCENT = "#00C853"
TEXT = "#FFFFFF"


# ============================
# EXECUTAR MÓDULOS
# ============================

def executar(nome):

    arquivo = os.path.join(MODULES_DIR, nome)

    if not os.path.exists(arquivo):
        messagebox.showerror(
            "Erro",
            f"Arquivo não encontrado:\n\n{arquivo}"
        )
        return

    subprocess.Popen([sys.executable, arquivo])


# ============================
# BOTÃO
# ============================

def criar_botao(parent, texto, comando):

    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=ACCENT,
        fg="white",
        activebackground="#18D860",
        activeforeground="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 11, "bold"),
        height=2
    )


# ============================
# JANELA
# ============================

root = tk.Tk()
root.title(APP_NAME)
root.configure(bg=BG)
root.geometry("600x520")
root.resizable(False, False)

if os.path.exists(LOGO_PATH):
    logo = Image.open(LOGO_PATH)
    logo = logo.resize((35,35))
    logo_img = ImageTk.PhotoImage(logo)

logo = logo.resize((35,35))

logo_img = ImageTk.PhotoImage(logo)

# ============================
# ÍCONE
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


icone = ICON_PATH

if os.path.exists(icone):
    try:
        root.iconbitmap(icone)
    except Exception as e:
        print(e)


# ============================
# CENTRALIZAR
# ============================

root.update_idletasks()

w = 600
h = 520

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws - w) // 2
y = (hs - h) // 2

root.geometry(f"{w}x{h}+{x}+{y}")


# ============================
# CARD
# ============================

card = tk.Frame(root, bg=CARD)
card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)


# ============================
# LOGO
# ============================

logo_png = LOGO_PATH

if os.path.exists(logo_png):

    imagem = Image.open(logo_png)
    imagem = imagem.resize((120,120))

    logo = ImageTk.PhotoImage(imagem)

    lbl_logo = tk.Label(
        card,
        image=logo,
        bg=CARD
    )

    lbl_logo.image = logo
    lbl_logo.pack(pady=20)


# ============================
# TÍTULO
# ============================

tk.Label(
    card,
    text="FolderFlow Pro",
    bg=CARD,
    fg="white",
    font=("Segoe UI",20,"bold")
).pack()


tk.Label(
    card,
    text="Gerador de Pastas e Excel",
    bg=CARD,
    fg="#AAAAAA",
    font=("Segoe UI",10)
).pack(pady=(0,20))


# ============================
# BOTÕES
# ============================

criar_botao(
    card,
    "📁 Gerador de Pastas",
    lambda: executar("Gerador de Pastas.py")
).pack(fill="x", padx=40, pady=8)


criar_botao(
    card,
    "📊 Gerador Excel",
    lambda: executar("Gerador Excel.py")
).pack(fill="x", padx=40, pady=8)


criar_botao(
    card,
    "🖼 Conversor PNG → ICO",
    lambda: executar("conversor_ico.py")
).pack(fill="x", padx=40, pady=8)


criar_botao(
    card,
    "❌ Sair",
    root.destroy
).pack(fill="x", padx=40, pady=25)


# ============================
# RODAPÉ
# ============================

tk.Label(
    root,
    text=f"{APP_NAME}  •  Versão {VERSION}",
    bg=BG,
    fg="#888888",
    font=("Segoe UI",9)
).pack(side="bottom", pady=10)


root.mainloop()