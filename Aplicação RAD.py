import tkinter as tk
from tkinter import messagebox
import mysql.connector

# INICIO TELA DE LOGIN ---

def registrar():
    global usuario
    global senha
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    root.destroy()

root = tk.Tk()
root.title("Registro de Usuário e Senha")

label_usuario = tk.Label(root, text="Usuário:")
label_usuario.pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

label_senha = tk.Label(root, text="Senha:")
label_senha.pack()
entry_senha = tk.Entry(root, show="*")  # O "show" esconde o texto da senha
entry_senha.pack()

botao_registrar = tk.Button(root, text="Acessar", command=registrar)
botao_registrar.pack()

root.mainloop()

# FIM TELA DE LOGIN ---

# CONEXÃO COM O BANCO DE DADOS MYSQL ---
db = mysql.connector.connect(
    host="localhost",
    user=usuario,
    password=senha,
    database="tarefas_db"
)

cursor = db.cursor()
# FIM DA CONEXÃO COM O BANCO DE DADOS MYSQL ---

# INICIO DAS FUNÇÕES DE REGISTRO DE TAREFAS ---

# Função para adicionar uma tarefa ao banco de dados
def adicionar_tarefa():
    tarefa = entrada_tarefa.get()
    if tarefa:
        cursor.execute("INSERT INTO tarefas (descricao) VALUES (%s)", (tarefa,))
        db.commit()
        listar_tarefas()
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira uma tarefa.")

# Função para listar as tarefas do banco de dados
def listar_tarefas():
    lista_tarefas.delete(0, tk.END)
    cursor.execute("SELECT * FROM tarefas")
    for (id, descricao) in cursor:
        lista_tarefas.insert(tk.END, f"{id}: {descricao}")

# Função para editar uma tarefa
def editar_tarefa():
    tarefa_selecionada = lista_tarefas.curselection()
    if tarefa_selecionada:
        tarefa_id = lista_tarefas.get(tarefa_selecionada[0]).split(":")[0]
        nova_descricao = entrada_tarefa.get()
        if nova_descricao:
            cursor.execute("UPDATE tarefas SET descricao=%s WHERE id=%s", (nova_descricao, tarefa_id))
            db.commit()
            listar_tarefas()
            entrada_tarefa.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma nova descrição para a tarefa.")
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para editar.")

# Função para excluir uma tarefa do banco de dados
def excluir_tarefa():
    tarefa_selecionada = lista_tarefas.curselection()
    if tarefa_selecionada:
        tarefa_id = lista_tarefas.get(tarefa_selecionada[0]).split(":")[0]
        cursor.execute("DELETE FROM tarefas WHERE id=%s", (tarefa_id,))
        db.commit()
        listar_tarefas()
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")

# Configuração da janela
janela = tk.Tk()
janela.title("Lista de Tarefas")

# Entrada de tarefa
entrada_tarefa = tk.Entry(janela, width=40)
entrada_tarefa.pack(pady=10)

# Botão para adicionar tarefa
botao_adicionar = tk.Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa)
botao_adicionar.pack()

# Botão para editar tarefa

botao_editar = tk.Button(janela, text="Editar Tarefa", command=editar_tarefa)
botao_editar.pack()


# Lista de tarefas
lista_tarefas = tk.Listbox(janela, width=50)
lista_tarefas.pack()

# Botão para excluir tarefa
botao_excluir = tk.Button(janela, text="Excluir Tarefa", command=excluir_tarefa)
botao_excluir.pack()

# Listar tarefas ao iniciar a aplicação
listar_tarefas()

# Loop principal
janela.mainloop()

# Fechar o cursor e a conexão com o banco de dados ao fechar a aplicação
cursor.close()
db.close()
# FIM DAS FUNÇÕES DE REGISTRO DE TAREFAS ---