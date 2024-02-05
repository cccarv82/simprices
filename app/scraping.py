from bs4 import BeautifulSoup

# https://loja.prsim.com.br
def scrape_prsim(soup):
    nome = soup.select_one('.title-product > h1:nth-child(1)').text
    nM = soup.select_one('#collapse-description > ul:nth-child(4) > li:nth-child(1) > p:nth-child(1) > span:nth-child(2)').text
    nM = nM.replace('Nm', '').strip()
    valor_str = soup.select_one('#price-old').text.replace('R$', '').strip()
    valor = float(valor_str.replace('.', '').replace(',', '.'))
    return nome, nM, valor

# def scrape_site_y(soup):
#     nome = soup.select_one('.site-y-product-name').text
#     nM = soup.select_one('.site-y-product-nM').text
#     valor = float(soup.select_one('.site-y-product-price').text.replace('$', ''))
#     status_preco = soup.select_one('.site-y-product-status').text
#     return nome, nM, valor, status_preco