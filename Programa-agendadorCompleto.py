
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from twilio.rest import Client



dados_servicos = []
dados_agendamentos = []

def atualizar_lista_servicos(lista_box):
    lista_box.delete(0, tk.END)
    for servico in dados_servicos:
        lista_box.insert(tk.END, f"{servico['nome']} - {servico['duracao']} min")

def cadastrar_servicos():
    def adicionar_servico():
        nome = entry_nome.get()
        duracao = entry_duracao.get()
        if nome and duracao.isdigit():
            dados_servicos.append({"nome": nome, "duracao": int(duracao)})
            atualizar_lista_servicos(lista_servicos)
            entry_nome.delete(0, tk.END)
            entry_duracao.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Insira um nome válido e uma duração em minutos.")

    def excluir_servico():
        selecionado = lista_servicos.curselection()
        if selecionado:
            indice = selecionado[0]
            del dados_servicos[indice]
            atualizar_lista_servicos(lista_servicos)
        else:
            messagebox.showwarning("Atenção", "Selecione um serviço para excluir.")

    def confirmar_operacao():
            messagebox.showinfo("Confirmado", "Serviços cadastrados com sucesso!")
            janela_servicos.destroy()
    
    janela_servicos = tk.Toplevel()
    janela_servicos.title("Cadastro de Serviços")
    janela_servicos.geometry("400x400")

    tk.Label(janela_servicos, text="Nome do Serviço:").pack()
    entry_nome = tk.Entry(janela_servicos)
    entry_nome.pack()

    tk.Label(janela_servicos, text="Duração (minutos):").pack()
    entry_duracao = tk.Entry(janela_servicos)
    entry_duracao.pack()

    btn_adicionar = tk.Button(janela_servicos, text="Adicionar Serviço", command=adicionar_servico)
    btn_adicionar.pack(pady=5)

    lista_servicos = tk.Listbox(janela_servicos, width=50, height=10)
    lista_servicos.pack()

    btn_excluir = tk.Button(janela_servicos, text="Excluir Serviço", command=excluir_servico)
    btn_excluir.pack(pady=5)
    
    btn_confirmar = tk.Button(janela_servicos, text="Confirmar", command=confirmar_operacao)
    btn_confirmar.pack(pady=5)
    
def gerar_horarios():
    horarios = []
    for hora in range(8, 20):
        if hora == 12:
            continue  # Pula horário do almoço
        for minuto in ["00", "30"]:
            horarios.append(f"{hora}:{minuto}")
    return horarios

def verificar_conflito(horario):
    for agendamento in dados_agendamentos:
        if agendamento["horario"] == horario:
            return True
    return False
    
def agendar_cliente():
    def confirmar_agendamento():
        nome = entry_nome.get()
        numero = entry_numero.get()
        servico = combo_servicos.get()
        horario = combo_horarios.get()
        
        if nome and numero.isdigit() and servico and horario:
            dados_agendamentos.append({"nome": nome, "numero": numero, "servico": servico, "horario": horario})
            messagebox.showinfo("Sucesso", f"Agendamento confirmado para {nome} às {horario}.")
            janela_agendamento.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    janela_agendamento = tk.Toplevel()
    janela_agendamento.title("Agendar Cliente")
    janela_agendamento.geometry("500x300")
    
    tk.Label(janela_agendamento, text="Nome do Cliente:").pack()
    entry_nome = tk.Entry(janela_agendamento)
    entry_nome.pack()
    
    tk.Label(janela_agendamento, text="Telefone do Cliente:").pack()
    entry_numero = tk.Entry(janela_agendamento)
    entry_numero.pack()
    
    tk.Label(janela_agendamento, text="Escolha o Serviço:").pack()
    combo_servicos = ttk.Combobox(janela_agendamento, values=[s["nome"] for s in dados_servicos])
    combo_servicos.pack()
    
    tk.Label(janela_agendamento, text="Escolha o Horário:").pack()
    combo_horarios = ttk.Combobox(janela_agendamento, values=gerar_horarios())  # Pode ser dinamizado depois
    combo_horarios.pack()
    
    btn_confirmar = tk.Button(janela_agendamento, text="Confirmar Agendamento", command=confirmar_agendamento)
    btn_confirmar.pack(pady=5)
    
    
