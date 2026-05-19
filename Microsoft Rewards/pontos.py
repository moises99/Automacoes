from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


#Verfica q quantidade de pontos do usuário
def verica_pontos():
    driver_segundo_plano = Options()
    driver_segundo_plano.add_argument("--headless=new")
    driver_pontos = webdriver.Edge(options=driver_segundo_plano)
    driver_pontos.get('https://rewards.bing.com/status/pointsbreakdown')
    pontos = driver_pontos.find_element(By.XPATH,"//p[@class='pointsDetail c-subheading-3 ng-binding']")
    pontos = pontos.text[:2]
    pontos = int(pontos)
    print(f'Pontos atuais: {pontos}/90')
    if pontos == 90:
        print(f"Você atingiu o máximo de pontos")
        driver_pontos.quit()
        return True
    driver_pontos.quit()
    return False

