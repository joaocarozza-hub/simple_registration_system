import customtkinter as ctk
from database import criar_tabela, inserir_usuario, buscar_usuarios
from utils import validar_cpf, validar_email
import re

# Configurações iniciais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Cadastro Completo")
app.geometry("1200x720")

criar_tabela()

# --- Labels dos Campos ---
labels = [
    "Nome", "CPF", "Nascimento", "Email", "Telefone",
    "Gênero", "Estado Civil", "Rua", "Número", "Complemento",
    "Bairro", "Cidade", "Estado", "CEP"
]

formulario_posicoes = [
    ("Nome", 0, 0), ("CPF", 1, 0), ("Nascimento", 2, 0), ("Email", 3, 0),
    ("Telefone", 4, 0), ("Gênero", 5, 0), ("Estado Civil", 6, 0), ("Rua", 7, 0),
    ("Número", 0, 2), ("Complemento", 1, 2), ("Bairro", 2, 2), ("Cidade", 3, 2),
    ("Estado", 4, 2), ("CEP", 5, 2)
]

campos = {}

# --- Criação dos campos do formulário ---
for label, row, col in formulario_posicoes:
    ctk.CTkLabel(app, text=label).grid(row=row, column=col, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(app, width=250)
    entry.grid(row=row, column=col + 1, padx=10, pady=5)
    campos[label.lower().replace(" ", "_")] = entry

# --- Mensagem de status ---
status = ctk.CTkLabel(app, text="")
status.grid(row=8, column=0, columnspan=4, pady=10)

# --- Funções principais ---
def limpar_campos():
    for campo in campos.values():
        campo.delete(0, 'end')
    status.configure(text="", text_color="white")

def validar_cep(cep):
    return re.fullmatch(r"\d{5}-?\d{3}", cep) is not None

def cadastrar():
    dados = [campos[label.lower().replace(" ", "_")].get() for label in labels]

    nome = campos["nome"].get()
    cpf = campos["cpf"].get()
    email = campos["email"].get()
    cep = campos["cep"].get()

    if not nome or not cpf:
        status.configure(text="Nome e CPF são obrigatórios.", text_color="orange")
        return
    if not validar_cpf(cpf):
        status.configure(text="CPF inválido. Use apenas 11 dígitos.", text_color="red")
        return
    if email and not validar_email(email):
        status.configure(text="E-mail inválido.", text_color="red")
        return
    if cep and not validar_cep(cep):
        status.configure(text="CEP inválido. Use o formato 00000-000.", text_color="red")
        return

    try:
        inserir_usuario(dados)
        status.configure(text="Cadastro realizado com sucesso!", text_color="green")
        limpar_campos()
    except Exception as e:
        status.configure(text=f"Erro ao cadastrar: {e}", text_color="red")

# --- Botões agrupados em frame centralizado ---
botoes_frame = ctk.CTkFrame(app)
botoes_frame.grid(row=9, column=0, columnspan=4, pady=25)

ctk.CTkButton(botoes_frame, text="Cadastrar", command=cadastrar).pack(side="left", padx=20)
ctk.CTkButton(botoes_frame, text="Limpar Campos", command=limpar_campos).pack(side="left", padx=20)

# --- Área de Pesquisa ---
ctk.CTkLabel(app, text="Pesquisar por Nome, CPF ou Email").grid(row=10, column=0, padx=10, pady=10, sticky="w")
pesquisa_entry = ctk.CTkEntry(app, width=300)
pesquisa_entry.grid(row=10, column=1, padx=10, pady=10)
ctk.CTkButton(app, text="Pesquisar", command=lambda: pesquisar()).grid(row=10, column=2, padx=10)

# --- Resultados da Pesquisa ---
resultados_box = ctk.CTkTextbox(app, width=1150, height=200)
resultados_box.grid(row=11, column=0, columnspan=4, padx=10, pady=10)

def pesquisar():
    resultados_box.delete("0.0", "end")
    chave = pesquisa_entry.get()
    if not chave:
        return
    resultados = buscar_usuarios(chave)
    if resultados:
        for r in resultados:
            texto = f"ID: {r[0]} | Nome: {r[1]} | CPF: {r[2]} | Email: {r[4]} | Cidade: {r[12]} - {r[13]}\n"
            resultados_box.insert("end", texto)
    else:
        resultados_box.insert("end", "Nenhum resultado encontrado.")

# --- Inicialização da interface ---
app.mainloop()