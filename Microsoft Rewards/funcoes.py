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
    try:
        arquivo_log = gera_txt()
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
                    noticias_func = coleta_noticias()
                    if len (noticias_func[0]) > 20:
                        break
                    else:
                        tentativa +=1
                        print(texto_personalizado(f' Quantidade de noticias insulficiente. Noticias encotradas: {len(noticias_func[0])}'.upper()))
                        print(texto_personalizado(f' Necessários ao menos 20 noticias '.upper()))
                        progresso.update(tarefa,advance=2,description="[yellow]Realizando uma nova tentantiva")
                        print(texto_personalizado(f' Tentantiva: {tentativa}/3 '.upper()))
                        if tentativa == 3:
                            progresso.update(tarefa,advance=3,description="[red]Numero de noticias insuficiente, execute a rotina novamente")
                            exit()
                progresso.update(tarefa,advance=5,description="[green]Concluindo",visible=False)
                meu_maximo_de_pontos = pontos_atuais[0] + pontos_nivel_membro
                print(texto_personalizado(f' Total de {len(noticias_func[0])} notícias'.upper()))
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
    for pos,titulo in track(enumerate(noticias_func[0]),description="[purple]Pesquisando...",transient=True):
        try:
            with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{CHAVE_ID["chave"]}\nLink: https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}\n')
                print()
        except FileNotFoundError:
            print(f'Arquivo ou diretório não encontrado, verifique o caminho {arquivo_log}.\nSeguiremos com as pesquisas')
            print()
        driver.get(f'https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}')
        load(0.01,f'Notícia {pos+1}: [link=https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}]{titulo}[/link]')
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
    if pontos_atualizados[2]:
        reivindicar(LINKS["home_page"])
    VARIAVEIS["c_ganhando"] = continue_ganhando(LINKS["home_page"])
    VARIAVEIS["d_diariamente"] = definido_diariamente(LINKS["home_page"])
    pontos_atualizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
    print(texto_personalizado(f' Você atingiu o máximo de pontos ').upper().center(120))
    try:                
        print(resumo(nome_nivel_membro,pontos_nivel_membro,pontos_atuais[0],pontos_atualizados[0],pontos_atualizados[1],pos,VARIAVEIS["d_diariamente"],VARIAVEIS["c_ganhando"]))
    except Exception as e:
        print(f'Erro: {e}')
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
    except FileNotFoundError as e:
        print(f'Arquivo ou diretório não encontrado, verifique o caminho {VARIAVEIS["local_arquivo"]}.\nSeguiremos apenas com as pesquisas.')
        print()
    return VARIAVEIS["nome_arquivo"]

#Cria a conexao com o site *Necessário estar logado tammbém faz uma rolagem automatica da Pagina
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
    for _ in track(range(10),description="[yellow]Aguarde...",transient=True):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    return driver

