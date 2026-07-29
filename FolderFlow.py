import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# ============================
# CONFIGURAÇÕES
# ============================

APP_NAME = "FolderFlow Pro"
VERSION = "1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(
    BASE_DIR,
    "assets"
)

MODULES_DIR = os.path.join(
    BASE_DIR,
    "modules"
)


LOGO_PATH = os.path.join(
    ASSETS_DIR,
    "logo.png"
)

ICON_PATH = os.path.join(
    ASSETS_DIR,
    "logo.ico"
)


BG = "#141414"
CARD = "#1E1E1E"
ACCENT = "#00C853"
TEXT = "#FFFFFF"



# ============================
# TESTE LOGO
# ============================

print("Caminho logo:")
print(LOGO_PATH)

print("Existe:")
print(os.path.exists(LOGO_PATH))



# ============================
# EXECUTAR MÓDULOS
# ============================

def executar(nome):

    arquivo = os.path.join(
        MODULES_DIR,
        nome
    )


    if not os.path.exists(arquivo):

        messagebox.showerror(
            "Erro",
            f"Arquivo não encontrado:\n\n{arquivo}"
        )

        return


    subprocess.Popen(
        [
            sys.executable,
            arquivo
        ]
    )



# ============================
# BOTÃO PERSONALIZADO
# ============================

def criar_botao(
        parent,
        texto,
        comando,
        imagem=None
):

    botao = tk.Button(
        parent,
        text=texto,
        command=comando,
        image=imagem,
        compound="left",

        bg=ACCENT,
        fg="white",

        activebackground="#18D860",
        activeforeground="white",

        bd=0,
        relief="flat",

        cursor="hand2",

        font=(
            "Segoe UI",
            11,
            "bold"
        ),

        height=2
    )


    # mantém imagem carregada
    if imagem:
        botao.image = imagem


    return botao




# ============================
# JANELA
# ============================

root = tk.Tk()

root.title(APP_NAME)

root.configure(
    bg=BG
)

root.geometry(
    "600x520"
)

root.resizable(
    False,
    False
)



# ============================
# ÍCONE DA JANELA
# ============================

if os.path.exists(ICON_PATH):

    try:

        root.iconbitmap(
            ICON_PATH
        )

    except Exception as e:

        print(e)



# ============================
# CENTRALIZAR JANELA
# ============================

root.update_idletasks()


w = 600
h = 520


ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()


x = (ws - w) // 2
y = (hs - h) // 2


root.geometry(
    f"{w}x{h}+{x}+{y}"
)




# ============================
# CARREGAR LOGO DO BOTÃO
# ============================

logo_img = None


if os.path.exists(LOGO_PATH):

    imagem_botao = Image.open(
        LOGO_PATH
    )


    imagem_botao = imagem_botao.resize(
        (25,25)
    )


    logo_img = ImageTk.PhotoImage(
        imagem_botao
    )




# ============================
# CARD PRINCIPAL
# ============================

card = tk.Frame(
    root,
    bg=CARD
)


card.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=520,
    height=450
)



# ============================
# LOGO PRINCIPAL
# ============================

if os.path.exists(LOGO_PATH):

    imagem = Image.open(
        LOGO_PATH
    )


    imagem = imagem.resize(
        (120,120)
    )


    logo_principal = ImageTk.PhotoImage(
        imagem
    )


    lbl_logo = tk.Label(
        card,
        image=logo_principal,
        bg=CARD
    )


    lbl_logo.image = logo_principal


    lbl_logo.pack(
        pady=20
    )




# ============================
# TÍTULO
# ============================

tk.Label(
    card,

    text="FolderFlow Pro",

    bg=CARD,

    fg="white",

    font=(
        "Segoe UI",
        20,
        "bold"
    )

).pack()



tk.Label(
    card,

    text="Gerador de Pastas e Excel",

    bg=CARD,

    fg="#AAAAAA",

    font=(
        "Segoe UI",
        10
    )

).pack(
    pady=(0,20)
)




# ============================
# BOTÕES
# ============================


criar_botao(
    card,

    "Gerador de Pastas",

    lambda:
    executar(
        "Gerador de Pastas.py"
    ),

    logo_img

).pack(
    fill="x",
    padx=40,
    pady=8
)



criar_botao(
    card,

    "📊 Gerador Excel",

    lambda:
    executar(
        "Gerador Excel.py"
    )

).pack(
    fill="x",
    padx=40,
    pady=8
)



criar_botao(
    card,

    "🖼 Conversor PNG → ICO",

    lambda:
    executar(
        "conversor_ico.py"
    )

).pack(
    fill="x",
    padx=40,
    pady=8
)



criar_botao(
    card,

    "❌ Sair",

    root.destroy

).pack(
    fill="x",
    padx=40,
    pady=25
)




# ============================
# RODAPÉ
# ============================

tk.Label(
    root,

    text=f"{APP_NAME}  •  Versão {VERSION}",

    bg=BG,

    fg="#888888",

    font=(
        "Segoe UI",
        9
    )

).pack(
    side="bottom",
    pady=10
)

root.mainloop()