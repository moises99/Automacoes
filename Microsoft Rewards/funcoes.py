from config import LINKS,XPATH_PAGINA,VARIAVEIS
from personalizacao import texto_personalizado
import datetime as dt
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from rich.progress import Progress, track
from rich import print
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
import secrets
import random
import sqlite3

ID_PESQUISA = secrets.token_hex(6).upper()

#Responsável por executar as funcionalidades da página
def func_principal():
    '''
    Função principal responsável por executar toda a rotina.
    '''
    try:
        destaques_txt = gera_txt('suas_pesquisa',f'====== PESQUISAS DATA {dt.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")} ======\n',f'{VARIAVEIS["nome_arquivo"]}.txt' )
        #Bloco responsável por executar algumas funções com barra de progresso
        pontos_atuais = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
        with Progress() as progresso:
            tarefa = progresso.add_task(description="",transient=True)
            while True:
                progresso.update(tarefa,advance=25,description="[yellow]Iniciando verificação...")
                print(texto_personalizado(f' PONTOS ATUAIS: {pontos_atuais[0]} '))
                progresso.update(tarefa,advance=25,description="[yellow]Verificando nivel de membro...")
                pontos_nivel_membro = verifica_membro(LINKS['home_page'] , XPATH_PAGINA["membro"])
                if pontos_nivel_membro == 60:
                    nome_nivel_membro = "OURO"
                else:
                    nome_nivel_membro = "PRATA"
                print(texto_personalizado(F' VOCÊ É MEMBRO {nome_nivel_membro} COM {pontos_nivel_membro} PONTOS DIARIOS DE PESQUISAS ')) 
                progresso.update(tarefa,advance=45,description="[yellow]Coletando informações...")
                #Valida a quantidade de noticias
                tentativa = 0
                while True:
                    noticias = coleta_noticias()
                    if len (noticias['titulo_noticia']) > 20:
                        break
                    else:
                        tentativa +=1
                        print(texto_personalizado(f' Quantidade de noticias insulficiente. Noticias encotradas: {len(noticias['titulo_noticia'])}'.upper()))
                        print(texto_personalizado(f' Necessários ao menos 20 noticias '.upper()))
                        progresso.update(tarefa,advance=2,description="[yellow]Realizando uma nova tentantiva")
                        print(texto_personalizado(f' Tentantiva: {tentativa}/3 '.upper()))
                        if tentativa == 3:
                            progresso.update(tarefa,advance=3,description="[red]Numero de noticias insuficiente, execute a rotina novamente")
                            exit()
                progresso.update(tarefa,advance=5,description="[green]Concluindo",visible=False)
                meu_maximo_de_pontos = pontos_atuais[0] + pontos_nivel_membro
                print(texto_personalizado(f' Total de {len(noticias['titulo_noticia'])} notícias'.upper()))
                break
        print(texto_personalizado(' Iniciando pesquisas '.upper()))
        driver_edge = Options()
        if not VARIAVEIS["ver_processo"]:
            driver_edge.add_argument("--headless=new")
        driver = webdriver.Edge(options=driver_edge)
    except Exception as e:
        print(f'Erro: {e}')
        exit()
    #Bloco responsável por executar as pesquisar e gravar as informações no arquivo de texto
    conexao = sqlite3.connect('minhas_pesquisas.db')
    cursor = conexao.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS noticias_links (id INTEGER PRIMARY KEY AUTOINCREMENT,titulo TEXT,link TEXT,id_pesquisa TEXT)')
    for pos,titulo in track(enumerate(noticias['titulo_noticia']),description="[purple]Pesquisando...",transient=True):
        TOKEN_ID = secrets.token_hex(26).upper()
        try:
            with open(destaques_txt,'a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'Destaque {pos+1}: {titulo}\n-Link: https://www.bing.com/search?q={noticias['link_noticia_formatada'][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias['link_noticia_formatada'][pos]}&sc=15-7&sk=&cvid={TOKEN_ID}\n\n')
                print()
            meu_link = f'https://www.bing.com/search?q={noticias['link_noticia_formatada'][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias['link_noticia_formatada'][pos]}&sc=15-7&sk=&cvid={TOKEN_ID}'
            try:
                cursor.execute(f'INSERT INTO noticias_links (titulo,link,id_pesquisa) VALUES ("{titulo}","{meu_link}","{ID_PESQUISA}")')
                conexao.commit()
            except:
                continue    
        except FileNotFoundError:
            print(f'Arquivo ou diretório não encontrado, verifique o caminho {destaques_txt}.\nSeguiremos com as pesquisas')
            print()
        driver.get(f'https://www.bing.com/search?q={noticias['link_noticia_formatada'][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias['link_noticia_formatada'][pos]}&sc=15-7&sk=&cvid={TOKEN_ID}')
        load(0.07,f'Notícia {pos+1}: [link=https://www.bing.com/search?q={noticias['link_noticia_formatada'][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias['link_noticia_formatada'][pos]}&sc=15-7&sk=&cvid={TOKEN_ID}]{titulo}[/link]')
        #Bloco responsável por verificar se o limite de pontos.
        VARIAVEIS["controle_pontos"] +=3
        if VARIAVEIS["controle_pontos"] == 60:
            pontos_atualizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
            maximo_ponto =  int(pontos_atualizados[0]) >= int(meu_maximo_de_pontos)
            pontos_faltando = int(meu_maximo_de_pontos) - int(pontos_atualizados[0])
            if maximo_ponto:
                break
            else:
                #Retorna uma "posição" da diferença de pontos exemplo: 60(pontos_nivel_membro) - 6(pontos_faltando) = 54, me retornar a posica 54 que no caso seira mais 2 duas pesquisa para fechar os 60 pontos
                VARIAVEIS["controle_pontos"] = pontos_nivel_membro - pontos_faltando
                print(texto_personalizado(f' Necessários mais {pontos_faltando} pontos').upper())
            #Verifica se há pontos a serem reivindicados e se faltam apenas tres pontos para chegar ao limite de pontos.
            #Caso não atinja o limite ele pega os pontos que faltam e faz novas tentativas até atingir o máximo de pontos.
            #Se faltar apenas tres pontos ira realizar tres tentativas de pesquisas e entao reivindicara os pontos disponiveis completando os seus pontos diarios.
            if pontos_faltando == 3:
                VARIAVEIS["controle_tres_pontos"] +=1
                print(texto_personalizado(f'Tentativa: {VARIAVEIS["controle_tres_pontos"]}/3'))
                if VARIAVEIS["controle_tres_pontos"] == 3:
                    break
    conexao.close()
    meus_pontos_reivindicados = reivindicar(LINKS["home_page"]) if pontos_atualizados[2] else 0
    VARIAVEIS["c_ganhando"] = continue_ganhando(LINKS["home_page"])
    VARIAVEIS["d_diariamente"] = definido_diariamente(LINKS["home_page"])
    if VARIAVEIS["d_diariamente"] == 0 :
        print(texto_personalizado('Sem defafios para fazer'.upper()))
    pontos_totais = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
    try:                
       VARIAVEIS["descricao"] = resumo(nome_nivel_membro,pontos_nivel_membro,pontos_atuais[0],pontos_totais[0],meus_pontos_reivindicados,pos +1,VARIAVEIS["d_diariamente"],VARIAVEIS["c_ganhando"])
       print(VARIAVEIS["descricao"])
    except Exception as e:
        print(f'Erro: {e}')
    print(texto_personalizado(f'ARQUIVO SALVO EM {destaques_txt}'))
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
        
        #Abre o navegador em segundo plano e recebe os parametros da função
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

#Gera um arquivo contendo a manchete e os links de cada pesquisa
def gera_txt(pasta ='log',cabecaclho = VARIAVEIS["data_hora"], nome_arquivo = 'log.txt'):
    '''
    Gera um arquivo txt com as manchetes e links de cada notícia.
    E retornar o nome do arquivo
    '''
    try:
        caminho = Path(__file__).parent / pasta
        caminho.mkdir(exist_ok=True)
        arquivo = Path(__file__).parent / pasta / nome_arquivo
        arquivo.touch()
        #Bloco para criar o arquico concatenando a data do dia com o nome do arquivo
        with open(arquivo,'a',encoding="utf-8") as arquivo:
            arquivo.write(cabecaclho)
    except FileNotFoundError as e:
        print(f'Arquivo ou diretório não encontrado, verifique o caminho {caminho}.')
        print()
    nome_caminho_arquivo = Path() / caminho / nome_arquivo
    return nome_caminho_arquivo

def coleta_noticias():
    '''
    Coleta as manchetes da pagina.
    '''
    titulo_noticia = []
    link_noticia_formatada = []
    for index in track(range(8,12),description=" [yellow]Realizando as requisições... ",transient=True):
        try:
            url = (f'https://www.bing.com/news/feed/infinitescrollajax?fcvid=11AB92FC6C326685139485E56D1D67F0&PageIndex={index}&NewsBrowseDataVersion=mkt_dataversion-4-chieeeap002edf4_v1.0&InfiniteScroll=1')
            response = requests.get(url)
            if response.status_code == 200:
                pagina = BeautifulSoup(response.text, "html.parser")
                manchetes = pagina.find_all("a", class_="title")
                for manchete in manchetes:
                    manchetetxt = manchete.get_text()
                    if manchetetxt not in titulo_noticia:
                        titulo_noticia.append(manchetetxt)
            else:
                print('STATUS DA REQUISIÇÃO : ',response.status_code)
        except Exception as e:
            print(e)
    random.shuffle(titulo_noticia)
    conexao = sqlite3.connect('minhas_pesquisas.db')
    cursor = conexao.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS noticias (id INTEGER PRIMARY KEY AUTOINCREMENT,titulo TEXT,id_pesquisa TEXT)')
    for titulos in track(titulo_noticia, description=" [yellow]Gerando links... ",transient=True):
        if len(titulos) > 5:
            link_formatado = titulos.replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            link_noticia_formatada.append(link_formatado)
    for titulo in track(titulo_noticia,description=" [yellow]Salvando dados... ",transient=True):
        try:
            cursor.execute(f'INSERT INTO noticias (titulo,id_pesquisa) VALUES ("{titulo}","{ID_PESQUISA}") ')
        except:
            continue
    conexao.commit()
    conexao.close()
    return {'titulo_noticia':titulo_noticia,
            'link_noticia_formatada':link_noticia_formatada
            }
coleta_noticias()
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

#Mostra um resumo das atividades após concluir a rotina
def resumo(nivel_membro="N/A",pontos_membro="N/A",pontos="N/A",pontos_atualizados="N/A",pontos_reivindicados="N/A",total_pesquisas="N/A",definidos_diariamente="N/A",cont_ganhando="N/A"):
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
    conexao = sqlite3.connect('minhas_pesquisas.db')
    cursor = conexao.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS pontos (id INTEGER PRIMARY KEY AUTOINCREMENT,nivel_membro TEXT,pontos_membro INTEGER,pontos_anteriores INTEGER,pontos_atualizados INTEGER,' \
    'ponto_reivindicados INTEGER,total_pesquisas INTEGER,definidos_diariamente INTEGER,cont_ganhando INTEGER, id_pesquisa TEXT) ')
    cursor.execute(f'INSERT INTO pontos (nivel_membro,pontos_membro,pontos_anteriores,pontos_atualizados,' \
    'ponto_reivindicados,total_pesquisas,definidos_diariamente,cont_ganhando, id_pesquisa)' \
    f' VALUES ("{nivel_membro}","{pontos_membro}","{pontos}","{pontos_atualizados}","{pontos_reivindicados}","{total_pesquisas}","{definidos_diariamente}","{cont_ganhando}","{ID_PESQUISA}")')
    conexao.commit()
    conexao.close()
    return painel
#Funcão responsável por coletar os pontos atuais e se há pontos para reivindicar.
def verifica_pontos(link_pagina , xpath_pontos):
    '''
    Funcão responsável por coletar os pontos atuais e se há pontos para reivindicar.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_pontos: o caminho do xpath dos pontos
    '''
    with Progress() as progresso:
        while True:
            tarefa_pontos = progresso.add_task(description='[yellow]Verificando pontos...',transient=True)
            try:
                #Abre o navegador em segundo plano e recebe os parametros da função
                driver_segundo_plano = Options()
                if not VARIAVEIS["ver_processo"]:
                    driver_segundo_plano.add_argument("--headless=new")
                progresso.update(tarefa_pontos, advance=40,description='[yellow]Verificando pontos...',transient=True)
                driver_pontos = webdriver.Edge(options=driver_segundo_plano)
                driver_pontos.get(link_pagina)
                pontos = driver_pontos.find_elements(By.XPATH,xpath_pontos)
                lista_pontos = [pontos.text.replace(".","") for pontos in pontos]
                progresso.update(tarefa_pontos, advance=50,description='[yellow]Verificando pontos...',transient=True)
                #converte o float para int
                pontos = int(lista_pontos[0])
                pontos_reivindicar = int(lista_pontos[1])
                flag_pontos_reivindicar = False
                if pontos_reivindicar >= 1: 
                    flag_pontos_reivindicar = True
                driver_pontos.quit()
                progresso.update(tarefa_pontos, advance=10,description='[green]Concluido...',visible=False)
                return int(pontos),int(pontos_reivindicar),bool(flag_pontos_reivindicar)
            except IndentationError as e:
                print(f'Erro de indentação {e}')
            except SyntaxError as e:
                print(f'Erro de sintaxe {e}')
            except KeyboardInterrupt as e:
                print(f'Interrompido pelo usuário: {e}')
            except NameError as e:
                print(f'Variavel nao definida: {e}')
            break

#Reivindica os pontos dosponiveis
def reivindicar(home_page) -> int:
    '''
    Reivindica os pontos dosponiveis
    '''
    try:
        with Progress() as progresso:
            tarefa_reivindicar = progresso.add_task(description="[yellow]Reivindicando pontos...")
            while True:
                progresso.update(tarefa_reivindicar,advance=5,description="[yellow]Reivindicando pontos...")
                driver_edge = Options()
                #Necessario mostrar o processo para que seja possivel clicar nos elementos
                if VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(home_page)
                clicar_reivindicar = driver.find_element(By.XPATH,XPATH_PAGINA["click_reivindicar"])
                driver.implicitly_wait(15)
                clicar_reivindicar.click()
                meus_pontos_reivindicar = int(driver.find_element(By.XPATH,XPATH_PAGINA["meus_pontos_reivindicar"]).text)
                if meus_pontos_reivindicar > 0:
                    driver.implicitly_wait(15)
                    clicar_ganhe_mais = driver.find_element(By.XPATH,XPATH_PAGINA['ganhar_mais_pontos_reivindicar'])
                    driver.implicitly_wait(5)
                    clicar_ganhe_mais.click()
                    progresso.update(tarefa_reivindicar,advance=95,description="[green]Pontos reivindicados",visible=False)
                else:
                    progresso.update(tarefa_reivindicar,advance=95,description="[purple]Sem pontos para reivindicar",visible=False)
                driver.quit()
                break
        return meus_pontos_reivindicar if meus_pontos_reivindicar > 0 else 0
    except Exception as e:
        print(texto_personalizado(f"Não foi possivel reivindicar os pontos"))
        arquivo_txt = gera_txt('log_error',nome_arquivo='reivindicar.txt')
        with open(arquivo_txt,'a',encoding="utf-8") as arquivo:
            arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
            arquivo.write("\n")
            arquivo.write(str(e))
        print(texto_personalizado(f'Verifique o arquivo: {arquivo_txt}'))
        driver.quit()

#Faz atividades "Continue Ganhando"
def continue_ganhando(link_home)->int:
    '''
    Tarefas Continue ganhando [EM TESTES]
    '''
    print()
    print(texto_personalizado('Continue Ganhando'.upper()))
    with Progress() as progresso:
        tarefa_continue_ganhando = progresso.add_task(description='[yellow]Verificando: "Continue ganhando"...')
        while True:
            progresso.update(tarefa_continue_ganhando,advance=10,description='[yellow]Verificando: "Continue ganhando"...')
            driver_edge = Options()
            #Necessario mostrar o processo para que seja possivel clicar nos elementos
            if VARIAVEIS["ver_processo"]: 
                driver_edge.add_argument("--headless=new")
            driver = webdriver.Edge(options=driver_edge)
            driver.get(link_home)
            progresso.update(tarefa_continue_ganhando,advance=5,description='[yellow]Verificando: "Continue ganhando"...')
            driver.get(LINKS['continue_ganhando'])
            progresso.update(tarefa_continue_ganhando,advance=5,description='[yellow]Verificando: "Continue ganhando"...')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for c in track(range(10),description="[yellow]Aguarde...",transient=True):
                time.sleep(1)
            try:
                titulos_continue_ganhando = driver.find_elements(By.XPATH,XPATH_PAGINA["titulos_continue_ganhando"])[5:]
                click_continue_ganhando = driver.find_elements(By.XPATH,XPATH_PAGINA['click_continue_ganhando'])[1:]
                if len(click_continue_ganhando) > 0:
                    for p,c in enumerate(track(click_continue_ganhando,description='[purple]Clicando...',transient=True)):
                        titulos_continue_ganhando_text = titulos_continue_ganhando[p].text.upper()
                        try:
                            c.click()
                            print(texto_personalizado(f'{titulos_continue_ganhando_text} [OK]'))
                        except Exception as e:
                            print(texto_personalizado(f'A tarefa: "{titulos_continue_ganhando_text}" deve ser feita manualmente'))
                            arquivo_txt = gera_txt('log_error',nome_arquivo='continue_ganhando.txt')
                            with open(arquivo_txt,'a',encoding="utf-8") as arquivo:
                                arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                                arquivo.write("\n")
                                arquivo.write(str(e))
                            print(texto_personalizado(f'Verifique o arquivo: {arquivo_txt}'))
                        finally:
                            progresso.update(tarefa_continue_ganhando,advance=10,description=f'[yellow]Fazendo o "Continue Ganhando: {titulos_continue_ganhando_text}"...')
                            time.sleep(5)
                    ponto_continue_ganhando = int(driver.find_elements(By.XPATH,XPATH_PAGINA['ponto_continue_ganhando'])[2].text)
                    progresso.update(tarefa_continue_ganhando,advance=5,description='[green]Concluido...',visible=False)
                    driver.quit()
                    return ponto_continue_ganhando
                else:
                    progresso.update(tarefa_continue_ganhando,advance=80,description='[purple]Não há tarefas disponiveis!')
                    driver.quit()
                    return 0
            except Exception as e:
                print(texto_personalizado(f'Não foi possivel fazer o "Continue ganhando"'))
                arquivo_txt = gera_txt('log_error',nome_arquivo='continue_ganhando.txt')
                with open(arquivo_txt,'a',encoding="utf-8") as arquivo:
                    arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                    arquivo.write("\n")
                    arquivo.write(str(e))
                print(texto_personalizado(f'Verifique o arquivo: {arquivo_txt}'))
            break

#Faz atividades "Desafios Diarios"
def definido_diariamente(home_page) ->int: 

    '''
    Desafios diarios [EM TESTES]
    '''
    print()
    print(texto_personalizado('Desafios Diários'.upper()))
    with Progress() as progresso:
        tarefa_definido_diariamente = progresso.add_task(description='[yellow]Verificando: "Desafios Diários..."')
        while True:
            try:
                progresso.update(tarefa_definido_diariamente,advance=5,description='[yellow]Verificando: "Desafios diários..."')
                driver_edge = Options()
                #Necessario mostrar o processo para que seja possivel clicar nos elementos
                if VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(home_page)
                driver.implicitly_wait(5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                titulo_definidos_diariamente = driver.find_elements(By.XPATH,XPATH_PAGINA["titulo_definidos_diariamente"])
                pontos_definidos_diariamente = driver.find_elements(By.XPATH,XPATH_PAGINA["pontos_definidos_diariamente"])
                pontos_definidos_diariamente_int = [int(p.text[1:]) for p in pontos_definidos_diariamente]
                click_definidos_diariamente = driver.find_elements(By.XPATH,XPATH_PAGINA["click_definidos_diariamente"])[2:5]
                progresso.update(tarefa_definido_diariamente,advance=10,description='[yellow]Verificando: "Desafios diários..."')  
                total_definidos_diariamente = 0
                for p,c in enumerate(track(click_definidos_diariamente[:len(pontos_definidos_diariamente_int)],description="[purple]Clicando...",transient=True,total=len(click_definidos_diariamente))):
                    titulo_definidos_diariamente_text = titulo_definidos_diariamente[p].text.upper()
                    try:
                        if len(pontos_definidos_diariamente_int) > 0:
                            c.click()
                            total_definidos_diariamente += pontos_definidos_diariamente_int[p]
                            print(texto_personalizado(f'{titulo_definidos_diariamente_text} + {pontos_definidos_diariamente_int[p]} [CONCLUÍDO]'))
                    except Exception as e:
                        print(texto_personalizado(f'A tarefa: "{titulo_definidos_diariamente_text}" deve ser feita manualmente'))
                        arquivo_txt = gera_txt('log_error',nome_arquivo='definido_diariamente.txt')
                        with open(arquivo_txt,'a',encoding="utf-8") as arquivo:
                            arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                            arquivo.write('definido_diariamente')
                            arquivo.write("\n")
                            arquivo.write(str(e))
                        print(texto_personalizado(f'Verifique o arquivo: {arquivo_txt}'))
                    finally:
                        progresso.update(tarefa_definido_diariamente,advance=25,description=f'[yellow]Fazendo o "Definido Diariamente: {titulo_definidos_diariamente_text}"...')
                        time.sleep(2)
                    progresso.update(tarefa_definido_diariamente,advance=10,description="[green]Concluido",visible=False)
                driver.quit()
                return total_definidos_diariamente if total_definidos_diariamente  > 0 else 0
            except Exception as e:
                print(texto_personalizado(f'Não foi possivel fazer o "Definido Diariamente"'))
                arquivo_txt = gera_txt('log_error',nome_arquivo='definido_diariamente.txt')
                with open(arquivo_txt,'a',encoding="utf-8") as arquivo:
                    arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                    arquivo.write("\n")
                    arquivo.write(str(e))
                print(texto_personalizado(f'Verifique o arquivo: {arquivo_txt}'))
            break