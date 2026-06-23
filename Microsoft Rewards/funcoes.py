from config import LINKS,XPATH_PAGINA,VARIAVEIS,CHAVE_ID
from personalizacao import texto_personalizado
import datetime as dt
import time
from time import sleep
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
    try:
        print(texto_personalizado(' Inicializando... '.upper()))
        arquivo_log = gera_txt()
        load(0.01,visibilidade = False)

        #Bloco responsável por executar algumas funções com barra de progresso
        with Progress() as progresso:
            tarefa = progresso.add_task(description="",transient=True)
            while True:
                progresso.update(tarefa,advance=25,description="[yellow]Verificando pontos...")
                pontos_atuais = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
                print(texto_personalizado(f' PONTOS ATUAIS: {pontos_atuais[0]} '))
                progresso.update(tarefa,advance=25,description="[yellow]Verificando nivel de membro...")
                pontos_nivel_membro = verifica_membro(LINKS['home_page'] , XPATH_PAGINA["membro"])
                if pontos_nivel_membro == 60:
                    nome_nivel_membro = "OURO"
                else:
                    nome_nivel_membro = "PRATA"
                print(texto_personalizado(F' VOCÊ É MEMBRO {nome_nivel_membro} COM {pontos_nivel_membro} PONTOS DIARIOS DE PESQUISAS ')) #if pontos_nivel_membro == 60 else print(texto_personalizado(F' VOCÊ É MEMBRO PRATA COM {pontos_nivel_membro} PONTOS DIARIOS DE PESQUISAS '))
                progresso.update(tarefa,advance=45,description="[yellow]Coletando informações...")
                noticias_func = coleta_noticias()
                progresso.update(tarefa,advance=5,description="[green]Concluindo")
                meu_maximo_de_pontos = pontos_atuais[0] + pontos_nivel_membro
                print(texto_personalizado(f' Total de {len(noticias_func[0])} notícias'.upper()))
                break
        print(texto_personalizado(' Iniciando pesquisas '.upper()))
        driver_edge = Options()
        if not VARIAVEIS["ver_processo"]:
            driver_edge.add_argument("--headless=new")
        driver = webdriver.Edge(options=driver_edge)
    except TypeError as e:
        print(f'Erro: {e}')
        exit()
    #Bloco respondavel por executar as pesquisar e gravar as informações no arquivo de texto
    for pos,titulo in track(enumerate(noticias_func[0]),description="[purple]Pesquisando...",transient=True):
        try:
            with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{CHAVE_ID["chave"]}\nLink: https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}\n')
                print()
        except FileNotFoundError:
            print(f'Arquivo ou diretório não encontrado, verifique o caminho {arquivo_log}.\nSeguiremos com as pesquisas')
            print()
        ""
        #driver.get(f'https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}')
        load(0.01,f'Notícia {pos+1}: [link=https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}]{titulo}[/link]')
        #Bloco responsável por verificar se o limite de pontos.
        VARIAVEIS["controle_pontos"] +=3
        print('VARIAVEIS["controle_pontos"]:  ',VARIAVEIS["controle_pontos"])
        if VARIAVEIS["controle_pontos"] == 60:
            with Progress() as progresso:
                tarefa = progresso.add_task(description="")
                while True:
                    progresso.update(tarefa,advance=5,description="[yellow]Verificando pontos...")
                    pontos_atualizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
                    progresso.update(tarefa,advance=95,description="[green]Pontos atualizado...")
                    break
            maximo_ponto =  int(pontos_atualizados[0]) >= int(meu_maximo_de_pontos)
            pontos_faltando = int(meu_maximo_de_pontos) - int(pontos_atualizados[0])
            print('pontos_faltando',pontos_faltando)
            if maximo_ponto:
                if pontos_atualizados[2]:
                    VARIAVEIS["d_diariamente"] = definido_diariamente(LINKS["home_page"])
                    VARIAVEIS["c_ganhando"] = continue_ganhando(LINKS["home_page"])
                    print(f'Você tem {pontos_atualizados[1]} pontos para reivindicar')
                    reivindicar(LINKS["home_page"])
                    print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
                    break
                else:
                    print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
                    break
            else:
                #Retorna uma "posição" da diferença de pontos exemplo: 60(pontos_nivel_membro) - 6(pontos_faltando) = 54, me retornar a posica 54 que no caso seira mais 2 duas pesquisa para fechar os 60 pontos
                VARIAVEIS["controle_pontos"] = pontos_nivel_membro - pontos_faltando
                print('VARIAVEIS["controle_pontos"]:  ',VARIAVEIS["controle_pontos"])
                print(texto_personalizado(f' Necessários mais {pontos_faltando} pontos').upper())
            #Verifica se há pontos a serem reivindicados e se faltam apenas tres pontos para chegar ao limite de pontos.
            #Caso não atinja o limite ele pega os pontos que faltam e faz novas tentativas até atingir o máximo de pontos.
            #Se faltar apenas tres pontos ira realizar tres tentativas de pesquisas e entao reivindicara os pontos disponiveis completando os seus pontos diarios.
            if pontos_faltando == 3:
                VARIAVEIS["controle_tres_pontos"] +=1
                print(texto_personalizado(f'Tentativa: {VARIAVEIS["controle_tres_pontos"]}/3'))
                if VARIAVEIS["controle_tres_pontos"] == 3:
                    pontos_atualizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
                    if pontos_atualizados[2]:
                        VARIAVEIS["d_diariamente"] = definido_diariamente(LINKS["home_page"])
                        VARIAVEIS["c_ganhando"] = continue_ganhando(LINKS["home_page"])
                        print(f'Você tem {pontos_atualizados[1]} pontos para reivindicar')
                        reivindicar(LINKS["home_page"])
                    print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
                    break

    print(resumo(nome_nivel_membro,pontos_nivel_membro,pontos_atuais[0],pontos_atualizados[0],pontos_atualizados[1],pos,VARIAVEIS["d_diariamente"],VARIAVEIS["c_ganhando"]))
    print(texto_personalizado(f'ARQUIVO SALVO EM {arquivo_log}'))
    print(texto_personalizado(f'Rotina finalizada').upper().center(120))
    driver.quit()

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
        if not VARIAVEIS["ver_processo"]:
            driver_segundo_plano.add_argument("--headless=new")
        driver_membro = webdriver.Edge(options=driver_segundo_plano)
        driver_membro.get(link_pagina)
        membro = driver_membro.find_element(By.XPATH,xpath_membro)
        membro = membro.text
        driver_membro.quit()
        if membro == 'Membro Ouro':
            membro = int(60)
            return membro
        if membro == 'Membro Prata':
            membro = int(30)
            return membro
        else:
            return "Não identificamos o mebro"
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
    if not VARIAVEIS["ver_processo"]:
        driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get(LINKS["msn_news"])
    for _ in track(range(12),description="[yellow]Aguarde...",transient=True):
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
    for titulos in track(titulos_noticia, description=" [yellow]Gerando lista... ",transient=True):
        manchete = f"{titulos.text}"
        if len(manchete) > 5:
            titulo_noticia.append(manchete)
            noticias_formatadas = str(titulos.text).replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            lista_noticia_formatada.append(noticias_formatadas)
    print()
    driver.quit()
    if len(titulo_noticia) > 20:
        return titulo_noticia,lista_noticia_formatada
    else:
        return f"Numero de noticias insulficiente: ({len(titulo_noticia)})"

