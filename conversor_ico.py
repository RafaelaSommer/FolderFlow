import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

SIZES = [16, 32, 48, 64, 128, 256]

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

janela = tk.Tk()
janela.title("Conversor de Imagem para ICO")
janela.geometry("400x200")
janela.resizable(False, False)

titulo = tk.Label(
    janela, 
    text="Conversor de Imagem para Ícone (.ICO)", 
    font=("Arial", 12, "bold")
)
titulo.pack(pady=20)

botao = tk.Button(
    janela, 
    text="Selecionar Imagem e Converter", 
    font=("Arial", 11), 
    command=converter
)
botao.pack(pady=30)

rodape = tk.Label(
    janela, 
    text="Suporta: PNG, JPG, JPEG, BMP, GIF", 
    font=("Arial", 9)
)
rodape.pack(side="bottom", pady=10)

janela.mainloop()
