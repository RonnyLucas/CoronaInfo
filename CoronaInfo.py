import PySimpleGUI as sg
import requests

sg.theme('DarkBlue1')   #Tema do PySimpleGUI

url = ('https://pomber.github.io/covid19/timeseries.json')  #Request do JSON.
req = requests.get(url, timeout = 3_000)
retorno = req.json()

def pesquisar():
    layout_selecao = [ [sg.Text('Digite o nome do país em inglês (sem preencher = Brazil):')],  #Layout da primeira janela.
                       [sg.InputText()],
                       [sg.Submit(), sg.Cancel()]
                    ] 
    janela = sg.Window('Corona - Info', layout_selecao)
    eventos, texto = janela.read()  # Retorno da GUI.
    if eventos[0] == 'C':
        quit()
    pais = texto[0].strip().title() # Tirar espaços em branco, capitalizar a 1a letra.
    if not pais:
        pais = 'Brazil'       
    if pais in retorno:
        dicionario = retorno[pais]
    else:
        layout_erro = [[sg.Text('País não encontrado! Pesquise novamente!'), sg.Ok()]]
        erro = sg.Window('Não encontrado!', layout_erro)
        erro.read()
        erro.Close()
        return None
    info = dicionario[-1]   # Inverter para acessar os últimos dados adicionados..
    janela.Close()
    return pais, info['date'], info['confirmed'], info['deaths'], info['recovered']
    

def exibir(ret_pesquisa):
    if ret_pesquisa == None:    # Caso receba None, retorna 'P' ao loop de eventos.
        return 'P'
    pais, data, confirmados, baixas, curados = ret_pesquisa
    layout_resposta = [ [sg.Text(f'País: {pais}')],
                  [sg.Text(f'Data dos dados: {data}')],
                  [sg.Text(f'Casos confirmados: {confirmados}')],
                  [sg.Text(f'Pessoas oficialmente curadas: {curados}')],
                  [sg.Text(f'Número de baixas oficial: {baixas}')],
                  [sg.Button('Ok'), sg.Button('Pesquisar outro país')] 
            ]
    resp = sg.Window(f'Resultados - {pais}', layout_resposta)
    eventos, retorno = resp.read()  # Retorno da GUI.
    resp.close()
    return(eventos[0])  # Retorna apenas o primeiro caracter da opção selecionada.

ret = ''
while ret != 'O':   # Loop de eventos, [O]k -> segue execução, [P]esquisar... -> interrompe.
        ret = exibir(pesquisar())
quit()