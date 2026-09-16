import requests
from bs4 import BeautifulSoup


def executar_scraping():
    # URL de exemplo (um site seguro e público para testes)
    url = "https://example.com"

    print(f"🔄 Conectando-se ao site: {url}...")

    # Fazendo a requisição HTTP para baixar o site
    resposta = requests.get(url)

    # Verifica se a requisição deu certo (código 200)
    if resposta.status_code == 200:
        print("✅ Conexão bem-sucedida!\n")

        # Analisando o HTML da página com o BeautifulSoup
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Extraindo o título da página
        titulo = soup.find("h1").text.strip()
        paragrafo = soup.find("p").text.strip()

        print(f"📌 Título encontrado: {titulo}")
        print(f"📄 Parágrafo encontrado: {paragrafo}")
    else:
        print(f"❌ Erro ao acessar o site. Código: {resposta.status_code}")


if __name__ == "__main__":
    executar_scraping()