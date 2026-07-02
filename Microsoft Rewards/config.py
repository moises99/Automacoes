#Definição das variaveis globais
import datetime as dt


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

VARIAVEIS = {
    "data_hora"             : dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
    "nome_arquivo"          : f'destaques_{dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}',
    "ver_processo"          : False,
    "controle_pontos"       : 0,
    "controle_tres_pontos"  : 0,
    "c_ganhando"            : 0,
    "d_diariamente"         : 0,
    "total_reivindicar"     : 0,
    }
