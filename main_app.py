import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime, timedelta
import customtkinter as ctk

class AlimentacaoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("DUDU - Seu sistema inteligente!")
        self.master.geometry("345x400")
        self.master.configure(bg="#f0f0f0")
        self.master.iconbitmap("imagem/azul.ico")
        
        self.conectar_banco()
        self.criar_tabela()
        
        self.criar_widgets()

    def conectar_banco(self):
        self.conn = sqlite3.connect('alimentacao.db')
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                            data TEXT,
                            alimentacao TEXT
                            )''')
        self.conn.commit()

    def criar_widgets(self):
        self.lbl_myhst = tk.Label(self.master, text="DUDU", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 20, 'bold'))
        self.lbl_myhst.pack(pady=10)

        self.lbl_data = tk.Label(self.master, text="SELECIONE A DATA:", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
        self.lbl_data.pack(pady=5)

        self.cal_data = DateEntry(self.master, width=12, background='#2c3e50', foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
        self.cal_data.pack(pady=5)

        self.lbl_info = tk.Label(self.master, text="REGISTRE SUA ALIMENTAÇÃO DIÁRIA", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
        self.lbl_info.pack(pady=5)

        self.opcoes_alimentacao = ["SELECIONE","NÃO FUI SAUDÁVEL", "FUI SAUDÁVEL", "FUI MUITO SAUDÁVEL"]
        self.tipo_alimentacao = tk.StringVar(self.master)
        self.tipo_alimentacao.set(self.opcoes_alimentacao[0]) 
        self.menu_alimentacao = tk.OptionMenu(self.master, self.tipo_alimentacao, *self.opcoes_alimentacao)
        self.menu_alimentacao.pack(pady=5)

        self.lbl_id = tk.Label(self.master, text="INSIRA SEU ID:", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
        self.lbl_id.pack(pady=5)

        self.entry_id = tk.Entry(self.master)
        self.entry_id.pack(pady=5)

        self.btn_registrar = ctk.CTkButton(self.master, text="REGISTRAR", command=self.registrar_alimentacao, corner_radius=5, width=20)
        self.btn_registrar.pack(pady=10, ipadx=10, ipady=5)

        self.btn_proxima_semana = ctk.CTkButton(self.master, text="HISTÓRICO DE REGISTROS", command=self.verificar_semana, corner_radius=5, width=20)
        self.btn_proxima_semana.pack(pady=10, ipadx=10, ipady=5)


    def registrar_alimentacao(self):
        
        if self.entry_id.get() == "":
            messagebox.showerror("ERRO", "INSIRA SEU ID DE USUÁRIO")
            return
            
            
        if self.tipo_alimentacao.get() == self.opcoes_alimentacao[0]:
            messagebox.showerror("ERRO", "SELECIONE UMA OPÇÃO")
            return
        
        data = self.cal_data.get_date()
        alimentacao = self.tipo_alimentacao.get()
        usuario_id = self.entry_id.get()

        self.cursor.execute("SELECT * FROM registros WHERE data=? AND usuario_id=?", (data, usuario_id))
        registro_existente = self.cursor.fetchone()

        if registro_existente:
            messagebox.showwarning("Aviso", "Já existe um registro para esta data e este ID de pessoa.")
            return

        self.cursor.execute("INSERT INTO registros (data, alimentacao, usuario_id) VALUES (?, ?, ?)", (data, alimentacao, usuario_id))
        self.conn.commit()

        messagebox.showinfo("Sucesso", "Alimentação registrada com sucesso!")



    def verificar_semana(self):
        
        if self.entry_id.get() == "":
            messagebox.showerror("ERRO", "INSIRA SEU ID DE USUÁRIO PARA CONSULTAR A SEMANA")
            return
        
        
        data_atual = datetime.now().date()
        data_inicio_semana = data_atual - timedelta(days=data_atual.weekday())
        data_fim_semana = data_inicio_semana + timedelta(days=6)
        usuario_id = self.entry_id.get()

        self.cursor.execute("SELECT data, alimentacao FROM registros WHERE usuario_id=? AND data BETWEEN ? AND ?", 
                            (usuario_id, data_inicio_semana, data_fim_semana))
        registros = self.cursor.fetchall()

        formulario = tk.Toplevel(self.master)
        formulario.title("DUDU - Seu sistema inteligente")

        if registros:
            for data, alimentacao in registros:
                data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                lbl_data = tk.Label(formulario, text=f"Data: {data_formatada}", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
                lbl_data.pack()
                lbl_alimentacao = tk.Label(formulario, text=f"Alimentação: {alimentacao}", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
                lbl_alimentacao.pack()
        else:
            lbl_aviso = tk.Label(formulario, text="Não há registros para esta semana.", bg="#f0f0f0", fg="#2c3e50", font=("Arial", 12))
            lbl_aviso.pack()
            
            
        

def main():
    root = tk.Tk()
    root.configure(bg="#f0f0f0")
    app = AlimentacaoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
