import PySimpleGUI as sg
import fcot as cot
import time


def janela_main():
    WIN_W = 30
    WIN_H = 50
    sg.theme('Default')
    layout_main = [
        [sg.Text('Nomes dos papéis'), sg.InputText(key='papel1', size=(int(WIN_W/2),1)), sg.InputText(key='papel2', size=(int(WIN_W/2),1))],
        [sg.Text('Valores de compra'), sg.InputText(key='valor1', size=(int(WIN_W/2),1)), sg.InputText(key='valor2', size=(int(WIN_W/2),1))],
        [sg.Text('Aumentar a taxa %'), sg.InputText(key='taxa', size=(int(WIN_W/2),1))],
        [sg.Button('Configurações', key='config'), sg.Button('Limpar', key='cls'), sg.Button('Salvar', key='save_main'), sg.Button('Cancelar', key='cancel_main'), sg.Button('Iniciar', key='start')],
        [sg.Text(key='1 papel atualizado em ')],
        [sg.Text(key='2 papel atualizado em ')],
        [sg.Text(key='Taxa atualizada em ')],
        [sg.Text(key='Última atualização')]
    ]
    return sg.Window('Alarme de cotações da BOVESPA',layout_main, finalize=True)

def janela_config():
    WIN_W = 25
    WIN_H = 20
    sg.theme('Default')
    layout = [
        [sg.Text('email'), sg.InputText(size=(int(WIN_W/2),1))],
        [sg.Text('Token'), sg.InputText(size=(int(WIN_W/2),1))],
        [sg.Checkbox('Iniciar ao inicializar a máquina', key='inicializar')],
        [sg.Button('Cancelar', key='cancel_config'), sg.Button('Salvar', key='save_config')]
    ]
    return sg.Window('Configurações',layout, finalize=True)

janela1, janela2 = janela_main(), None

while True:
    window, event, values = sg.read_all_windows()
    # X
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela2 and event == sg.WIN_CLOSED:
        janela2.hide()
    # BOTÃO CONFIGURAÇÕES
    if window == janela1 and event == 'config':
        janela2 = janela_config()
    # BOTÃO PÁGINA CONFIG CANCELAR
    if window == janela2 and event == 'cancel_config':
        janela2.hide()
    # BOTÃO PÁGINA CONFIG SALVAR
    if window == janela2 and event == 'save_config':
        # Construir lógica de save das informações
        if values['inicializar'] == True:
            sg.popup('teste')
            # Construir lógica de save das informações
        janela2.hide()
    
    # COMANDOS JANELA MAIN
    if window == janela1 and event == 'start':
        while True:
            if event == 'cancel_main':
                sg.popup('Processo cancelado com sucesso')
                break
            taxa_inicial = cot.taxa(cot.virgula(values['valor1']), cot.virgula(values['valor2']))
            taxa_inst = cot.taxa(cot.pregao_inst(values['papel1']), cot.pregao_inst(values['papel2']))
            # Condicional de parada
            if taxa_inst >= taxa_inicial + cot.virgula(values['taxa'])*0.01:
                meta = True
                break
            else:
                meta = False
                pass
        if meta:
            sg.popup('Meta Atingida com sucesso!')

    
