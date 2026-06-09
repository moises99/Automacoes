from config import LINKS,XPATH_PAGINA,VARIAVEIS,CHAVE_ID
from personalizacao import texto_personalizado
import datetime as dt
from time import sleep as sl
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from personalizacao import texto_personalizado


#Responsavél por executar as funcionalidades da página
def func_principal():
    seus_pontos_dia = pontos_membro()
    arquivo_log = gera_log()
    noticias_func = coleta_noticias()
    print(texto_personalizado('Iniciando pesquisas'.upper()))
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    for pos,titulo in enumerate(noticias_func[0]):
        try:
            with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{CHAVE_ID["chave"]}\nLink: https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}\n')
                print()
        except FileNotFoundError as e:
            print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {arquivo_log}.\nSeguiremos com as pesquisas')
            print()
        print(f'Notícia {pos+1} = Manchete: {titulo}\nID:{CHAVE_ID["chave"]}\nLINK: https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}')
        driver.get(f'https://www.bing.com/search?q={noticias_func[1][pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={noticias_func[1][pos]}&sc=15-7&sk=&cvid={CHAVE_ID["chave"]}')
        sl(5)
        #Verifica na posição 14 se o limite de pontos foram atingidos
        if pos == 20:
            pontos_atuallizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
            maximo_ponto =  pontos_atuallizados >= seus_pontos_dia
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {seus_pontos_dia}')
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanhão para ganhar novos pontos.')
                driver.quit()
                break
        #Verifica na posição 30 se o limite de pontos foram atingidos, se não ele ira fazer uma verificção a cada pesquisa.
        if pos >= 30:
            pontos_atuallizados = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
            maximo_ponto = pontos_atuallizados >= seus_pontos_dia
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {seus_pontos_dia}')
            #Se o limite de pontos foram atingido finaliza a rotina 
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanhão para ganhar novos pontos.')
                driver.quit()
                break
        print()
    driver.quit()


#Rerorna a quantidade de pontos do usuário
def verifica_pontos(link_pagina , xpath_pontos) -> int:
    '''
    Funcão responavél por coletar os pontos atuais.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_pontos: o caminho do xpath dos pontos
    '''
    
    try:
        print(texto_personalizado('Iniciado a verificação dos pontos'.upper()))
        #Abre navegado em segundo plano e recebe os parametros da função
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
        print(f'Erro de identação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt as e:
        print(f'Interrompido pelo usuário: {e}')
    except NameError as e:
        print(f'Variavel nao definida: {e}')

#Rerorna a quantidade de pontos do usuário
def verifica_membro(link_pagina,xpath_membro) -> int:
    '''
    Funcão responavél verificar o nivel de membro.
    Necessário passar dois parametros:
    link_pagina: url do sua pgina logada
    xpath_membro: o caminho do xpath nivel (Ouro,Prata etc...)
    '''
    try:
        print(texto_personalizado('Iniciado a verificação de nivel Membro'.upper()))
        #Abre navegado em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        driver_segundo_plano.add_argument("--headless=new")
        driver_membro = webdriver.Edge(options=driver_segundo_plano)
        driver_membro.get(link_pagina)
        membro = driver_membro.find_element(By.XPATH,xpath_membro)
        membro = membro.text
        driver_membro.quit()
        if membro == 'Gold':
            membro = 60
            return membro
        if membro == 'Silver':
            membro = 30
            return membro
    except IndentationError as e:
        print(f'Erro de identação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt as e:
        print(f'Interrompido pelo usuário: {e}')
    except NameError as e:
        print(f'Variavel no definida: {e}')


#Verifica a quantida de pontos e nivél de membro
def pontos_membro():
    pontos_atuais = verifica_pontos(LINKS['home_page'] , XPATH_PAGINA["pontos"])
    pontos_membro = verifica_membro(LINKS['home_page'] , XPATH_PAGINA["membro"])
    print(texto_personalizado(f'PONTOS ATUAIS: {pontos_atuais} '))
    print(texto_personalizado(F' VOCÊ É MEMBRO OURO COM {pontos_membro} PONTOS DIARIOS DE PESQUISAS ')) if pontos_membro == 60 else print(texto_personalizado(F' VOCÊ É MEMBRO PRATA COM {pontos_membro} PONTOS DIARIOS DE PESQUISAS '))
    seus_pontos_dia = pontos_atuais + pontos_membro
    return seus_pontos_dia

#Gera um arquivo vontendo a manche e os links de cada noticia
def gera_log():
    try:
        #Bloco para criar o arquico concatenando a data do dia com o nome do arquivo
        arquivo_log = VARIAVEIS["local_arquivo"] + VARIAVEIS["nome_arquivo"]
        with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
            arquivo.write(f'======PESQUISAS DATA {dt.datetime.now().strftime("%d/%m/%Y")}======\n')
    except FileNotFoundError as e:
        print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {VARIAVEIS["local_arquivo"]}.\nSeguiremos apenas com a coleta de dados.')
        print()
    return arquivo_log


#Cria a conexao com o site *Necessário estar logado e Rolagem automatica da Pagina
def driver_edge():
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get(LINKS["msn_news"])
    print(texto_personalizado('Acessando página de notícias'.upper()))
    for _ in range(12):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sl(2)
    print(texto_personalizado('Coletando informaçoes'.upper()))
    sl(.2)
    print()
    return driver


#Coleta o titulo das noticias
def coleta_noticias():
    driver = driver_edge()
    print(texto_personalizado('Gerando lista'.upper()))
    titulo_noticia = []
    lista_noticia_formatada = []
    titulos_noticia = driver.find_elements(By.XPATH,"//a[@class='title']")
    for titulos in titulos_noticia:
        manchete = f"{titulos.text}"
        if len(manchete) > 5:
            titulo_noticia.append(manchete)
            noticias_formatadas = str(titulos.text).replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            lista_noticia_formatada.append(noticias_formatadas)
    print(texto_personalizado('Lista gerada'.upper()))
    print(texto_personalizado(f'Total de noticias: {len(titulo_noticia)} '.upper()))
    print()
    return titulo_noticia,lista_noticia_formatada
