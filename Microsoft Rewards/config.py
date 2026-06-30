#Definição das variaveis globais
import secrets
import datetime as dt
from pathlib import Path
import os

# caminho = Path("laalalalala","lilili")
# caminho.mkdir(parents=True, exist_ok=True)
# print("Caminho criado com sucesso!")

LINKS = {
    "home_page"         : "https://rewards.bing.com/dashboard",
    "msn_news"          : "https://www.bing.com/news/search?q=Brasil&nvaug=%5bNewsVertical+Category%3d%22rt_Brazil%22%5d&FORM=NSBABR",
    "continue_ganhando" : "https://rewards.bing.com/earn"
    }


XPATH_PAGINA = {
    "membro"                                : "//p[@class='rounded-ctrlBadgeCorner px-2 py-1 text-globalCaption1Strong text-rewardsLevelBadgeFg bg-rewardsGoldBadgeBg']",
    "pontos"                                : "//p[@class='text-pageHeader']",
    "click_reivindicar"                     : "//button[@class='group/ctrl text-start cursor-pointer disabled:cursor-default outline-0 outline-ctrlFocusOuterStroke outline-offset-(--spacing-ctrlFocusInnerStrokeWidth) data-focus-visible:outline-ctrlFocusOuterStrokeWidth w-full rounded-cornerCardDefault']",
    "ganhar_mais_pontos_reivindicar"        : "//span[@class='relative px-paddingCtrlTextSide inline-flex items-center pt-paddingCtrlLgTextTop pb-paddingCtrlLgTextBottom gap-gapBetweenContentXSmall']",
    "click_continue_ganhando"               : "//a[@class='group/ctrl cursor-pointer data-disabled:cursor-default outline-0 outline-ctrlFocusOuterStroke focus-visible:outline-ctrlFocusOuterStrokeWidth rounded-cornerCardDefault']",
    "ponto_continue_ganhando"               : "//span[@class='font-semibold']",
    "titulos_continue_ganhando"             : "//p[@class='line-clamp-3 text-globalBody2Strong']",
    "click_definidos_diariamente"           : "//a[@class='group/ctrl cursor-pointer data-disabled:cursor-default outline-0 outline-ctrlFocusOuterStroke focus-visible:outline-ctrlFocusOuterStrokeWidth rounded-cornerCardDefault']",
    "titulo_definidos_diariamente"          : "//p[@class='line-clamp-3 text-globalBody2Strong']"
    }

CHAVE_ID = {
    "chave" : secrets.token_hex(26).upper()
    }


VARIAVEIS = {
    "data_hora"             : dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
    "local_arquivo"         : 'D:\\py\\Projeto Automacao\\logs_pesquisa\\',
    "nome_arquivo"          : f'manchete_{dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}',
    "ver_processo"          : False,
    "controle_pontos"       : 0,
    "controle_tres_pontos"  : 0,
    "c_ganhando"            : 0,
    "d_diariamente"         : 0,
    "total_reivindicar"     : 0,
    }