def reagendar_cliente():
    def confirmar_reagendamento():
        cliente = combo_clientes.get()
        novo_horario = combo_horarios.get()
        novo_servico = combo_servicos.get()
        
        if cliente and novo_horario:
            for agendamento in dados_agendamentos:
                if agendamento["nome"] == cliente:
                    if verificar_conflito(novo_horario):
                        messagebox.showerror("Erro", "Horário já agendado. Escolha outro.")
                        return
                    agendamento["horario"] = novo_horario
                    if novo_servico:
                        agendamento["servico"] = novo_servico
                    messagebox.showinfo("Sucesso", f"{cliente} reagendado para {novo_horario}.")
                    janela_reagendamento.destroy()
                    return
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
    
    janela_reagendamento = tk.Toplevel()
    janela_reagendamento.title("Reagendar Cliente")
    janela_reagendamento.geometry("400x400")
    
    tk.Label(janela_reagendamento, text="Escolha o Cliente:").pack()
    combo_clientes = ttk.Combobox(janela_reagendamento, values=[a["nome"] for a in dados_agendamentos])
    combo_clientes.pack()
    
    tk.Label(janela_reagendamento, text="Novo Horário:").pack()
    combo_horarios = ttk.Combobox(janela_reagendamento, values=gerar_horarios())
    combo_horarios.pack()
    
    tk.Label(janela_reagendamento, text="Novo Serviço (opcional):").pack()
    combo_servicos = ttk.Combobox(janela_reagendamento, values=[s["nome"] for s in dados_servicos])
    combo_servicos.pack()
    
    btn_confirmar = tk.Button(janela_reagendamento, text="Confirmar Reagendamento", command=confirmar_reagendamento)
    btn_confirmar.pack(pady=5)
    
def consultar_agendamentos():
    def buscar_agendamentos():
        nome_busca = entry_nome.get().strip().lower()
        
        lista_agendamentos.delete(0, tk.END)
        
        agendamentos_encontrados = False
        for agendamento in dados_agendamentos:
            if not nome_busca or nome_busca in agendamento["nome"].lower():
                lista_agendamentos.insert(tk.END, f"{agendamento['nome']} - {agendamento['horario']} - {agendamento['servico']} ")
                agendamentos_encontrados = True
        
        if not agendamentos_encontrados:
            lista_agendamentos.insert(tk.END, "Nenhum agendamento encontrado.")
    
    
    janela_consulta = tk.Toplevel()
    janela_consulta.title("Consulta de Agendamentos")
    janela_consulta.geometry("600x500")
    
    frame_busca = tk.Frame(janela_consulta)
    frame_busca.pack(pady=10)
    
    tk.Label(frame_busca, text="Nome:").grid(row=0, column=0, padx=5)
    entry_nome = tk.Entry(frame_busca, width=20)
    entry_nome.grid(row=0, column=1, padx=5)
    
    btn_buscar = tk.Button(frame_busca, text="Buscar", command=buscar_agendamentos)
    btn_buscar.grid(row=0, column=2, padx=5)
    
    tk.Label(janela_consulta, text="Agendamentos:", font=("Arial", 12)).pack(pady=5)
    
    lista_agendamentos = tk.Listbox(janela_consulta, width=80, height=20)
    lista_agendamentos.pack(pady=10)
    
    frame_botoes = tk.Frame(janela_consulta)
    frame_botoes.pack(pady=10)
    
    btn_fechar = tk.Button(frame_botoes, text="Fechar", command=janela_consulta.destroy)
    btn_fechar.grid(row=0, column=1, padx=10)
    
    # Mostrar todos os agendamentos inicialmente
    buscar_agendamentos()

