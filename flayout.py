import PySimpleGUI as sg

def janela_main(icon_path):
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
        [sg.Button('Configurações', key='config'), sg.Button('Arquivos', key='save_main'), sg.Button('Cancelar', key='cancel_main', button_color=('white', 'grey')), sg.Button('Iniciar', key='start', button_color=('black', '#3de226'))]
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
        [sg.Button('Cancelar', key='cancel_config', button_color=('white', 'red')), sg.Button('Salvar', key='save_config', button_color=('black', '#3de226'))]
    ]
    layout_carregar = [
        [sg.Text('Selecione a predefinição')],
        [sg.OptionMenu(['Nenhum'], key='option_files', default_value='Nenhum')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button('Excluir', key='del_load', button_color=('white', 'red')), sg.Button('Carregar', key='load_load', button_color=('white', '#6ab2e4'))]
    ]
    layout = [[sg.TabGroup([[sg.Tab("Emails", layout_emails), sg.Tab("Carregar", layout_carregar)]])]]
    return sg.Window('Configurações',layout, finalize=True, icon=icon_path)
# email
# remetente
# token
# files_config, cancel_config, save_config


def janela_files(icon_path):
    WIN_W = 25
    WIN_H = 20
    sg.theme('GrayGrayGray')
    layout_save = [
        [sg.Text('Nome da nova predefinição'), sg.Push()],
        [sg.InputText(key='file_name', size=(int(WIN_W),1))],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_files1', button_color=('white', 'red')), sg.Button('Salvar', key='save_files', button_color=('black', '#3de226'))]
    ]
    layout_load = [
        [sg.Text('Selecione a predefinição a ser carregada')],
        [sg.OptionMenu(['Selecionar'], key='option_files', default_value='Selecionar')],
        [sg.Text('')],
        [sg.Button('Cancelar', key='cancel_files2'), sg.Button('Excluir', key='del_files2', button_color=('white', 'red')), sg.Button('Carregar', key='load_files2', button_color=('black', '#3de226'))]
    ]
    layout = [[sg.TabGroup([[sg.Tab("Salvar", layout_save), sg.Tab("Carregar", layout_load)]])]]
    return sg.Window('Arquivos', layout, finalize=True, icon=icon_path)
# TAB 1: Salvar
# file_name
# cancel_files1, save_files 

# TAB 2: Carregar
# option_files
# cancel_files2, del_files2, load_files2
