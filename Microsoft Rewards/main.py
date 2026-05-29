from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep as sl
import datetime as dt
from pontos import verifica_pontos
from personalizacao import texto_personalizado
import secrets


#Verifica a quantida de pontos antes de iniciar a rotina

pontos_atuais = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex items-center gap-2']")
pontos_mais_30 = pontos_atuais + 30
print(texto_personalizado(f'PONTOS ATUAIS: {pontos_atuais}'))

try:
    try:
        print()
        #Bloco para criar o arquico concatenando a data do dia com o nome do arquivo
        data = dt.datetime.today().now()
        local_arquivo = 'D:\\py\\Projeto Automacao\\logs_pesquisa\\'
        nome_arquivo = f"manchete_{data}".replace(' ','_').replace(':','-').replace('.','_')
        arquivo_log = local_arquivo + nome_arquivo
        with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
            arquivo.write(f'======PESQUISAS DATA {dt.date.today().day}/{dt.date.today().month}/{dt.date.today().year}======\n')
    except FileNotFoundError as e:
        print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {local_arquivo}.\nSeguiremos apenas com a coleta de dados.')
        print()


    #Cria a conexao com o site *Necessário estar logado
    print(texto_personalizado(f'Iniciado rotina: {nome_arquivo}.'.upper()))
    url = 'https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1'
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get(url)
    print(texto_personalizado('Pagina acessada'.upper()))


    # #Rolagem automatica da Pagina
    print(texto_personalizado('Coletando informaçoes da pagina'.upper()))
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sl(2)
    sl(.2)


    #Listas para armazenar as manchetes e as  noticias formatadas respectivamente
    titulo_noticia = []
    lista_noticia_formatada = []

    #Busca o eleento que contem o titulo das noticias
    titulos_noticia = driver.find_elements(By.XPATH,"//a[@class='title']")


    #Adciona o as informações formatadas e separadas nas listas titulo_noticia = [], lista_noticia_formatada = []
    print(texto_personalizado('Gerando lista'.upper()))
    for titulos in titulos_noticia:
        manchete = f"{titulos.text}"
        if len(manchete) > 5:
            titulo_noticia.append(manchete)
            noticias_formatadas = str(titulos.text).replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            lista_noticia_formatada.append(noticias_formatadas)
    print(texto_personalizado('Lista gerada'.upper()))

    #Print nas manchetes e concatena as mesma com o link
    print(texto_personalizado('Iniciando pesquisas'.upper()))
    print(texto_personalizado(f'Total de noticias: {len(titulo_noticia)} '.upper()))

    #Visualização e pesquisa
    for pos,titulo in enumerate(titulo_noticia):
        #Gera um ID aleatorio para concatenar a url de pesquisa
        chave = secrets.token_hex(26).upper()
        print()
        if pos == 0:
            try:
                with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                    arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{chave}\nLink: https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave}\n')
                    print()
            except FileNotFoundError as e:
                print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {local_arquivo}.\nSeguiremos com as pesquisas')
            print()
        print(f'Notícia {pos+1} = Manchete: {titulo}\nID:{chave}\nLINK: https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave}')
        driver.get(f'https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave}')
        sl(3)
        
        #Verifica na posição 14 se o limite de pontos foram atingidos
        if pos == 30:
            pontos_atuallizados = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex items-center gap-2']")
            maximo_ponto =  pontos_atuallizados >= pontos_mais_30
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {pontos_mais_30}')
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanão para ganhar novos pontos.')
                driver.quit()
                break
        #Verifica na posição 30 se o limite de pontos foram atingidos, se não ele ira fazer uma verificção a cada pesquisa.
        elif pos >= 50:
            pontos_atuallizados = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex items-center gap-2']")
            maximo_ponto = pontos_atuallizados >= pontos_mais_30
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {pontos_mais_30}')
            #Se o limite de pontos foram atingido finaliza a rotina 
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanhão para ganhar novos pontos.')
                driver.quit()
                break


    driver.quit()


except FileNotFoundError as e:
    print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {local_arquivo} : {e}')
except IndentationError as e:
    print(f'Erro de identação {e}')
except SyntaxError as e:
    print(f'Erro de sintaxe {e}')
except KeyboardInterrupt as e:
    print(f'Interrompido pelo usuário: {e}')
except NameError as e:
    print(f'Variavel não definida: {e}')
    