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
        #converte o float para int
        pontos = pontos.text.replace('.','')
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
