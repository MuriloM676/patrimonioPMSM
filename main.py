from PySide6 import QtWidgets, QtGui
import pandas as pd

# Definindo o caminho para o arquivo de dados
DB_FILE = "equipamentos.xlsx"
LOG_FILE = "logs.txt"

# Função para registrar logs
def registrar_log(log):
    with open(LOG_FILE, "r+") as log_file:
        # Lê todos os logs existentes
        existing_logs = log_file.readlines()
        # Volta para o início do arquivo
        log_file.seek(0)
        # Escreve o novo log no início do arquivo
        log_file.write(log + "\n")
        # Escreve os logs antigos logo abaixo
        log_file.writelines(existing_logs)
        
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

    num_patrimonio, ok = QtWidgets.QInputDialog.getText(None, "Cadastro", "Número de Patrimônio:")
    
    if num_patrimonio in df["Numero Patrimonio"].astype(str).values:
        QtWidgets.QMessageBox.critical(None, "Erro", "Número de patrimônio já cadastrado!")
        return

    nome, ok = QtWidgets.QInputDialog.getText(None, "Cadastro", "Nome do equipamento:")
    categoria, ok = QtWidgets.QInputDialog.getText(None, "Cadastro", "Categoria:")
    setor, ok = QtWidgets.QInputDialog.getText(None, "Cadastro", "Setor inicial:")

    if num_patrimonio and nome and categoria and setor:
        novo_id = len(df) + 1
        novo_equipamento = pd.DataFrame([[novo_id, num_patrimonio, nome, categoria, setor]], columns=df.columns)
        df = pd.concat([df, novo_equipamento], ignore_index=True)
        df.to_excel(DB_FILE, index=False)

        log = f"Cadastrado: ID {novo_id}, Patrimônio {num_patrimonio}, Nome {nome}, Setor {setor}"
        registrar_log(log)

        atualizar_logs()
        QtWidgets.QMessageBox.information(None, "Sucesso", "Equipamento cadastrado com sucesso!")
    else:
        QtWidgets.QMessageBox.warning(None, "Atenção", "Todos os campos devem ser preenchidos!")

# Função para consultar equipamentos
def verificar_equipamento():
    try:
        df = pd.read_excel(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Numero Patrimonio", "Nome", "Categoria", "Setor"])

    num_patrimonio, ok = QtWidgets.QInputDialog.getText(None, "Consulta", "Número de Patrimônio do equipamento para consulta:")
    
    equipamento = df[df["Numero Patrimonio"].astype(str) == num_patrimonio]

    if equipamento.empty:
        QtWidgets.QMessageBox.critical(None, "Erro", "Número de Patrimônio não encontrado!")
    else:
        movimentacoes = carregar_logs()
        historico = [log for log in movimentacoes if num_patrimonio in log]

        # Criando janela de consulta
        janela_consulta = QtWidgets.QWidget()
        janela_consulta.setWindowTitle("Consulta de Equipamento")
        janela_consulta.setGeometry(100, 100, 400, 300)
        janela_consulta.setStyleSheet("background-color: #f4f4f4; border-radius: 8px; padding: 10px;")

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel(f"Equipamento {num_patrimonio} Encontrado", parent=janela_consulta))
        layout.addWidget(QtWidgets.QLabel(f"Nome: {equipamento['Nome'].values[0]}", parent=janela_consulta))
        layout.addWidget(QtWidgets.QLabel(f"Categoria: {equipamento['Categoria'].values[0]}", parent=janela_consulta))
        layout.addWidget(QtWidgets.QLabel(f"Setor Atual: {equipamento['Setor'].values[0]}", parent=janela_consulta))

        layout.addWidget(QtWidgets.QLabel("Histórico de Movimentações:", parent=janela_consulta))

        if historico:
            for mov in historico:
                layout.addWidget(QtWidgets.QLabel(mov, parent=janela_consulta))
        else:
            layout.addWidget(QtWidgets.QLabel("Nenhuma movimentação registrada.", parent=janela_consulta))

        janela_consulta.setLayout(layout)
        janela_consulta.show()

# Função para movimentar equipamentos
def movimentar_equipamento():
    try:
        df = pd.read_excel(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Numero Patrimonio", "Nome", "Categoria", "Setor"])

    num_patrimonio, ok = QtWidgets.QInputDialog.getText(None, "Movimentação", "Número de Patrimônio para movimentação:")
    
    equipamento = df[df["Numero Patrimonio"].astype(str) == num_patrimonio]

    if equipamento.empty:
        QtWidgets.QMessageBox.critical(None, "Erro", "Número de Patrimônio não encontrado!")
        return

    novo_setor, ok = QtWidgets.QInputDialog.getText(None, "Movimentação", "Novo setor:")
    
    if novo_setor:
        df.loc[df["Numero Patrimonio"] == num_patrimonio, "Setor"] = novo_setor
        df.to_excel(DB_FILE, index=False)

        log = f"Movimentado: Patrimônio {num_patrimonio}, Novo Setor {novo_setor}"
        registrar_log(log)

        atualizar_logs()
        QtWidgets.QMessageBox.information(None, "Sucesso", "Equipamento movimentado com sucesso!")
    else:
        QtWidgets.QMessageBox.warning(None, "Atenção", "Você precisa informar o novo setor!")

# Função para atualizar os logs na interface
def atualizar_logs():
    log_text_widget.setPlainText("")
    
    logs = carregar_logs()
    if logs:
        log_text_widget.setPlainText("\n".join(logs))
    else:
        log_text_widget.setPlainText("Não há logs registrados.")

# Criando a interface gráfica
app = QtWidgets.QApplication([])

root = QtWidgets.QWidget()
root.setWindowTitle("Sistema de Controle de Equipamentos")
root.setGeometry(100, 100, 500, 400)
root.setStyleSheet("""
    background-color: #f2f2f2;
    border-radius: 10px;
    font-family: Arial, sans-serif;
""")

layout = QtWidgets.QVBoxLayout()

frame_buttons = QtWidgets.QGroupBox("Ações do Sistema", parent=root)
frame_buttons.setStyleSheet("background-color: #ffffff; border-radius: 8px; padding: 10px;")
frame_layout = QtWidgets.QVBoxLayout()

btn_cadastrar = QtWidgets.QPushButton("Cadastrar Equipamento", clicked=cadastrar_equipamento)
btn_consultar = QtWidgets.QPushButton("Consultar Equipamento", clicked=verificar_equipamento)
btn_movimentar = QtWidgets.QPushButton("Movimentar Equipamento", clicked=movimentar_equipamento)
btn_atualizar_logs = QtWidgets.QPushButton("Atualizar Logs", clicked=atualizar_logs)

# Estilizando os botões
btn_cadastrar.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; margin: 5px; font-size: 14px;")
btn_consultar.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px; margin: 5px; font-size: 14px;")
btn_movimentar.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 5px; margin: 5px; font-size: 14px;")
btn_atualizar_logs.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 5px; margin: 5px; font-size: 14px;")

frame_layout.addWidget(btn_cadastrar)
frame_layout.addWidget(btn_consultar)
frame_layout.addWidget(btn_movimentar)
frame_layout.addWidget(btn_atualizar_logs)
frame_buttons.setLayout(frame_layout)

layout.addWidget(frame_buttons)

log_text_widget = QtWidgets.QPlainTextEdit()
log_text_widget.setReadOnly(True)
log_text_widget.setStyleSheet("""
    background-color: #ffffff;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    font-size: 12px;
    font-family: Arial, sans-serif;
""")
layout.addWidget(log_text_widget)

root.setLayout(layout)

atualizar_logs()

root.show()
app.exec_()
