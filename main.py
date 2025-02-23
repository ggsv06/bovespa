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
temp = False
finish_time = 0
# try:
    # predefinição = sav.read_json_keys('config')[0]
# except:
    # predefinição = 'Nenhum'

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
    if window == janela1 and event == 'config' and running == False:
        janela2 = janela_config(icon_path)
        # Auto preenchimento
        try:
            dic = sav.read_json('config', predefinição)
            if dic == False:
                pass
            else:
                try:
                    janela2['nome_pre'].update(predefinição)
                    janela2['email'].update(dic['email'])
                    janela2['remetente'].update(dic['remetente'])
                    janela2['token'].update(dic['token'])
                except:
                    pass
        except:
            pass
        # Atualizar opções do option menu
        try:
                keys = sav.read_json_keys('config')
                janela2['option_files'].update(values=keys, value=keys[0])
        except:
            pass
        
    # BOTÃO PÁGINA CONFIG CANCELAR
    if window == janela2 and event == 'cancel_config':
        janela2.hide()
    if window == janela2 and event == 'cancel_config2':
        janela2.hide()
    # BOTÃO PÁGINA CONFIG SALVAR
    if window == janela2 and event == 'save_config':
        predefinição = values['nome_pre']
        email = values['email']
        remetente = values['remetente']
        token = values['token']
        if '' in [predefinição, email, remetente, token]:
            sg.popup('Ocorreu um erro. Verifique se todos os dados foram inseridos.', icon=icon_path)
            continue
        result = sav.create_json_config(email, remetente, token, predefinição)
        # Atualizar status email
        try:
            janela1['status_email'].update(predefinição, text_color='green')
        except:
            pass
        sg.popup('Dados salvos com sucesso!', icon=icon_path)
        janela2.hide()
    # BOTÃO PÁGINA CONFIG DEL LOAD
    if window == janela2 and event == 'del_load':
        if values['option_files'] == values['nome_pre']:
            for i in ['nome_pre', 'email', 'remetente', 'token']:
                janela2[i].update('')
        result = sav.del_json_pre('config', values['option_files'])
        if result == False:
            sg.popup('Ocorreu um erro', icon=icon_path)
        else:
            keys = sav.read_json_keys('config')
            if len(keys) == 0:
                keys = ['Nenhum']
            janela2['option_files'].update(values=keys, value=keys[0])
            try:
                janela1['status_email'].update('Nenhum', text_color='red')
            except:
                pass
            sg.popup('Dados excluidos com sucesso!', icon=icon_path)

    # BOTÃO PÁGINA CONFIG CARREGAR LOAD
    if window == janela2 and event == 'load_load':
        try:
            predefinição = values['option_files']
            dic = sav.read_json('config', predefinição)
            janela2['nome_pre'].update(predefinição)
            janela2['email'].update(dic['email'])
            janela2['remetente'].update(dic['remetente'])
            janela2['token'].update(dic['token'])
            try:
                janela1['status_email'].update(predefinição, text_color='green')
            except:
                pass
            sg.popup('Dados carregados com sucesso!', icon=icon_path)
            janela2.hide()
        except:
            sg.popup('Não foi possível carregar os dados.', icon=icon_path)

    # BOTÃO ARQUIVOS
    if window == janela1 and event == 'files_main' and running == False:
        nome1, nome2, valor1, valor2, taxa = values['nome1'], values['nome2'], values['valor1'], values['valor2'], values['taxa']
        janela3 = janela_files(icon_path)
        # Atualizar opções do option menu
        try:
            keys = sav.read_json_keys('menu')
            janela3['option_files_menu'].update(values=keys, value=keys[0])
        except:
            pass
    # BOTÃO TAB SAVE: CANCELAR
    if window == janela3 and event == 'cancel_files_menu1':
        janela3.hide()
    if window == janela3 and event == 'cancel_files_menu2':
        janela3.hide()
    # BOTÃO TAB SAVE: SAVE
    if event == 'save_files_menu':
        nome_temp = values['file_name_menu']
        if nome_temp == '':
            sg.popup('Digite um nome válido.', icon=icon_path)
            continue
        try:
            sav.create_json_menu(nome1, nome2, valor1, valor2, taxa, nome_temp)
            janela1['status_ativos'].update(nome_temp, text_color='green')
            sg.popup('Dados salvos com sucesso!', icon=icon_path)
            janela3.hide()
        except:
            sg.popup('Ocorreu um erro.', icon=icon_path)
        # Atualizar status ativos
    # BOTÃO TAB LOAD: CARREGAR
    if window == janela3 and event == 'load_files_menu2':
        try:
            predefinição_menu = values['option_files_menu']
            dic = sav.read_json('menu', predefinição_menu)
            # Auto preenchimento
            janela1['nome1'].update(dic['nome1'])
            janela1['nome2'].update(dic['nome2'])
            janela1['valor1'].update(dic['valor1'])
            janela1['valor2'].update(dic['valor2'])
            janela1['taxa'].update(dic['taxa'])
            # Atualizar status
            janela1['status_ativos'].update(predefinição_menu, text_color='green')
            sg.popup('Dados carregados com sucesso!', icon=icon_path)
            janela3.hide()
        except:
            sg.popup('Não foi possível carregar os dados.', icon=icon_path)
    # BOTÃO PÁGINA CONFIG DEL LOAD
    if event == 'del_files_menu2':
        result = sav.del_json_pre('menu', values['option_files_menu'])
        if result == False:
            sg.popup('Ocorreu um erro', icon=icon_path)
        else:
            keys = sav.read_json_keys('menu')
            if len(keys) == 0:
                keys = ['Nenhum']
            janela3['option_files_menu'].update(values=keys, value=keys[0])
            janela1['status_ativos'].update('Nenhum', text_color='red')
            sg.popup('Dados excluidos com sucesso!', icon=icon_path)
    
    # COMANDOS JANELA MAIN
    if window == janela1 and event == 'start':
        try:
            valor1 = cot.virgula(values['valor1'])
            valor2 = cot.virgula(values['valor2'])
            taxa = cot.virgula(values['taxa'])*0.01
            nome1 = values['nome1'].upper()
            nome2 = values['nome2'].upper()
            janela1['status'].update('--- Ativado ---', text_color='green')
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
        janela1['status'].update('--- Desativado ---', text_color='red')
        janela1['output'].update(text_color='black')

    # A cada 60 segundos o cálculo é realizado
    if running:
        inst_time = time.time()
        if inst_time - start_time >= 2:
            if inst_time - finish_time >= 1800 or inst_time - finish_time == inst_time:
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
        # Disparar email
        if meta:
            meta = False
            running = True
            finish_time = time.time()
            # janela1['cancel_main'].update(button_color=('white', 'gray'))
            # janela1['start'].update(button_color=('black', '#3de226'))
            # janela1['status'].update('--- Desativado ---', text_color='red')
            janela1['output'].update('META ATINGIDA COM SUCESSO!\n', text_color='green', append=True)
            try:
                dic_conf = sav.read_json('config', predefinição)
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
            # sg.popup('Meta Atingida com sucesso!', icon=icon_path)