def cancelar_agendamento():
    def buscar_agendamentos():
        nome_busca = entry_nome.get().strip().lower()
        
        lista_agendamentos.delete(0, tk.END)
        indices_encontrados.clear()
        
        for i, agendamento in enumerate(dados_agendamentos):
            if not nome_busca or nome_busca in agendamento["nome"].lower():
                lista_agendamentos.insert(tk.END, f"{agendamento['nome']} - {agendamento['horario']} - {agendamento['servico']}")
                indices_encontrados.append(i)
        
        if not indices_encontrados:
            lista_agendamentos.insert(tk.END, "Nenhum agendamento encontrado.")
    
    def cancelar():
        selecionado = lista_agendamentos.curselection()
        if selecionado:
            indice_lista = selecionado[0]
            if indice_lista < len(indices_encontrados):
                indice_agendamento = indices_encontrados[indice_lista]
                cliente = dados_agendamentos[indice_agendamento]["nome"]
                horario = dados_agendamentos[indice_agendamento]["horario"]
                
                resposta = messagebox.askyesno("Confirmação", f"Deseja realmente cancelar o agendamento de {cliente} às {horario}?")
                if resposta:
                    del dados_agendamentos[indice_agendamento]
                    messagebox.showinfo("Sucesso", "Agendamento cancelado com sucesso!")
                    # Atualizar a lista
                    indices_encontrados.clear()
                    buscar_agendamentos()
            else:
                messagebox.showwarning("Atenção", "Selecione um agendamento válido.")
        else:
            messagebox.showwarning("Atenção", "Selecione um agendamento para cancelar.")
    
    janela_cancelamento = tk.Toplevel()
    janela_cancelamento.title("Cancelamento de Agendamentos")
    janela_cancelamento.geometry("500x600")
    
    frame_busca = tk.Frame(janela_cancelamento)
    frame_busca.pack(pady=10)
    
    tk.Label(frame_busca, text="Nome do Cliente:").grid(row=0, column=0, padx=5)
    entry_nome = tk.Entry(frame_busca, width=30)
    entry_nome.grid(row=0, column=1, padx=5)
    
    btn_buscar = tk.Button(frame_busca, text="Buscar", command=buscar_agendamentos)
    btn_buscar.grid(row=0, column=2, padx=5)
    
    tk.Label(janela_cancelamento, text="Agendamentos:", font=("Arial", 12)).pack(pady=5)
    
    lista_agendamentos = tk.Listbox(janela_cancelamento, width=70, height=15)
    lista_agendamentos.pack(pady=10)
    
    indices_encontrados = []
    
    btn_cancelar = tk.Button(janela_cancelamento, text="Cancelar Agendamento Selecionado", command=cancelar)
    btn_cancelar.pack(pady=5)
    
    btn_fechar = tk.Button(janela_cancelamento, text="Fechar", command=janela_cancelamento.destroy)
    btn_fechar.pack(pady=5)
    
    # Mostrar todos os agendamentos inicialmente
    buscar_agendamentos()


