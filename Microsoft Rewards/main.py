from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep as sl
import datetime as dt
from pontos import verifica_pontos,verifica_membro
from funcoes import chave
from personalizacao import texto_personalizado


#Verifica a quantida de pontos e nivél de membro antes de iniciar a rotina
try:
    pontos_atuais = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex']")
    pontos_membro =  verifica_membro("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//p[@class='rounded-ctrlBadgeCorner px-2 py-1 text-globalCaption1Strong text-rewardsLevelBadgeFg bg-rewardsGoldBadgeBg']")
    seus_pontos_dia = pontos_atuais + pontos_membro
    print(texto_personalizado(f'PONTOS ATUAIS: {pontos_atuais} '))
    if pontos_membro == 60:
        print(texto_personalizado(F' VOCÊ É MEMBRO OURO COM {pontos_membro} PONTOS DIARIOS DE PESQUISAS '))
    elif pontos_membro == 30:
        print(texto_personalizado(F' VOCÊ É MEMBRO PRATA COM {pontos_membro} PONTOS DIARIOS DE PESQUISAS '))
except:
    print(f'Algo deu errado!!!'.upper())
    exit()

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
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get('https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1')
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
        chave_id = chave()
        print()
        
        try:
            with open(f'{arquivo_log}.txt','a',encoding="utf-8") as arquivo:
                arquivo.writelines(f'\nManchete {pos+1}: {titulo}\nID:{chave_id}\nLink: https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave_id}\n')
                print()
        except FileNotFoundError as e:
            print(f'Arquivo ou diretorio nao encontrado ,verifique o caminho {local_arquivo}.\nSeguiremos com as pesquisas')
            print()
        print(f'Notícia {pos+1} = Manchete: {titulo}\nID:{chave_id}\nLINK: https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave_id}')
        driver.get(f'https://www.bing.com/search?q={lista_noticia_formatada[pos]}&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq={lista_noticia_formatada[pos]}&sc=15-7&sk=&cvid={chave_id}')
        sl(5)
        
        #Verifica na posição 14 se o limite de pontos foram atingidos
        if pos == 20:
            pontos_atuallizados =pontos_atuais = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex']")
            print(f'{pontos_atuallizados} / {seus_pontos_dia} / ')
            maximo_ponto =  pontos_atuallizados >= seus_pontos_dia
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {seus_pontos_dia}')
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanão para ganhar novos pontos.')
                driver.quit()
                break
        #Verifica na posição 30 se o limite de pontos foram atingidos, se não ele ira fazer uma verificção a cada pesquisa.
        if pos >= 30:
            pontos_atuallizados = pontos_atuais = verifica_pontos("https://rewards.bing.com/dashboard?ref=pin&OCID=PINREW" , "//div[@class='flex']")
            print(f'{pontos_atuallizados} / {seus_pontos_dia} / ')
            maximo_ponto = pontos_atuallizados >= seus_pontos_dia
            print(f'PONTOS ATUAIS: {pontos_atuallizados} / {seus_pontos_dia}')
            #Se o limite de pontos foram atingido finaliza a rotina 
            if maximo_ponto:
                print(f'Parabéns você atingiu o numero máximo de pontos: {pontos_atuallizados}!!!\nVolte amanhão para ganhar novos pontos.')
                driver.quit()
                break

    print(texto_personalizado(f'Total de noticias: {len(titulo_noticia)} '.upper()))            
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
    