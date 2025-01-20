import PySimpleGUI as sg
import fcot as cot
import fsav as sav
import fmsg as mil
import time
import sys
import os

if getattr(sys, 'frozen', False):  # If running as a compiled .exe
    icon_path = os.path.join(sys._MEIPASS, 'img.ico')
else:  # If running as a .py file
    icon_path = 'img.ico'

def janela_main():
    WIN_W = 30
    WIN_H = 50
    sg.theme('GrayGrayGray')
    layout_main = [
        [sg.Text('Ativo Bovespa'), sg.InputText(key='nome1', size=(int(WIN_W/2),1)), sg.InputText(key='nome2', size=(int(WIN_W/2),1))],
        [sg.Text('Preços          '), sg.InputText(key='valor1', size=(int(WIN_W/2),1)), sg.InputText(key='valor2', size=(int(WIN_W/2),1))],
        [sg.Text('Meta %         '), sg.InputText(key='taxa', size=(int(WIN_W/2),1))],
        [sg.Push(), sg.Text('Desativado', key='status'), sg.Push()],
        [sg.Multiline(size=(50,10), key='output', disabled=True, autoscroll=True)],
        [sg.Text('')],
        [sg.Button('Configurações', key='config'), sg.Button('Limpar', key='cls'), sg.Button('Salvar', key='save_main'), sg.Button('Cancelar', key='cancel_main', button_color=('white', 'grey')), sg.Button('Iniciar', key='start', button_color=('black', '#3de226'))]
    ]
    return sg.Window('Alarme de cotações da BOVESPA',layout_main, finalize=True, icon=icon_path)

def janela_config():
    WIN_W = 25
    WIN_H = 20
    sg.theme('GrayGrayGray')
    layout = [
        [sg.Text('Email destinatário'), sg.InputText(key='email',size=(int(WIN_W),1))],
        [sg.Text('Email remetente  '), sg.InputText(key='remetente',size=(int(WIN_W),1))],
        [sg.Text('Senha remetente '), sg.InputText(key='token',size=(int(WIN_W),1))],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_config', button_color=('white', 'red')), sg.Button('Salvar', key='save_config', button_color=('black', '#3de226'))]
    ]
    return sg.Window('Configurações',layout, finalize=True, icon=icon_path)

janela1, janela2 = janela_main(), None
running = False
start_time = None
meta = False

dic = sav.read_json('menu')
if dic == False:
    pass
else:
    try:
        for i in ['nome1', 'nome2', 'valor1', 'valor2', 'taxa']:
            janela1[i].update(dic[i])
    except:
        pass

while True:
    window, event, values = sg.read_all_windows(timeout=1000)
    # X
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela2 and event == sg.WIN_CLOSED:
        janela2.hide()
    # BOTÃO CONFIGURAÇÕES
    if window == janela1 and event == 'config':
        janela2 = janela_config()
        # Auto preenchimento
        dic = sav.read_json('config')
        if dic == False:
            pass
        else:
            try:
                janela2['email'].update(dic['email'])
                janela2['remetente'].update(dic['remetente'])
                janela2['token'].update(dic['token'])
            except:
                pass
    # BOTÃO PÁGINA CONFIG CANCELAR
    if window == janela2 and event == 'cancel_config':
        janela2.hide()
    # BOTÃO PÁGINA CONFIG SALVAR
    if window == janela2 and event == 'save_config':
        result = sav.create_json_config(values['email'], values['remetente'], values['token'])
        if result == False:
            sg.popup('Ocorreu um erro. Verifique se todos os dados foram inseridos.', icon=icon_path)
        janela2.hide()
    
    # COMANDOS JANELA MAIN
    if window == janela1 and event == 'start':
        try:
            valor1 = cot.virgula(values['valor1'])
            valor2 = cot.virgula(values['valor2'])
            taxa = cot.virgula(values['taxa'])*0.01
            nome1 = values['nome1'].upper()
            nome2 = values['nome2'].upper()
            janela1['status'].update('Ativado')
            janela1['cancel_main'].update(button_color=('white', 'red'))
            janela1['start'].update(button_color=('white', 'grey'))
            running = True
            start_time = time.time()
            janela1['output'].update('')
        except:
            janela1['output'].update('Digite valores válidos\n', append=True)
    
    # BOTÃO CANCELAR OPERAÇÃO
    if window == janela1 and event == 'cancel_main':
        running = False
        janela1['cancel_main'].update(button_color=('white', 'grey'))
        janela1['start'].update(button_color=('black', '#3de226'))
        janela1['status'].update('Desativado')

    # A cada 60 segundos o cálculo é realizado
    if running:
        inst_time = time.time()
        if inst_time - start_time >= 2:
            papel1 = cot.pregao_inst(nome1)
            papel2 = cot.pregao_inst(nome2)
            taxa_inicial = cot.taxa(valor1, valor2)
            taxa_inst = cot.taxa(papel1, papel2)
            janela1['output'].update(f"\n{time.strftime('%d/%m/%Y %H:%M:%S')}", append=True)
            janela1['output'].update(f"\n{nome1}: {papel1}\n{nome2}: {papel2}\nTaxa: {round((taxa_inst-taxa_inicial)*100, 3)}%\n\n", append=True)
            # Condicional de parada
            if taxa_inst >= taxa_inicial + taxa:
                meta = True
            else:
                meta = False
                pass
            start_time = time.time()
        if meta:
            meta = False
            running = False
            janela1['cancel_main'].update(button_color=('white', 'gray'))
            janela1['start'].update(button_color=('black', '#3de226'))
            janela1['status'].update('Desativado')
            janela1['output'].update('Meta atingida com sucesso!\n', append=True)

            dic_conf = sav.read_json('config')
            try:
                if dic_conf == False:
                    janela1['output'].update('Nenhum email encontrado\n', append=True)
                    pass
                else:
                    mil.enviar_email(dic_conf['token'], dic_conf['remetente'], dic_conf['email'], taxa_inst - taxa_inicial, nome1, nome2)
            except Exception as e:
                janela1['output'].update('Email não pode ser enviado.\n')
            sg.popup('Meta Atingida com sucesso!', icon=icon_path)
    
    # BOTÃO SALVAR DADOS DO MENU
    if window == janela1 and event == 'save_main':
        result = sav.create_json_menu(values['nome1'], values['nome2'], values['valor1'], values['valor2'], values['taxa'])
        if result == True:
            janela1['output'].update('Dados salvos com sucesso!\n', append=True)
        else:
            janela1['output'].update('Ocorreu um erro, verifique se os dados estão corretos.\n', append=True)

    # BOTÃO LIMPAR DADOS DO MENU
    if window == janela1 and event == 'cls':
        result = sav.create_json_menu('', '', '', '', '')
        if result == True:
            for i in ['nome1', 'nome2', 'valor1', 'valor2', 'taxa']:
                janela1[i].update('')
    
        