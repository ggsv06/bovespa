import PySimpleGUI as sg

def janela_main(icon_path):
    WIN_W = 30
    WIN_H = 50
    sg.theme('GrayGrayGray')
    layout_main = [
        [sg.Text('Ativo Bovespa   '), sg.InputText(key='nome1', size=(int(WIN_W/2),1)), sg.InputText(key='nome2', size=(int(WIN_W/2),1))],
        [sg.Text('Preços             '), sg.InputText(key='valor1', size=(int(WIN_W/2),1)), sg.InputText(key='valor2', size=(int(WIN_W/2),1))],
        [sg.Text('Meta %            '), sg.InputText(key='taxa', size=(int(WIN_W/2),1))],
        [sg.Push(), sg.Text('--- Desativado ---', key='status', text_color='red'), sg.Push()],
        [sg.Text('Email      '), sg.Text('Nenhum', key='status_email', text_color='red'), sg.Push()],
        [sg.Text('Estratégia'), sg.Text('Nenhum', key='status_ativos', text_color='red'), sg.Push()],
        [sg.Multiline(size=(50,10), key='output', disabled=True, autoscroll=True)],
        [sg.Text('')],
        [sg.Button('Configurações', key='config'), sg.Button('Estratégia', key='files_main'), sg.Button('Cancelar', key='cancel_main', button_color=('white', 'grey')), sg.Button('Iniciar', key='start', button_color=('black', '#3de226'))]
    ]
    return sg.Window('Alarme de cotações da BOVESPA',layout_main, finalize=True, icon=icon_path)
# nome1, nome2 
# valor1, valor2 
# taxa 
# status 
# output
# config, save_main, cancel_main, start

def janela_config(icon_path):
    WIN_W = 25
    WIN_H = 20
    sg.theme('GrayGrayGray')
    layout_emails = [
        [sg.Text('Nome da predefinição'), sg.InputText(key='nome_pre', size=(int(WIN_W),1))],
        [sg.Text('Email destinatário     '), sg.InputText(key='email',size=(int(WIN_W),1))],
        [sg.Text('Email remetente       '), sg.InputText(key='remetente',size=(int(WIN_W),1))],
        [sg.Text('Senha remetente      '), sg.InputText(key='token',size=(int(WIN_W),1))],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_config'), sg.Button('Salvar', key='save_config', button_color=('black', '#3de226'))]
    ]
    layout_carregar = [
        [sg.Text('Selecione a predefinição')],
        [sg.OptionMenu(['Nenhum'], key='option_files', default_value='Nenhum')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_config2'), sg.Button('Excluir', key='del_load', button_color=('white', 'red')), sg.Button('Carregar', key='load_load', button_color=('white', '#6ab2e4'))]
    ]
    layout = [[sg.TabGroup([[sg.Tab("Emails", layout_emails), sg.Tab("Carregar", layout_carregar)]])]]
    return sg.Window('Configurações',layout, finalize=True, icon=icon_path)
    # TAB1 emails:
# nome_pre
# email
# remetente
# token
# cancel_config, save_config
    # TAB2 carregar:
# option_files
# del_load, load_load


def janela_files(icon_path):
    WIN_W = 25
    WIN_H = 20
    sg.theme('GrayGrayGray')
    layout_save = [
        [sg.Text('Nome da nova estratégia'), sg.Push()],
        [sg.InputText(key='file_name_menu', size=(int(WIN_W),1))],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_files_menu1'), sg.Button('Salvar', key='save_files_menu', button_color=('black', '#3de226'))]
    ]
    layout_load = [
        [sg.Text('Selecione a estratégia a ser carregada')],
        [sg.OptionMenu(['Nenhum'], key='option_files_menu', default_value='Nenhum')],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_files_menu2'), sg.Button('Excluir', key='del_files_menu2', button_color=('white', 'red')), sg.Button('Carregar', key='load_files_menu2', button_color=('black', '#6ab2e4'))]
    ]
    layout = [[sg.TabGroup([[sg.Tab("Salvar", layout_save), sg.Tab("Carregar", layout_load)]])]]
    return sg.Window('Arquivos', layout, finalize=True, icon=icon_path)
    # TAB 1: Salvar
# file_name_menu
# cancel_files_menu1, save_files_menu 

    # TAB 2: Carregar
# option_files_menu
# cancel_files_menu2, del_files_menu2, load_files_menu2
