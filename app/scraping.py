from bs4 import BeautifulSoup

# https://loja.prsim.com.br
def scrape_prsim(soup):
    nome = soup.select_one('.title-product > h1:nth-child(1)').text

    # Extrair o torque
    torque_element = soup.select_one('#content .content-product-content #tab-description #collapse-description ul:first-of-type li:first-of-type')
    if torque_element is not None:
        torque_text = torque_element.get_text(strip=True)
        nM = torque_text.replace('Torque:', '').replace(' Nm', '')
    else:
        nM = '0'  # fallback value

    valor_str = soup.select_one('#price-old').text.replace('R$', '').strip()
    valor = float(valor_str.replace('.', '').replace(',', '.'))
    return nome, nM, valor

# def scrape_site_y(soup):
#     nome = soup.select_one('.site-y-product-name').text
#     nM = soup.select_one('.site-y-product-nM').text
#     valor = float(soup.select_one('.site-y-product-price').text.replace('$', ''))
#     status_preco = soup.select_one('.site-y-product-status').text
#     return nome, nM, valor, status_preco