import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

SIZES = [16, 32, 48, 64, 128, 256]

# =========================
# Cores Dark Mode
# =========================
BG = "#141414"          # Fundo principal (Preto)
TEXT = "#EAEAEA"        # Texto em branco/cinza claro
ACCENT = "#11C620"      # Verde para destaques e botão
ACCENT_HOVER = "#0EB21C"# Verde ao passar o mouse

# =========================
# Função para encontrar arquivos (Assets)
# =========================
def obter_caminho_asset(nome_arquivo):
    """Procura o arquivo em múltiplos caminhos possíveis."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()

    caminhos_tentativa = [
        os.path.join(base_dir, "assets", nome_arquivo),
        os.path.join(base_dir, nome_arquivo),
        os.path.join(os.getcwd(), "assets", nome_arquivo),
        os.path.join(os.getcwd(), nome_arquivo)
    ]

    for caminho in caminhos_tentativa:
        if os.path.exists(caminho):
            return caminho
    return None

def converter():
    caminho_entrada = filedialog.askopenfilename(
        title="Selecione a imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    if not caminho_entrada:
        return

    caminho_saida = filedialog.asksaveasfilename(
        defaultextension=".ico",
        filetypes=[("Ícone", "*.ico")],
        title="Salvar como"
    )

    if not caminho_saida:
        return

    try:
        img = Image.open(caminho_entrada).convert("RGBA")

        imagens = []
        for tamanho in SIZES:
            copia = img.copy()
            copia.thumbnail((tamanho, tamanho), Image.LANCZOS)
            imagens.append(copia)

        # ✅ SALVA USANDO A MAIOR IMAGEM COMO BASE
        imagens[-1].save(
            caminho_saida,
            format="ICO",
            sizes=[(s, s) for s in SIZES]
        )

        messagebox.showinfo("Sucesso", f"Ícone criado com sucesso!\n\n{caminho_saida}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter:\n{str(e)}")

# =========================
# CONFIGURAÇÃO DA JANELA
# =========================
janela = tk.Tk()
janela.title("Conversor de Imagem para ICO")
janela.geometry("420x330")
janela.configure(bg=BG)
janela.resizable(False, False)

# Centraliza a janela na tela
ws, hs = janela.winfo_screenwidth(), janela.winfo_screenheight()
x, y = (ws - 420)//2, (hs - 330)//2
janela.geometry(f"420x330+{x}+{y}")

# =========================
# LOGO E ÍCONE DA JANELA
# =========================
logo_tk = None

# Ícone da barra de título (.ico)
ico_path = obter_caminho_asset("logo.ico")
if ico_path:
    try:
        janela.iconbitmap(ico_path)
    except Exception:
        pass

# Logo grande em cima do texto (.png)
png_path = obter_caminho_asset("logo.png")
if png_path:
    try:
        imagem_logo = Image.open(png_path)
        # Redimensionado para 80x80 (ajuste se quiser maior ou menor)
        imagem_logo = imagem_logo.resize((80, 80), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(imagem_logo)
        janela.iconphoto(True, logo_tk)
    except Exception as e:
        print(f"Erro ao carregar logo.png: {e}")

# =========================
# ELEMENTOS DA INTERFACE (DARK MODE)
# =========================

# 1. Logo exibida em cima do texto (se disponível)
if logo_tk:
    lbl_logo = tk.Label(janela, image=logo_tk, bg=BG)
    lbl_logo.pack(pady=(20, 5))

# 2. Título em branco
titulo = tk.Label(
    janela, 
    text="Conversor de Imagem para Ícone (.ICO)", 
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg=TEXT
)
titulo.pack(pady=(0 if logo_tk else 25, 15))

# 3. Botão Estilizado em Verde
botao = tk.Button(
    janela, 
    text="Selecionar Imagem e Converter", 
    font=("Segoe UI", 10, "bold"), 
    bg=ACCENT,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    bd=0,
    relief="flat",
    cursor="hand2",
    command=converter
)
botao.pack(pady=15, ipadx=10, ipady=8)

# 4. Rodapé em tom cinza claro
rodape = tk.Label(
    janela, 
    text="Suporta: PNG, JPG, JPEG, BMP, GIF", 
    font=("Segoe UI", 9),
    bg=BG,
    fg="#888888"
)
rodape.pack(side="bottom", pady=15)

janela.mainloop()