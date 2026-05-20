from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep as sl
from pontos import verica_pontos




if verica_pontos() == True:
    ...
else:
    #Cria a conexao com o site *Necessário estar logado
    url = 'https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1'
    driver_edge = Options()
    driver_edge.add_argument("--headless=new")
    driver = webdriver.Edge(options=driver_edge)
    driver.get(url)


    #Lista de noticias
    titulo_noticia = []
    lista_noticia_formatada = []


    # #Rolagem da Pagina
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sl(2)
    sl(.2)


    #Elementos apos a Rolagem
    # titulos_noticia = driver.find_elements(By.XPATH,"//div[@class='news-card newsitem cardcommon nosnip']")
    titulos_noticia = driver.find_elements(By.XPATH,"//a[@class='title']")


    for titulos in titulos_noticia:
        manchete = titulos.text
        if len(manchete) > 5:
            titulo_noticia.append(manchete)
            noticias_formatadas = str(titulos.text).replace(' ','%20').replace(',','%2C').replace(':','%3A').replace(';','%3B').replace("'","%27")
            lista_noticia_formatada.append(noticias_formatadas)
            sl(.1)

    #Print nas manchetes e concatena as mesma com o link
    print(f'Total de noticias: {len(titulo_noticia)}')
    for pos,titulo in enumerate(titulo_noticia):
        print(f'Notícia {pos+1} = Manchete: {titulo}\nLINK: https://www.bing.com/search?q={lista_noticia_formatada[pos]}&form=IPRV10')
        print()
        driver.get(f'https://www.bing.com/search?q={lista_noticia_formatada[pos]}&form=IPRV10')
        sl(3)
        if pos == 30:
            if verica_pontos() == True:
                driver.quit()
                break
        elif pos > 60:
            if verica_pontos() == True:
                driver.quit()
                break     


    driver.quit()
