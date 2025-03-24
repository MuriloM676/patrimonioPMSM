import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd

# Definindo o caminho para o arquivo de dados
DB_FILE = "equipamentos.xlsx"
LOG_FILE = "logs.txt"

# Função para registrar logs
def registrar_log(log):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log + "\n")

# Função para carregar os logs
def carregar_logs():
    try:
        with open(LOG_FILE, "r") as log_file:
            return log_file.readlines()
    except FileNotFoundError:
        return []

# Função para cadastrar equipamentos
def cadastrar_equipamento():
    try:
        df = pd.read_excel(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Numero Patrimonio", "Nome", "Categoria", "Setor"])

    num_patrimonio = simpledialog.askstring("Cadastro", "Número de Patrimônio:")

    if num_patrimonio in df["Numero Patrimonio"].astype(str).values:
        messagebox.showerror("Erro", "Número de patrimônio já cadastrado!")
        return

    nome = simpledialog.askstring("Cadastro", "Nome do equipamento:")
    categoria = simpledialog.askstring("Cadastro", "Categoria:")
    setor = simpledialog.askstring("Cadastro", "Setor inicial:")

    if num_patrimonio and nome and categoria and setor:
        novo_id = len(df) + 1
        novo_equipamento = pd.DataFrame([[novo_id, num_patrimonio, nome, categoria, setor]], columns=df.columns)
        df = pd.concat([df, novo_equipamento], ignore_index=True)
        df.to_excel(DB_FILE, index=False)

        log = f"Cadastrado: ID {novo_id}, Patrimônio {num_patrimonio}, Nome {nome}, Setor {setor}"
        registrar_log(log)

        atualizar_logs()
        messagebox.showinfo("Sucesso", "Equipamento cadastrado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")

# Função para consultar equipamentos
def verificar_equipamento():
    try:
        df = pd.read_excel(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Numero Patrimonio", "Nome", "Categoria", "Setor"])

    num_patrimonio = simpledialog.askstring("Consulta", "Número de Patrimônio do equipamento para consulta:")
    
    equipamento = df[df["Numero Patrimonio"].astype(str) == num_patrimonio]

    if equipamento.empty:
        messagebox.showerror("Erro", "Número de Patrimônio não encontrado!")
    else:
        movimentacoes = carregar_logs()
        historico = [log for log in movimentacoes if num_patrimonio in log]

        # Criando janela de consulta
        janela_consulta = tk.Toplevel()
        janela_consulta.title("Consulta de Equipamento")
        janela_consulta.geometry("400x300")
        janela_consulta.configure(bg="#f2f2f2")

        ttk.Label(janela_consulta, text=f"Equipamento {num_patrimonio} Encontrado", font=("Arial", 12, "bold"), background="#f2f2f2").pack(pady=10)
        ttk.Label(janela_consulta, text=f"Nome: {equipamento['Nome'].values[0]}", background="#f2f2f2").pack()
        ttk.Label(janela_consulta, text=f"Categoria: {equipamento['Categoria'].values[0]}", background="#f2f2f2").pack()
        ttk.Label(janela_consulta, text=f"Setor Atual: {equipamento['Setor'].values[0]}", background="#f2f2f2").pack()

        ttk.Label(janela_consulta, text="Histórico de Movimentações:", font=("Arial", 10, "bold"), background="#f2f2f2").pack(pady=5)

        if historico:
            for mov in historico:
                ttk.Label(janela_consulta, text=mov, background="#f2f2f2").pack()
        else:
            ttk.Label(janela_consulta, text="Nenhuma movimentação registrada.", background="#f2f2f2").pack()

# Função para movimentar equipamentos
def movimentar_equipamento():
    try:
        df = pd.read_excel(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Numero Patrimonio", "Nome", "Categoria", "Setor"])

    num_patrimonio = simpledialog.askstring("Movimentação", "Número de Patrimônio para movimentação:")
    
    equipamento = df[df["Numero Patrimonio"].astype(str) == num_patrimonio]

    if equipamento.empty:
        messagebox.showerror("Erro", "Número de Patrimônio não encontrado!")
        return

    novo_setor = simpledialog.askstring("Movimentação", "Novo setor:")
    
    if novo_setor:
        df.loc[df["Numero Patrimonio"] == num_patrimonio, "Setor"] = novo_setor
        df.to_excel(DB_FILE, index=False)

        log = f"Movimentado: Patrimônio {num_patrimonio}, Novo Setor {novo_setor}"
        registrar_log(log)

        atualizar_logs()
        messagebox.showinfo("Sucesso", "Equipamento movimentado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Você precisa informar o novo setor!")

# Função para atualizar os logs na interface
def atualizar_logs():
    log_text_widget.config(state=tk.NORMAL)
    log_text_widget.delete("1.0", tk.END)
    
    logs = carregar_logs()
    if logs:
        log_text_widget.insert(tk.END, "\n".join(logs))
    else:
        log_text_widget.insert(tk.END, "Não há logs registrados.")

    log_text_widget.config(state=tk.DISABLED)

# Criando a interface gráfica melhorada
root = tk.Tk()
root.title("Sistema de Controle de Equipamentos")
root.geometry("500x400")
root.configure(bg="#f2f2f2")

style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", background="#f2f2f2", font=("Arial", 10))

frame_buttons = tk.Frame(root, bg="#f2f2f2")
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="Cadastrar Equipamento", command=cadastrar_equipamento, width=30).grid(row=0, column=0, pady=5)
ttk.Button(frame_buttons, text="Consultar Equipamento", command=verificar_equipamento, width=30).grid(row=1, column=0, pady=5)
ttk.Button(frame_buttons, text="Movimentar Equipamento", command=movimentar_equipamento, width=30).grid(row=2, column=0, pady=5)
ttk.Button(frame_buttons, text="Atualizar Logs", command=atualizar_logs, width=30).grid(row=3, column=0, pady=5)

log_text_widget = tk.Text(root, width=60, height=10, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", relief="solid", borderwidth=1)
log_text_widget.pack(pady=10)

atualizar_logs()

root.mainloop()