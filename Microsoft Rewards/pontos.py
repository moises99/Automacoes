from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from personalizacao import texto_personalizado

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
            membro = 54
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
