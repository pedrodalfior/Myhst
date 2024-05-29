import tkinter as tk
from tkinter import messagebox
import sqlite3
import main_app

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Myhst")
        self.master.geometry("300x200")
        self.master.minsize(300, 200) 
        self.master.maxsize(300, 200)  
        self.master.configure(bg="white")
        
        self.conectar_banco()
        self.criar_tabela_usuarios()
        
        self.criar_widgets()

    def conectar_banco(self):
        try:
            self.conn = sqlite3.connect('alimentacao.db')
            self.cursor = self.conn.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except sqlite3.Error as e:
            print("Erro ao conectar ao banco de dados:", e)

    def criar_tabela_usuarios(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT,
                                senha TEXT
                                )''')
            self.conn.commit()
            print("Tabela de usuários criada com sucesso.")
        except sqlite3.Error as e:
            print("Erro ao criar tabela de usuários:", e)

    def criar_widgets(self):
        self.lbl_usuario = tk.Label(self.master, text="Nome de usuário:", bg="white", fg="#2c3e50", font=("Arial", 12))
        self.lbl_usuario.grid(row=0, column=0, padx=10, pady=5)

        self.entry_usuario = tk.Entry(self.master)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=5)

        self.lbl_senha = tk.Label(self.master, text="Senha:", bg="white", fg="#2c3e50", font=("Arial", 12))
        self.lbl_senha.grid(row=1, column=0, padx=10, pady=5)

        self.entry_senha = tk.Entry(self.master, show="*")
        self.entry_senha.grid(row=1, column=1, padx=10, pady=5)

        self.btn_login = tk.Button(self.master, text="Login", command=self.fazer_login, bg="#2c3e50", fg="white", font=("Arial", 12), relief=tk.FLAT, bd=0, padx=10, pady=5, borderwidth=0, highlightthickness=0)
        self.btn_login.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        self.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
        usuario_encontrado = self.cursor.fetchone()

        if usuario_encontrado:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.master.destroy() 
            main_app.main() 
            
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")

def main():
    root = tk.Tk()
    root.configure(bg="white")

    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
