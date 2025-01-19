import PySimpleGUI as sg
import fcot as cot
import time


def janela_main():
    WIN_W = 30
    WIN_H = 50
    sg.theme('GrayGrayGray')
    layout_main = [
        [sg.Text('Nomes dos papéis '), sg.InputText(key='papel1', size=(int(WIN_W/2),1)), sg.InputText(key='papel2', size=(int(WIN_W/2),1))],
        [sg.Text('Valores de compra '), sg.InputText(key='valor1', size=(int(WIN_W/2),1)), sg.InputText(key='valor2', size=(int(WIN_W/2),1))],
        [sg.Text('Aumentar a taxa %'), sg.InputText(key='taxa', size=(int(WIN_W/2),1))],
        [sg.Push(), sg.Text('Desativado', key='status'), sg.Push()],
        [sg.Multiline(size=(50,10), key='output', disabled=True, autoscroll=True)],
        [sg.Text(key='1 papel atualizado em ')],
        [sg.Text(key='2 papel atualizado em ')],
        [sg.Text(key='Taxa atualizada em ')],
        [sg.Text(key='Última atualização')],
        [sg.Button('Configurações', key='config', button_color=('white', 'black')), sg.Button('Limpar', key='cls'), sg.Button('Salvar', key='save_main'), sg.Button('Cancelar', key='cancel_main', button_color=('white', 'grey')), sg.Button('Iniciar', key='start', button_color=('black', '#3de226'))]
    ]
    return sg.Window('Alarme de cotações da BOVESPA',layout_main, finalize=True)

def janela_config():
    WIN_W = 25
    WIN_H = 20
    sg.theme('GrayGrayGray')
    layout = [
        [sg.Text('email'), sg.InputText(size=(int(WIN_W),1))],
        [sg.Text('Token'), sg.InputText(size=(int(WIN_W),1))],
        [sg.Checkbox('Iniciar ao inicializar a máquina', key='inicializar')],
        [sg.Button('Cancelar', key='cancel_config'), sg.Button('Salvar', key='save_config')]
    ]
    return sg.Window('Configurações',layout, finalize=True)

janela1, janela2 = janela_main(), None
running = False
start_time = None
meta = False

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
        try:
            valor1 = cot.virgula(values['valor1'])
            valor2 = cot.virgula(values['valor2'])
            papel1 = cot.pregao_inst(values['papel1'])
            papel2 = cot.pregao_inst(values['papel2'])
            taxa = cot.virgula(values['taxa'])*0.01
            nome1 = values['papel1']
            nome2 = values['papel2']
            janela1['status'].update('Ativado')
            janela1['cancel_main'].update(button_color=('white', 'red'))
            janela1['start'].update(button_color=('white', 'grey'))
            running = True
            start_time = time.time()
            janela1['output'].update('')
        except:
            janela1['output'].update('Digite valores válidos\n', append=True)
    
    if window == janela1 and event == 'cancel_main':
        running = False
        janela1['cancel_main'].update(button_color=('white', 'grey'))
        janela1['start'].update(button_color=('black', '#3de226'))
        janela1['status'].update('Desativado')

    # A cada 60 segundos o cálculo é realizado
    if running:
        inst_time = time.time()
        if inst_time - start_time >= 10:
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
            sg.popup('Meta Atingida com sucesso!')
            meta = False
            running = False
            janela1['cancel_main'].update(button_color=('white', 'gray'))
            janela1['start'].update(button_color=('black', '#3de226'))
            janela1['status'].update('Desativado')
            janela1['output'].update('Meta atingida com sucesso!\n', append=True)


    try:
        print(inst_time - start_time)
    except:
        print('erro')

    
