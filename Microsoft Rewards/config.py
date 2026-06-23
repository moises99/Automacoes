#Definição das variaveis globais
import secrets
import datetime as dt


LINKS = {
    "home_page"  : "https://rewards.bing.com/dashboard",
    #"msn_news"   : "https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1",
    "msn_news"   : "https://www.bing.com/news/search?q=Brasil&nvaug=%5bNewsVertical+Category%3d%22rt_Brazil%22%5d&FORM=NSBABR",
    "continue_ganhando" : "https://rewards.bing.com/earn"
    }


XPATH_PAGINA = {
    "membro"                    : "//p[@class='rounded-ctrlBadgeCorner px-2 py-1 text-globalCaption1Strong text-rewardsLevelBadgeFg bg-rewardsGoldBadgeBg']",
    "pontos"                    : "//p[@class='text-pageHeader']",
    "reivindicar"               : "//button[@class='group/ctrl text-start cursor-pointer disabled:cursor-default outline-0 outline-ctrlFocusOuterStroke outline-offset-(--spacing-ctrlFocusInnerStrokeWidth) data-focus-visible:outline-ctrlFocusOuterStrokeWidth w-full rounded-cornerCardDefault']",
    "ganhar_mais_pontos"        : "//span[@class='relative px-paddingCtrlTextSide inline-flex items-center pt-paddingCtrlLgTextTop pb-paddingCtrlLgTextBottom gap-gapBetweenContentXSmall']",
    #"definidos_diariamente"     : "//p[@class='line-clamp-3 text-fgCtrlNeutralSecondaryRest']",
    "definidos_diariamente"     : "//p[@class='line-clamp-3 text-globalBody2Strong']",
    "ganhe_mais"                :"//span[@class='relative px-paddingCtrlTextSide inline-flex items-center pt-paddingCtrlTextTop pb-paddingCtrlTextBottom gap-gapBetweenContentXxSmall']",
    "continue_ganhando"         : "//p[@class='line-clamp-3 text-globalBody2Strong']",
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


    }
