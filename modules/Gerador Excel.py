import os
import openpyxl
from openpyxl.styles import Font, Border, Side
from openpyxl.utils import get_column_letter
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog # <-- IMPORTAÇÃO ADICIONADA AQUI
from PIL import Image, ImageTk

# ---------------------------- TEMA VISUAL ---------------------------- #
BG = "#1e1e1e"
CARD = "#2b2b2b"
INPUT_BG = "#3a3a3a"
TEXT = "#f0f0f0"
ACCENT = "#6C63FF"
ACCENT_HOVER = "#827CFF"
BTN_BG = "#6C63FF"
BTN_FG = "white"

def styled_button(master, text, command):
    btn = tk.Button(master, text=text, command=command,
                    bg=BTN_BG, fg=BTN_FG, activebackground=ACCENT_HOVER,
                    activeforeground="white", relief="flat",
                    font=("Segoe UI", 11, "bold"), bd=0)
    return btn

# ---------------------------- UTIL ---------------------------- #
def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    ws = janela.winfo_screenwidth()
    hs = janela.winfo_screenheight()
    x = (ws - largura) // 2
    y = (hs - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

entradas_celulas = []

# ---------------------------- LÓGICA ---------------------------- #
def criar_grade():
    global entradas_celulas

    if 'frame_grade' not in globals():
        messagebox.showerror("Erro interno", "frame_grade não encontrado. Reinicie a aplicação.")
        return

    for widget in frame_grade.winfo_children():
        widget.destroy()
    entradas_celulas = []

    try:
        n_colunas = int(entry_colunas.get())
        n_linhas = int(entry_linhas.get())
        if n_colunas <= 0 or n_linhas <= 0:
            raise ValueError
    except:
        messagebox.showerror("Erro", "Digite números válidos maiores que zero.")
        return

    altura_ajustada = 320 + (n_linhas + 1) * 30
    if altura_ajustada > 700:
        altura_ajustada = 700
    centralizar_janela(root, 900, altura_ajustada)

    for r in range(n_linhas + 1):
        linha_entradas = []
        for c in range(n_colunas):
            e = tk.Entry(frame_grade, width=18, justify='center',
                          font=("Segoe UI", 10), bg=INPUT_BG, fg=TEXT,
                          insertbackground="white", relief="flat")
            e.grid(row=r, column=c, padx=4, pady=4, ipady=6, sticky="nsew")
            if r == 0:
                e.config(font=("Segoe UI", 10, "bold"), bg="#4b4b4b")
            linha_entradas.append(e)
        entradas_celulas.append(linha_entradas)

    for c in range(n_colunas):
        frame_grade.grid_columnconfigure(c, weight=1)


def ajustar_largura_colunas(ws, dados):
    if not dados or not dados[0]:
        return
    for col_idx in range(len(dados[0])):
        max_length = 0
        for row in dados:
            if row[col_idx]:
                max_length = max(max_length, len(str(row[col_idx])))
        ws.column_dimensions[get_column_letter(col_idx + 1)].width = min(max_length + 2, 50)


# Função 'obter_caminho_desktop' REMOVIDA, pois não é mais necessária com filedialog

def gerar_excel():
    global entradas_celulas
    if not entradas_celulas:
        messagebox.showerror("Erro", "Crie a grade antes de gerar o arquivo.")
        return

    n_linhas = len(entradas_celulas) - 1
    n_colunas = len(entradas_celulas[0])

    dados = []
    for r in range(n_linhas + 1):
        linha = []
        for c in range(n_colunas):
            valor = entradas_celulas[r][c].get().strip()
            if r == 0 and valor == "":
                messagebox.showerror("Erro", "Todos os nomes das colunas devem ser preenchidos.")
                return
            linha.append(valor)
        dados.append(linha)

    # AQUI ESTÁ A MUDANÇA PRINCIPAL: Usa a caixa de diálogo para salvar
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Arquivos Excel", "*.xlsx")],
        title="Salvar arquivo Excel como...",
        initialfile="Planilha.xlsx" 
    )

    if not caminho_arquivo:
        # Usuário cancelou a operação
        return
    # ---------------------------------------------------------- #

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Planilha Personalizada"

        for linha in dados:
            ws.append(linha)

        for col in range(1, n_colunas + 1):
            ws.cell(row=1, column=col).font = Font(bold=True)

        thin = Border(left=Side(style='thin'), right=Side(style='thin'),
                      top=Side(style='thin'), bottom=Side(style='thin'))

        for r in range(1, n_linhas + 2):
            for c in range(1, n_colunas + 1):
                ws.cell(row=r, column=c).border = thin

        ajustar_largura_colunas(ws, dados)
        wb.save(caminho_arquivo)

    except Exception as err:
        messagebox.showerror("Erro ao salvar", str(err))
        return

    messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{caminho_arquivo}")

# ---------------------------- INTERFACE ---------------------------- #
root = tk.Tk()
root.title("Gerador de Excel")
root.configure(bg=BG)
centralizar_janela(root, 520, 360)
root.resizable(True, True)

# Logo opcional (mantido como estava)
try:
    caminho_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    if os.path.exists(caminho_logo):
        img = Image.open(caminho_logo).resize((72, 72))
        logo_tk = ImageTk.PhotoImage(img)
        tk.Label(root, image=logo_tk, bg=BG).pack(pady=8)
        root.iconphoto(True, logo_tk)
except:
    pass

frame_config = tk.Frame(root, bg=CARD, highlightbackground="#3a3a3a", highlightthickness=1)
frame_config.pack(padx=20, pady=8, fill="x")

frame_inputs = tk.Frame(frame_config, bg=CARD)
frame_inputs.pack(pady=12)

tk.Label(frame_inputs, text="Número de colunas:", bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=18)
entry_colunas = tk.Entry(frame_inputs, width=12, bg=INPUT_BG, fg=TEXT, relief="flat")
entry_colunas.grid(row=1, column=0, padx=18)

tk.Label(frame_inputs, text="Número de linhas:", bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=18)
entry_linhas = tk.Entry(frame_inputs, width=12, bg=INPUT_BG, fg=TEXT, relief="flat")
entry_linhas.grid(row=1, column=1, padx=18)

# -------- BOTÕES LADO A LADO -------- #
frame_botoes = tk.Frame(frame_config, bg=CARD)
frame_botoes.pack(pady=10)

btn_gerar_grade = styled_button(frame_botoes, "Criar Grade", criar_grade)
btn_gerar_grade.pack(side="left", padx=10)

btn_gerar_excel = styled_button(frame_botoes, "Gerar Excel", gerar_excel)
btn_gerar_excel.pack(side="left", padx=10)

frame_grade = tk.Frame(root, bg=BG)
frame_grade.pack(padx=20, pady=10, fill="both", expand=True)

root.mainloop()