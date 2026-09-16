import csv
import requests
from bs4 import BeautifulSoup


def raspar_e_salvar_dados():
    url_base = "http://quotes.toscrape.com"
    url_atual = url_base

    pagina = 1
    total_citacoes_geral = 0
    dados_para_salvar = []

    print("🚀 Iniciando o robô de Web Scraping com Paginação e Salvamento...\n")

    while url_atual:
        print(f"📄 Raspando a Página {pagina}: {url_atual}")

        resposta = requests.get(url_atual)

        if resposta.status_code != 200:
            print(f"❌ Erro ao acessar a página. Código: {resposta.status_code}")
            break

        soup = BeautifulSoup(resposta.text, "html.parser")
        lista_de_citacoes = soup.find_all("div", class_="quote")

        print(
            f"   -> Encontradas {len(lista_de_citacoes)} citações nesta página."
        )

        for item in lista_de_citacoes:
            texto = item.find("span", class_="text").text
            autor = item.find("small", class_="author").text
            total_citacoes_geral += 1

            # Guardando os dados em uma lista de dicionários
            dados_para_salvar.append({"Autor": autor, "Citacao": texto})

        botao_next = soup.find("li", class_="next")

        if botao_next:
            proximo_link = botao_next.find("a")["href"]
            url_atual = url_base + proximo_link
            pagina += 1
            print("-" * 50)
        else:
            print("\n🏁 Fim da paginação! Coleta concluída.")
            url_atual = None

    # Salvando os dados coletados em um arquivo CSV
    nome_arquivo = "citacoes.csv"
    print(f"\n💾 Salvando os dados no arquivo '{nome_arquivo}'...")

    # Abrindo o arquivo em modo de escrita ('w') com codificação UTF-8 para aceitar acentos
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
        # Definindo as colunas da planilha
        colunas = ["Autor", "Citacao"]
        escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)

        # Escrevendo o cabeçalho
        escritor.writeheader()

        # Escrevendo todas as linhas de dados coletadas
        for linha in dados_para_salvar:
            escritor.writerow(linha)

    print(f"✨ Arquivo '{nome_arquivo}' gerado com sucesso!")
    print(f"📊 Total geral de citações salvas: {total_citacoes_geral}")


if __name__ == "__main__":
    raspar_e_salvar_dados()