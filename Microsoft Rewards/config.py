#Definição das varias globais
import secrets
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
