from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from personalizacao import texto_personalizado


#Rerorna a quantidade de pontos do usuário
def verifica_pontos(minha_url,meuxpath)->int:
    '''
    Funcão responavél por coletar os pontos atuais.
    Necessário passar dois parametros:
    minha_url: url do sua pgina logada
    meuxpath: o caminho do xpath
    '''
    
    try:
        print(texto_personalizado('Iniciado a verificação dos pontos'.upper()))
        #Abre navegado em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        driver_segundo_plano.add_argument("--headless=new")
        driver_pontos = webdriver.Edge(options=driver_segundo_plano)
        driver_pontos.get(minha_url)
        pontos = driver_pontos.find_element(By.XPATH,meuxpath)
        membro = driver_pontos.find_element(By.XPATH,meuxpath)
        #converte o float para int
        pontos = pontos.text.replace('.','')
        membro = membro.text.lower()
        pontos = int(pontos)
        driver_pontos.quit()
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
def verifica_membro(minha_url,meuxpath) -> int:
    '''
    Funcão responavél verificar o nivel de membro.
    Necessário passar dois parametros:
    minha_url: url do sua pgina logada
    meuxpath: o caminho do xpath
    '''
    try:
        print(texto_personalizado('Iniciado a verificação de nivel Membro'.upper()))
        #Abre navegado em segundo plano e recebe os parametros da função
        driver_segundo_plano = Options()
        driver_segundo_plano.add_argument("--headless=new")
        driver_membro = webdriver.Edge(options=driver_segundo_plano)
        driver_membro.get(minha_url)
        membro = driver_membro.find_element(By.XPATH,meuxpath)
        membro = membro.text
        driver_membro.quit()
        if membro == 'Membro Ouro':
            membro = 60
            return membro
        if membro == 'Membro Prata':
            membro = 30
            return membro
    except IndentationError as e:
        print(f'Erro de identação {e}')
    except SyntaxError as e:
        print(f'Erro de sintaxe {e}')
    except KeyboardInterrupt as e:
        print(f'Interrompido pelo usuário: {e}')
    except NameError as e:
        print(f'Variavel nao definida: {e}')

