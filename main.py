import fcot as cot
import fsav as sav
import fmsg as mil
from flayout import *
import time
import sys
import os

# CAMINHO DO ICO
if getattr(sys, 'frozen', False):  # If running as a compiled .exe
    icon_path = os.path.join(sys._MEIPASS, 'img.ico')
else:  # If running as a .py file
    icon_path = 'img.ico'

janela1, janela2, janela3 = janela_main(icon_path), None, None
running = False
start_time = None
meta = False

#dic = sav.read_json('menu')
#if dic == False:
    #pass
#else:
    #try:
        #for i in ['nome1', 'nome2', 'valor1', 'valor2', 'taxa']:
            #janela1[i].update(dic[i])
    #except:
        #pass

while True:
    window, event, values = sg.read_all_windows(timeout=1000)
    # X
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela2 and event == sg.WIN_CLOSED:
        janela2.hide()
    if window == janela3 and event == sg.WIN_CLOSED:
        janela3.hide()

    # BOTÃO PÁGINA MAIN CONFIG
    if window == janela1 and event == 'config':
        janela2 = janela_config(icon_path)
        # Auto preenchimento
        try:
            dic = sav.read_json('config', file_name)
            if dic == False:
                pass
            else:
                try:
                    janela2['email'].update(dic['email'])
                    janela2['remetente'].update(dic['remetente'])
                    janela2['token'].update(dic['token'])
                except:
                    pass
        except:
            pass

    # BOTÃO PÁGINA CONFIG CANCELAR
    if window == janela2 and event == 'cancel_config':
        janela2.hide()
    # BOTÃO PÁGINA CONFIG SALVAR
    if window == janela2 and event == 'save_config':
        try:
            email = values['email']
            remetente = values['remetente']
            token = values['token']
        except:
            sg.popup('Ocorreu um erro. Verifique se todos os dados foram inseridos.', icon=icon_path)
        result = sav.create_json_config(values['email'], values['remetente'], values['token'], values['file_name'])
        if result == False:
            sg.popup('Ocorreu um erro. Verifique se todos os dados foram inseridos.', icon=icon_path)
        janela2.hide()
    # BOTÃO PÁGINA CONFIG SALVAR COMO
    if window == janela2 and event == 'files_config':
        janela3 = janela_files(icon_path)

    # BOTÃO TAB SAVE: CANCELAR
    if window == janela3 and event == 'cancel_files1':
        janela3.hide()
    # BOTÃO TAB SAVE: SAVE
    if window == janela3 and event == 'save_files':
        try:
            file_name = values['file_name']
            sav.create_json_config(email, remetente, token, file_name)
            sg.popup('Dados salvos com sucesso!', icon=icon_path)
            janela3.hide()
        except:
            sg.popup('1Ocorreu um erro. Verifique se todos os dados foram inseridos.', icon=icon_path)
    
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
            janela1['output'].update(f"\n{nome1}: {papel1:.2f}\n{nome2}: {papel2:.2f}\nTaxa: {taxa_inst-taxa_inicial:.3%}\n\n", append=True)
            # Condicional de parada
            if taxa >= 0:
                if taxa_inst >= taxa_inicial + taxa:
                    meta = True
                else:
                    meta = False
                    pass
            else:
                if taxa_inst <= taxa_inicial + taxa:
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
            try:
                dic_conf = sav.read_json('config', values_file_name)
            except:
                pass
            try:
                if dic_conf == False:
                    janela1['output'].update('Nenhum email encontrado\n', append=True)
                    pass
                else:
                    mil.enviar_email(dic_conf['token'], dic_conf['remetente'], dic_conf['email'], taxa, nome1, nome2)
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
    
        