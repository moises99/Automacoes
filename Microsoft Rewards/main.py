from funcoes import func_principal,load,definido_diariamente,continue_ganhando,reivindicar,LINKS,VARIAVEIS,resumo,coleta_noticias
from personalizacao import texto_personalizado
from rich import print



def main():
    func_principal()
    # listopc =['Rotina Completa','Definidos Diariamente','Continue Ganhando','Reivindicar Pontos','Sair']

    # while True:
    #     [print(f'[{p}] - {t}') for p,t in enumerate(listopc,start=1)]
    #     opc = input(str('Escolha uma rotina: ').upper()).strip()
    #     if opc.isnumeric():
    #         opc = int(opc)
    #     else:
    #         print(' Escolcha um ooção válida!')
    #         continue
    #     match opc:
    #         case 1:
    #             func_principal()
    #         case 2:
    #             definido_diariamente(LINKS["home_page"])
    #         case 3:
    #             continue_ganhando(LINKS["home_page"])
    #         case 4:
    #             reivindicar(LINKS["home_page"])
    #         case 5:
    #             print(texto_personalizado('Finalizando...').upper())
    #             break
    #         case _:
    #             continue

if __name__ == "__main__":
    print(texto_personalizado(' Sistema de Pesquisas Automaticas Mircrosoft Rewards ').upper())
    load(0.01,texto="    Inicializando     ".upper())
    main()