def load(tempo = 0.02,texto ="[green]Processando...", visibilidade=True):
    '''
    Função simples apenas para gerar uma barra de progresso.
    Recebe parametros opcionais, um tempo,um texto, e se será mostrada respectivamente.
    '''
    with Progress() as progress:
        task1 = progress.add_task(texto,total = 100,visible=visibilidade)
        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(tempo)

#Mostra um resumo das atividas após concluir a rotina
def resumo(nivel_membro="N/A",pontos_membro="N/A",pontos="N/A",pontos_atualizados="N/A",pontos_reivindicados="N/A",total_pesquisas="N/A",definidos_diariamente="N/A",cont_ganhando="N/A"):
    with Progress() as progresso:
        tarefa_resumo = progresso.add_task(description="",transient=True)
        progresso.update(tarefa_resumo,advance=25,description="[yellow]Atualizando pontos...")
        pontos_atualizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
        # cont_ganhando = continue_ganhando(LINKS["home_page"])
        # definidos_diariamente = definido_diariamente(LINKS["home_page"])
        pontos_atualizados= pontos_atualizados[0]
        table = Table(expand=True)
        table.add_column("Nivel de Membro", justify="center")
        table.add_column("Pontos de Membro", justify="center")
        table.add_column("Pontos Anteriores", justify="center")
        table.add_column("Pontos Atualizados", justify="center")
        table.add_column("Pontos Reivindicados", justify="center")
        table.add_column("N. de Pesquisas Realizadas", justify="center")
        table.add_column("Desafios Diarios", justify="center")
        table.add_column("Continue Ganhando", justify="center")
        table.add_row(str(nivel_membro),str(pontos_membro),str(pontos),str(pontos_atualizados),str(pontos_reivindicados),str(total_pesquisas),str(definidos_diariamente),str(cont_ganhando))
        painel = Panel(table,title=texto_personalizado("Resumo").upper(),width=120,subtitle="Volte amanhão para ganhar novos pontos",style="bold")
        progresso.update(tarefa_resumo,advance=74,description="[yellow]Gerando resumo...")
        progresso.update(tarefa_resumo,advance=74,description="[green]Concluido")
        return painel

