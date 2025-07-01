import sqlite3

def conectar():
    return sqlite3.connect("cadastros.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            nascimento TEXT,
            email TEXT,
            telefone TEXT,
            genero TEXT,
            estado_civil TEXT,
            rua TEXT,
            numero TEXT,
            complemento TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserir_usuario(dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (
            nome, cpf, nascimento, email, telefone,
            genero, estado_civil,
            rua, numero, complemento, bairro, cidade, estado, cep
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()

def buscar_usuarios(chave):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios
        WHERE nome LIKE ? OR cpf LIKE ? OR email LIKE ?
    ''', (f'%{chave}%', f'%{chave}%', f'%{chave}%'))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
