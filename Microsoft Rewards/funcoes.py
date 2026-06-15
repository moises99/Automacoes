from config import LINKS,XPATH_PAGINA,VARIAVEIS,CHAVE_ID
from personalizacao import texto_personalizado
import datetime as dt
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from rich.progress import Progress, track
from rich import print
from rich.table import Table
from rich.panel import Panel

#Responsável por executar as funcionalidades da página
def func_principal():
    '''
    Função principal responsável por executar toda a rotina.
    '''
    print(texto_personalizado(' Inicializando... '.upper()))
    arquivo_log = gera_txt()
    load(0.01)

    #Bloco responsável por executar algumas funções com barra de progresso
    with Progress() as progresso:
        tarefa = progresso.add_task(description="")
        while True:
            progresso.update(tarefa,advance=25,description="[green]Verificando pontos...")
            pontos_atuais = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
            print(texto_personalizado(f' PONTOS ATUAIS: {pontos_atuais} '))
            progresso.update(tarefa,advance=25,description="[green]Verificando nivel de membro...")
            pontos_nivel_membro = verifica_membro(LINKS['home_page'] , XPATH_PAGINA["membro"])
            if pontos_nivel_membro == 60:
                nome_nivel_membro = "OURO"
            else:
                nome_nivel_membro = "PRATA"
            print(texto_personalizado(F' VOCÊ É MEMBRO {nome_nivel_membro} COM {pontos_nivel_membro} PONTOS DIARIOS DE PESQUISAS ')) #if pontos_nivel_membro == 60 else print(texto_personalizado(F' VOCÊ É MEMBRO PRATA COM {pontos_nivel_membro} PONTOS DIARIOS DE PESQUISAS '))
            progresso.update(tarefa,advance=45,description="[green]Coletando informações...")
            noticias_func = coleta_noticias()
            progresso.update(tarefa,advance=5,description="[green]Concluindo",transient=True)
            meu_maximo_de_pontos = pontos_atuais + pontos_nivel_membro
            print(texto_personalizado(f' Total de {len(noticias_func[0])} notícias'.upper()))
            break
    print(texto_personalizado(' Iniciando pesquisas '.upper()))
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    #Bloco respondavel por executar as pesquisar e gravar as informações no arquivo de texto
    for pos,titulo in track(enumerate(noticias_func[0]),description="[purple]Pesquisando...",transient=True):
        try:
            with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{CHAVE_ID["chave"]}\nLink: https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}\n')
                print()
        except FileNotFoundError:
            print(f'Arquivo ou diretório não encontrado, verifique o caminho {arquivo_log}.\nSeguiremos com as pesquisas')
            print()
        driver.get(f'https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}')
        load(0.05,f'Manchete {pos+1}: {titulo} ')
        
        #Bloco responsável por verificar se o limite de pontos na posição 30 foram atingido e na posição 50 ou maior foram atingido, se não, verificará a cada pesquisa.
        if pos == 30 or pos >= 50:
            with Progress() as progresso:
                tarefa = progresso.add_task(description="")
                while True:
                    progresso.update(tarefa,advance=5,description="[green]Verificando pontos...")
                    pontos_atuallizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
                    progresso.update(tarefa,advance=95,description="Pontos atualizado...")
                    break
            maximo_ponto =  pontos_atuallizados >= meu_maximo_de_pontos
            pontos_faltando = meu_maximo_de_pontos - pontos_atuallizados
            if maximo_ponto:
                print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
                print(resumo(nome_nivel_membro,pontos_nivel_membro,pontos_atuais,pontos_atuallizados,pos))
                break
            else:
                print()
                print(texto_personalizado(f' Necessários mais {pontos_faltando} pontos').upper())
            
        #Miau
        if pontos_faltando == 3:
            VARIAVEIS["controle_pontos"] +=1
            print(f'Tentativa: {VARIAVEIS["controle_pontos"]}')
            if VARIAVEIS["controle_pontos"] == 5:
                print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
                print(resumo(nome_nivel_membro,pontos_nivel_membro,pontos_atuais,pontos_atuallizados,pos))
                break


    print(texto_personalizado(f'Rotina finalizada').upper())
    print(texto_personalizado(f'ARQUIVO SALVO EM {arquivo_log}'))
    driver.quit()


