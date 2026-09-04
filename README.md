# Microsoft Rewards Auto Search

Automação desenvolvida em Python para realizar pesquisas automaticamente no Microsoft Rewards, auxiliando no acúmulo de pontos diários de forma prática.

## ✨ Funcionalidades

- Realiza pesquisas automáticas no Bing.
- Suporte para pesquisas em Desktop.
- Monitoramento da pontuação atual.
- Interface simples via terminal.
- Configurações personalizáveis.

## 📋 Requisitos
- Estar logando em https://rewards.bing.com/ 
- Python 3.10 ou superior
- Microsoft Edge
- ChromeDriver ou WebDriver compatível

## 📦 Instalação
Clone o repositório:
```bash
git clone https://github.com/moises99/Automacoes.git
```

Instale as dependências:

```bash
pip install -r requirements.txt
```


## 🚀 Como usar
Execute o programa:

```bash
python main.py
```

A automação só funcionará se estiver feito o login anteriomente, verificará a pontuação atual e realizará as pesquisas necessárias até atingir o limite diário.
Também fará os desafio e conjuntos diarios. 

## 📊 Recursos
- Verificação automática de pontos.
- Compatível com Windows.

## 📁 Estrutura do Projeto

```text
Microsoft Rewards/
├── main.py
├── requirements.txt
├── config.py
├── funcoes.py
```

## ⚠️ Aviso

Este projeto é destinado exclusivamente para fins educacionais e de aprendizado em automação com Python e Selenium. O uso desta ferramenta pode violar os Termos de Serviço do Microsoft Rewards. Utilize por sua própria conta e risco.

## 🛠️ Tecnologias Utilizadas

- Python
- Selenium
- Rich
- WebDriver Manager