#Funcão responsável por coletar os pontos atuais e se há pontos para reivindicar.
def verifica_pontos(link_pagina , xpath_pontos):
    '''
    Funcão responsável por coletar os pontos atuais e se há pontos para reivindicar.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_pontos: o caminho do xpath dos pontos
    '''
    
    try:
        #Abre navegador em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        if not VARIAVEIS["ver_processo"]:
            driver_segundo_plano.add_argument("--headless=new")
        driver_pontos = webdriver.Edge(options=driver_segundo_plano)
        driver_pontos.get(link_pagina)
        pontos = driver_pontos.find_elements(By.XPATH,xpath_pontos)
        lista_pontos = [pontos.text.replace(".","") for pontos in pontos]
        #converte o float para int
        pontos = int(lista_pontos[0])
        pontos_reinvidicar = int(lista_pontos[1])
        flag_pontos_reivindicar = False
        if pontos_reinvidicar >= 1: 
            flag_pontos_reivindicar = True
        driver_pontos.quit()
        return int(pontos),int(pontos_reinvidicar),bool(flag_pontos_reivindicar)
    
    except IndentationError as e:
        print(f'Erro de indentação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt as e:
        print(f'Interrompido pelo usuário: {e}')
    except NameError as e:
        print(f'Variavel nao definida: {e}')

#Reivindica os pontos dosponiveis
def reivindicar(home_page):
    '''
    Reivindica os pontos dosponiveis
    '''
    try:
        with Progress() as progresso:
            tarefa_reivindicar = progresso.add_task(description="[yellow]Reivindicando pontos...")
            while True:
                progresso.update(tarefa_reivindicar,advance=5,description="[yellow]Reivindicando pontos...")
                driver_edge = Options()
                if not VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(home_page)
                clicar = driver.find_element(By.XPATH,XPATH_PAGINA["reivindicar"])
                time.sleep(5)
                driver.implicitly_wait(5)
                clicar.click()
                time.sleep(5)
                driver.implicitly_wait(5)
                clicar = driver.find_element(By.XPATH,XPATH_PAGINA["ganhar_mais_pontos"])
                time.sleep(5)
                driver.implicitly_wait(5)
                clicar.click()
                progresso.update(tarefa_reivindicar,advance=95,description="[green]Pontos reivindicados")
                driver.quit()
                break
    except Exception as e:
        print(f'Não foi possivel reinvidicar os pontos error: {e}')

def definido_diariamente(home_page):
    '''
    Desafios diarios
    '''
    try:
        with Progress() as progresso:
            tarefa_definido_diariamente = progresso.add_task(description='[yellow]Fazendo: "Desafios diários..."')
            while True:
                progresso.update(tarefa_definido_diariamente,advance=5,description='[yellow]Fazendo: "Desafios diários..."')
                driver_edge = Options()
                if not VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(home_page)
                time.sleep(10)
                elementos = driver.find_elements(By.XPATH,XPATH_PAGINA['definidos_diariamente'])
                time.sleep(10)
                for c in track(range(3),total=100,description='[yellow]Concluindo: "Desafios diários"...',transient=True):
                    elementos[c].click()

                    progresso.update(tarefa_definido_diariamente,advance=30,description=f"[yellow]Conjunto{[c+1]}")
                    time.sleep(10)
                progresso.update(tarefa_definido_diariamente,advance=5,description="[green]Desafios conluídos")
                driver.quit()
                break
    except Exception as e:
        print(f'Não foi possivel realizar o "Conjutos Diarios!" error:\n {e}')

def continue_ganhando(ganhe_mais):
    try:
        with Progress() as progresso:
            tarefa_continue_ganhando = progresso.add_task(description='[yellow]Fazendo: "Continue ganhando"...')
            while True:
                progresso.update(tarefa_continue_ganhando,advance=30,description='[yellow]Fazendo: "Continue ganhando"...')
                driver_edge = Options()
                if not VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(ganhe_mais)
                time.sleep(10)
                ganhar = driver.find_elements(By.XPATH,XPATH_PAGINA['ganhe_mais'])
                time.sleep(10)
                ganhar[1].click()
                time.sleep(10)
                driver.get(LINKS["continue_ganhando"])
                time.sleep(10)
                progresso.update(tarefa_continue_ganhando,advance=60,description="[yellow]Fazendo desafios diários...")
                c_ganhar = driver.find_elements(By.XPATH,XPATH_PAGINA['continue_ganhando'])
                time.sleep(10)
                for c in track(c_ganhar[5:14],total=100,description='[yellow]Concluindo: "Continue ganhando"...',transient=True):
                    c.click()
                    time.sleep(0.07)
                progresso.update(tarefa_continue_ganhando,advance=10,description="[green]Concluido...")
                driver.quit()
                break
    except Exception as e:
        print(f'Não foi possivel realizar o "Ganhe Mais!" error:\n {e}')