#Retorna a quantidade de pontos do usuário
def verifica_pontos(link_pagina , xpath_pontos) -> int:
    '''
    Funcão responsável por coletar os pontos atuais.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_pontos: o caminho do xpath dos pontos
    '''
    
    try:
        #Abre navegador em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        driver_segundo_plano.add_argument("--headless=new")
        driver_pontos = webdriver.Edge(options=driver_segundo_plano)
        driver_pontos.get(link_pagina)
        pontos = driver_pontos.find_element(By.XPATH,xpath_pontos)
        #converte o float para int
        pontos = pontos.text.replace('.','')
        driver_pontos.quit()
        pontos = int(pontos)
        return pontos
    except IndentationError as e:
        print(f'Erro de indentação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt as e:
        print(f'Interrompido pelo usuário: {e}')
    except NameError as e:
        print(f'Variavel nao definida: {e}')

#Retorna a quantidade de pontos do usuário
def verifica_membro(link_pagina,xpath_membro) -> int:
    '''
    Funcão responsável por verificar o nivel de membro.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_membro: o caminho do xpath nivel (Ouro,Prata etc...) 
    *Use termos em inglês como Gold e Silver
    '''
    try:
        
        #Abre navegado em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        driver_segundo_plano.add_argument("--headless=new")
        driver_membro = webdriver.Edge(options=driver_segundo_plano)
        driver_membro.get(link_pagina)
        membro = driver_membro.find_element(By.XPATH,xpath_membro)
        membro = membro.text
        driver_membro.quit()
        # print(texto_personalizado('Iniciado a verificação de nivel Membro'.upper()))
        if membro == 'Gold':
            membro = int(60)
            return membro
        if membro == 'Silver':
            membro = int(30)
            return membro
    except IndentationError as e:
        print(f'Erro de identação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt:
        print(f'Interrompido pelo usuário')
    except NameError as e:
        print(f'Variavel no definida {e}')



#Gera um arquivo contendo a manche e os links de cada pesquisa
def gera_txt():
    '''
    Gera um arquivo txt com as manchetes e links de cada notícia.
    E retornar o nome do arquivo
    '''
    try:
        #Bloco para criar o arquico concatenando a data do dia com o nome do arquivo
        arquivo_log = VARIAVEIS["local_arquivo"] + VARIAVEIS["nome_arquivo"]
        with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
            arquivo.write(f'====== PESQUISAS DATA {dt.datetime.now().strftime("%d/%m/%Y")} ======\n')
    except KeyError as e:
        print(f'Chave inexistente: {e}')
    except FileNotFoundError as e:
        print(f'Arquivo ou diretório não encontrado, verifique o caminho {VARIAVEIS["local_arquivo"]}.\nSeguiremos apenas com as pesquisas.')
        print()
    return arquivo_log


#Cria a conexao com o site *Necessário estar logado e Rolagem automatica da Pagina
def driver_edge():
    '''
    Abre uma pagina web recebendo o link atravrés da variavel LINKS["msn_news"].
    Faz uma rolagem automatica de 2 em 2 segundo.
    E retorna a pagina aberta.
    '''
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get(LINKS["msn_news"])
    for _ in track(range(12),description="[green]Aguarde...",transient=True):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return driver


#Coleta o título das noticias
def coleta_noticias():
    '''
    Coleta as manchetes da pagina.
    '''
    driver = driver_edge()
    titulo_noticia = []
    lista_noticia_formatada = []
    titulos_noticia = driver.find_elements(By.XPATH,"//a[@class='title']")
    for titulos in track(titulos_noticia, description=" [green]Gerando lista... "):
        manchete = f"{titulos.text}"
        if len(manchete) > 5:
            titulo_noticia.append(manchete)
            noticias_formatadas = str(titulos.text).replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            lista_noticia_formatada.append(noticias_formatadas)
    print()
    driver.quit()
    return titulo_noticia,lista_noticia_formatada


def load(tempo = 0.02,texto ="[green]Processando..."):
    '''
    Função simples apenas para gerar uma barra de progresso.
    Recebe parametros opcionais, um tempo e um texto respectivamente.
    '''
    with Progress() as progress:
        task1 = progress.add_task(texto,total = 100)
        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(tempo)



def resumo(nivel_membro=0,pontos_membro=0,pontos=0,pontos_atualizados=0,total_pesquisas=0):
    table = Table(expand=True)
    table.add_column("Nivel de Membro", justify="center")
    table.add_column("Pontos de Membro", justify="center")
    table.add_column("Pontos Anteriores", justify="center")
    table.add_column("Pontos Atualizados", justify="center")
    table.add_column("T. de Pesquisas Realizadas", justify="center")
    table.add_row(str(nivel_membro),str(pontos_membro),str(pontos),str(pontos_atualizados),str(total_pesquisas))
    painel = Panel(table,title=texto_personalizado("Resumo").upper(),width=120,subtitle="Volte amanhão para ganhar novos pontos",style="bold")
    return painel

