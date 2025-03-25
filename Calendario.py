import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

def selecionar_data(data_var):
    def confirmar_data():
        data_var.set(cal.get_date())
        janela_data.destroy()
    
    janela_data = tk.Toplevel()
    janela_data.title("Selecionar Data")
    janela_data.geometry("400x300")
    
    frame_calendario = tk.Frame(janela_data)
    frame_calendario.pack(fill=tk.BOTH, expand=True, pady=10)
    
    cal = Calendar(frame_calendario, selectmode='day')
    cal.pack(fill=tk.BOTH, expand=True)
    
    frame_botoes = tk.Frame(janela_data)
    frame_botoes.pack(pady=10)
    
    btn_confirmar = tk.Button(frame_botoes, text="Confirmar", command=confirmar_data)
    btn_confirmar.pack(side=tk.LEFT, padx=5)
    
    btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_data.destroy)
    btn_cancelar.pack(side=tk.RIGHT, padx=5)
    