#Coleta o título das noticias
def coleta_noticias():
    '''
    Coleta as manchetes da pagina.
    '''
    try:
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
        driver.quit()
        return titulo_noticia,lista_noticia_formatada
    except Exception as e:
        print(f'Ocorreu um erro.\n {e}')
        return 1
        
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
                #Abre navegador em segundo plano e recebe os parametros da função
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
                #Necessario mostrar o processo para que seja possivel clicar nos elementos
                if VARIAVEIS["ver_processo"]: 
                    driver_edge.add_argument("--headless=new")
                driver = webdriver.Edge(options=driver_edge)
                driver.get(home_page)
                clicar_reivindicar = driver.find_element(By.XPATH,XPATH_PAGINA["click_reivindicar"])
                time.sleep(5)
                driver.implicitly_wait(5)
                clicar_reivindicar.click()
                time.sleep(5)
                clicar_ganhe_mais = driver.find_element(By.XPATH,XPATH_PAGINA['ganhar_mais_pontos_reivindicar'])
                driver.implicitly_wait(5)
                time.sleep(5)
                clicar_ganhe_mais.click()
                progresso.update(tarefa_reivindicar,advance=95,description="[green]Pontos reivindicados")
                driver.quit()
                break
    except Exception as e:
        print(texto_personalizado(f"Não foi possivel reivindicar os pontos"))
        print(texto_personalizado('Verifique o arquivo reivindicar.txt'))
        with open('reivindicar.txt','w') as arquivo:
            arquivo.write(str(e))

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
                click_continue_ganhando = driver.find_elements(By.XPATH,XPATH_PAGINA['click_continue_ganhando'])[3:]
                if len(click_continue_ganhando) > 0:
                    for p,c in enumerate(track(click_continue_ganhando,description='[purple]Clicando...',transient=True)):
                        titulos_continue_ganhando_text = titulos_continue_ganhando[p].text.upper()
                        try:
                            c.click()
                            print(texto_personalizado(f'{titulos_continue_ganhando_text} [OK]'))
                        except Exception as e:
                            print(texto_personalizado(f'A tarefa: "{titulos_continue_ganhando_text}" deve ser feita manualmente'))
                            with open('definidos_diariamente.txt','a',encoding="utf-8") as arquivo:
                                arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                                arquivo.write("\n")
                                arquivo.write(str(e))
                        finally:
                            progresso.update(tarefa_continue_ganhando,advance=10,description=f'[yellow]Fazendo o "Continue Ganhando: {titulos_continue_ganhando_text}"...')
                            time.sleep(5)
                    ponto_continue_ganhando = int(driver.find_elements(By.XPATH,XPATH_PAGINA['ponto_continue_ganhando'])[2].text)
                    progresso.update(tarefa_continue_ganhando,advance=5,description='[green]Concluido...',visible=False)
                    driver.quit()
                    return ponto_continue_ganhando
                else:
                    print(texto_personalizado('Sem elementos para clicar'))
                    driver.quit()
                    return 0
            except Exception as e:
                print(texto_personalizado(f'Não foi possivel fazer o "Continue ganhando"'))
                print(texto_personalizado('Verifique o arquivo: continue_ganhando.txt'))
                with open("continue_ganhando.txt","w",encoding="utf-8") as arquivo:
                    arquivo.write(str(e))
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
            progresso.update(tarefa_definido_diariamente,advance=5,description='[yellow]Verificando: "Desafios diários..."')
            driver_edge = Options()
            #Necessario mostrar o processo para que seja possivel clicar nos elementos
            if VARIAVEIS["ver_processo"]: 
                driver_edge.add_argument("--headless=new")
            driver = webdriver.Edge(options=driver_edge)
            driver.get(home_page)
            driver.implicitly_wait(20)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            for c in track(range(10),description="[yellow]Aguarde...",transient=True):
                time.sleep(1)
            try:
                titulo_definidos_diariamente = driver.find_elements(By.XPATH,XPATH_PAGINA["titulo_definidos_diariamente"])
                click_definidos_diariamente = driver.find_elements(By.XPATH,XPATH_PAGINA["click_definidos_diariamente"])[2:5]
                progresso.update(tarefa_definido_diariamente,advance=10,description='[yellow]Verificando: "Desafios diários..."')
                pontos_definidos_diariamente = 0
                for p,c in enumerate(track(click_definidos_diariamente,description="[purple]Clicando...",transient=True,total=len(click_definidos_diariamente))):
                    titulo_definidos_diariamente_text = titulo_definidos_diariamente[p].text.upper()
                    
                    try:
                        c.click()
                        pontos_definidos_diariamente += 10
                        print(texto_personalizado(f'{titulo_definidos_diariamente_text} [OK]'))
                    except Exception as e:
                        print(texto_personalizado(f'A tarefa: "{titulo_definidos_diariamente_text}" deve ser feita manualmente'))
                        with open('definidos_diariamente.txt','a',encoding="utf-8") as arquivo:
                            arquivo.write(f'{VARIAVEIS["data_hora"]}\n')
                            arquivo.write("\n")
                            arquivo.write(str(e))
                    finally:
                        progresso.update(tarefa_definido_diariamente,advance=25,description=f'[yellow]Fazendo o "Definido Diariamente: {titulo_definidos_diariamente_text}"...')
                        time.sleep(5)
                progresso.update(tarefa_definido_diariamente,advance=10,description="[green]Concluido",visible=False)
                driver.quit()
                return pontos_definidos_diariamente if pontos_definidos_diariamente  > 0 else 0
            except Exception as e:
                print(texto_personalizado(f'Não foi possivel fazer o "Definido Diariamente"'))
                print(texto_personalizado('Verifique o arquivo: definido_diariamente.txt'))
                with open("definido_diariamente.txt","w",encoding="utf-8") as arquivo:
                    arquivo.write(str(e))
            break

print(resumo())