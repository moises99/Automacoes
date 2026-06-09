#Definição das varias globais
import secrets
import datetime as dt
LINKS = {
    "home_page" : "https://rewards.bing.com/dashboard",
    "msn_news"  : "https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1",
    }


XPATH_PAGINA = {
    "membro" : "//span[@class='font-semibold']",
    "pontos" : "//p[@class='text-pageHeader']",

    }


CHAVE_ID = {
    "chave" : secrets.token_hex(26).upper()
    }


VARIAVEIS = {
    "data_hora" : dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
    "local_arquivo": 'D:\\py\\Projeto Automacao\\logs_pesquisa\\',
    "nome_arquivo" : f'manchete_{dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}',
    }
