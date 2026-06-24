from funcoes import func_principal,load
from personalizacao import texto_personalizado


def main():
    func_principal()

if __name__ == "__main__":
    print(texto_personalizado('Inicializando...'.upper()))
    load(0.01,texto="         ")
    print(texto_personalizado(' Sistema de Pesquisas Automaticas Mircrosoft Rewards ').upper())
    main()