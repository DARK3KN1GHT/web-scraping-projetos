import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def buscar_produtos_ecommerce():
    print("🛒 --- SISTEMA DE INTELIGÊNCIA DE MERCADO & E-COMMERCE --- 🛒\n")

    # Entrada interativa: o usuário escolhe o que quer procurar
    termo_busca = (
        input("🔍 O que você deseja buscar no catálogo? (Ex: star, love, etc.): ")
        .strip()
        .lower()
    )

    if not termo_busca:
        termo_busca = "book"

    # Capturando a data e hora atual para auditoria e nomeação de arquivos
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_formatada_exibicao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    # URL base do catálogo público de testes de e-commerce
    url_base = "http://books.toscrape.com/catalogue/"
    url_atual = "http://books.toscrape.com/catalogue/page-1.html"

    produtos_coletados = []
    pagina = 1

    print(
        f"\n🚀 Robô acionado! Buscando por '{termo_busca}' nas páginas do fornecedor...\n"
    )

    while url_atual:
        resposta = requests.get(url_atual)

        if resposta.status_code != 200:
            break

        soup = BeautifulSoup(resposta.text, "html.parser")
        itens = soup.find_all("article", class_="product_pod")

        for item in itens:
            titulo = item.find("h3").find("a")["title"]

            # Limpeza robusta do preço
            preco_raw = item.find("p", class_="price_color").text
            preco_limpo = (
                preco_raw.replace("£", "")
                .replace("Â", "")
                .replace("Â£", "")
                .strip()
            )

            try:
                preco = float(preco_limpo)
            except ValueError:
                continue

            # Filtra caso o termo de busca esteja no título
            if termo_busca in titulo.lower():
                produtos_coletados.append(
                    {"Produto": titulo, "Preco (£)": preco}
                )

        # Paginação automática
        botao_next = soup.find("li", class_="next")
        if botao_next:
            proximo_link = botao_next.find("a")["href"]
            url_atual = url_base + proximo_link
            pagina += 1
        else:
            url_atual = None

    # Ordenando os produtos do mais barato para o mais caro
    produtos_coletados.sort(key=lambda x: x["Preco (£)"])

    # Salvando os resultados em um arquivo CSV com nome dinâmico único
    nome_arquivo = f"produtos_{termo_busca}_{data_hora_atual}.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Produto", "Preco (£)"])
        writer.writeheader()
        writer.writerows(produtos_coletados)

    # --- 📊 RELATÓRIO DE ENTREGA EXECUTIVA PARA O CLIENTE ---
    print("=" * 60)
    print("📋 RELATÓRIO EXECUTIVO DE ENTREGA - INTELIGÊNCIA DE PREÇOS")
    print("=" * 60)
    print(f"🎯 Termo Pesquisado        : {termo_busca.upper()}")
    print(f"⏱️ Data/Hora da Varredura  : {data_formatada_exibicao}")
    print(f"📦 Oportunidades Encontradas : {len(produtos_coletados)}")
    print(f"💾 Relatório Exportado em    : {nome_arquivo}")
    print("-" * 60)

    if produtos_coletados:
        print("🏆 MELHOR OFERTA ENCONTRADA (Menor Preço):")
        melhor = produtos_coletados[0]
        print(f"   • Produto : {melhor['Produto']}")
        print(f"   • Preço   : £ {melhor['Preco (£)']:.2f}")
        print("-" * 60)

        print("📋 TOP PRODUTOS ECONÔMICOS:")
        for idx, prod in enumerate(produtos_coletados[:3], start=1):
            print(f"   {idx}. {prod['Produto']} — £ {prod['Preco (£)']:.2f}")
    else:
        print(
            "❌ Nenhum produto encontrado com esse termo. Tente outra palavra-chave!"
        )

    print("=" * 60)
    print("✨ Processo concluído com sucesso e pronto para o cliente!")


if __name__ == "__main__":
    buscar_produtos_ecommerce()