def enviar_lembrete():
    def enviar_whatsapp(destinatario, mensagem):
        try:
            # Configurações da conta Twilio
            # Substitua pelo seu Account SID
            account_sid = "AC3622426f06a40ae104263981f255a9a8"
            auth_token = "922128e79e0aabd8a93d70fc28c73fa4"    # Substitua pelo seu Auth Token
            twilio_whatsapp_number = "whatsapp:+14155238886"  # Número do Twilio

            # Cria o cliente Twilio
            client = Client(account_sid, auth_token)

            # Envia a mensagem
            message = client.messages.create(
                body=mensagem,
                from_=twilio_whatsapp_number,
                # Número do destinatário no formato internacional
                to=f"whatsapp:{destinatario}"
            )
            print(f"Mensagem enviada para {destinatario}: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
        
        
    janela_lembrete = tk.Toplevel()
    janela_lembrete.title("Envio de Lembretes")
    janela_lembrete.geometry("600x500")
    
    tk.Label(janela_lembrete, text="Agendamentos:", font=("Arial", 12)).pack(pady=5)
    
    lista_agendamentos = tk.Listbox(janela_lembrete, width=80, height=15)
    lista_agendamentos.pack(pady=10)
    
    # Preencher lista de agendamentos
    for agendamento in dados_agendamentos:
        lista_agendamentos.insert(tk.END, f"{agendamento['nome']} - {agendamento['horario']} - {agendamento['servico']} - {agendamento['numero']}")
    
    tk.Label(janela_lembrete, text="Mensagem de Lembrete:").pack(pady=5)
    entry_mensagem = tk.Text(janela_lembrete, width=70, height=5)
    entry_mensagem.pack(pady=5)
    
    # Texto padrão para a mensagem
    entry_mensagem.insert("1.0", "Olá! Este é um lembrete para seu agendamento. Aguardamos sua presença!")
    
    frame_botoes = tk.Frame(janela_lembrete)
    frame_botoes.pack(pady=10)
    
    btn_enviar = tk.Button(frame_botoes, text="Enviar Lembrete", command=enviar_whatsapp)
    btn_enviar.grid(row=0, column=0, padx=10)
    
    btn_fechar = tk.Button(frame_botoes, text="Fechar", command=janela_lembrete.destroy)
    btn_fechar.grid(row=0, column=1, padx=10)
    
    
def visualizar_calendario():
    try:
        from tkcalendar import Calendar
    except ImportError:
        messagebox.showerror("Erro", "A biblioteca tkcalendar não está instalada. Instale-a usando 'pip install tkcalendar'.")
        return
    
    def mostrar_agendamentos_do_dia(event):
        # Obter a data selecionada no calendário
        data_selecionada = cal.get_date()  # Formato: MM/DD/YY
        
        # Limpar a lista de agendamentos
        lista_agendamentos_dia.delete(0, tk.END)
        
        # Buscar agendamentos para o dia
        agendamentos_do_dia = []
        for agendamento in dados_agendamentos:
            if agendamento["horario"].startswith(data_selecionada[:2]):  # Simplificação para demonstração
                agendamentos_do_dia.append(agendamento)
        
        # Ordenar por horário
        agendamentos_do_dia.sort(key=lambda x: x["horario"])
        
        # Preencher a lista
        if agendamentos_do_dia:
            for agendamento in agendamentos_do_dia:
                status = "Confirmado" if agendamento.get("confirmado", False) else "Pendente"
                lista_agendamentos_dia.insert(tk.END, f"{agendamento['horario']} - {agendamento['nome']} - {agendamento['servico']} - {status}")
        else:
            lista_agendamentos_dia.insert(tk.END, "Nenhum agendamento para esta data.")
    
    janela_calendario = tk.Toplevel()
    janela_calendario.title("Visualização de Agenda")
    janela_calendario.geometry("800x600")
    
    # Dividir a tela em duas partes
    frame_esquerda = tk.Frame(janela_calendario)
    frame_esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    frame_direita = tk.Frame(janela_calendario)
    frame_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Adicionar o calendário
    cal = Calendar(frame_esquerda, selectmode='day')
    cal.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Vincular evento de seleção de data
    cal.bind("<<CalendarSelected>>", mostrar_agendamentos_do_dia)
    
    # Lista de agendamentos do dia
    tk.Label(frame_direita, text="Agendamentos do Dia:", font=("Arial", 12)).pack(pady=5)
    
    lista_agendamentos_dia = tk.Listbox(frame_direita, width=50, height=20)
    lista_agendamentos_dia.pack(pady=10, fill=tk.BOTH, expand=True)
    
    btn_fechar = tk.Button(frame_direita, text="Fechar", command=janela_calendario.destroy)
    btn_fechar.pack(pady=10)

ARQUIVO_DADOS = "dados_servicos.json"

def carregar_dados():
    global dados_servicos
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r') as f:
            dados_servicos = json.load(f)

def salvar_dados():
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(dados_servicos, f)

# Adicione estas linhas ANTES de criar a janela principal
carregar_dados()

# Modifique a função de fechamento da janela principal

# Criando a janela principal
janela = tk.Tk()
janela.title("Sistema de Agendamento")
janela.geometry("500x500")

# Mensagem de boas-vindas
label_titulo = tk.Label(janela, text="Bem-vindo ao Sistema de Agendamento", font=("Arial", 14))
label_titulo.pack(pady=10)

janela.protocol("WM_DELETE_WINDOW", lambda: [salvar_dados(), janela.destroy()])

# Botões das funcionalidades
botoes = [
    ("Cadastro de Serviços", cadastrar_servicos),
    ("Agendar Cliente", agendar_cliente),
    ("Reagendar Cliente", reagendar_cliente),
    ("Consulta de Agendamentos", consultar_agendamentos),
    ("Cancelamentos", cancelar_agendamento),
    ("Enviar Lembrete", enviar_lembrete),
    ("Visualizar Calendarío", visualizar_calendario)
]

for texto, comando in botoes:
    btn = tk.Button(janela, text=texto, font=("Arial", 12), width=30, height=2, command=comando)
    btn.pack(pady=5)

# Rodando a aplicação
janela.mainloop()
