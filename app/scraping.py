from bs4 import BeautifulSoup
import re
import requests

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
    status = 'ativo'
    return nome, nM, valor, status

def scrape_king_moza(soup):
    # Seleciona o texto do link e divide em palavras
    marca_text = soup.select_one('a[itemprop="url"]').text.split()
    
    # Seleciona a primeira palavra (MOZA)
    marca = marca_text[0]
    
    # Seleciona o texto do título do produto
    produto_text = soup.select_one('.nome-produto.titulo').text
    
    # Seleciona a última palavra (R9)
    produto = produto_text.split()[-1]
    
    # Concatena a marca e o produto
    nome = marca + ' - ' + produto

    # Extrai o valor de nM do título do produto
    nM_match = re.search(r'(\d+)(nm|m)', produto_text, re.IGNORECASE)
    if nM_match:
        nM = nM_match.group(1)
    else:
        nM = '0'  # fallback value

    valor_str = soup.select_one('.desconto-a-vista .titulo').text.replace('R$', '').replace('.', '').replace(',', '.')
    valor = float(valor_str)
    status = 'ativo'
    return nome, nM, valor, status

def scrape_real_drive(soup):
    # Extrai o nome do produto e substitui 'Direct Drive' por 'Real Drive'
    nome = soup.select_one('.product_title').text.replace('Direct Drive', 'Real Drive')

    # Usa uma expressão regular para extrair os dois dígitos após o primeiro dígito que segue o 'T' no nome
    match = re.search(r'T\d(\d{2})', nome)
    if match:
        # Se um número foi encontrado, converte para um inteiro
        nM = int(match.group(1))
    else:
        # Se nenhum número foi encontrado, define nM como 0
        nM = 0

    # Seleciona o elemento com a classe 'woocommerce-Price-amount amount'
    element = soup.select_one('.fswp_in_cash_price > p:nth-child(1) > span:nth-child(2) > bdi:nth-child(1)')

    # Obtém o texto do elemento, remove o 'R$', substitui o ponto por nada e a vírgula por um ponto
    text = element.text.replace('R$', '').replace('.', '').replace(',', '.')

    # Converte o texto para um float
    valor = float(text)


    status = 'ativo'
    return nome, nM, valor, status

def scrape_cockpitextremeracing(soup):
    # Extrai o nome do produto
    marca = soup.select_one('#ficha .board_htm table tr:nth-child(5) td:nth-child(2)').text
    modelo = soup.select_one('#ficha .board_htm table tr:nth-child(3) td:nth-child(2)').text
    nome = marca + ' - ' + modelo

    # Extrai o texto do elemento h1 com a classe product-name e remove espaços extras
    product_name = soup.select_one('h1.product-name').text.strip()

    # Usa uma expressão regular para extrair o número que precede "Nm" no product_name
    match = re.search(r'(\d+)\s*Nm', product_name)
    if match:
        # Se um número foi encontrado, converte para um inteiro
        nM = int(match.group(1))
    else:
        # Se nenhum número foi encontrado, define nM como 0
        nM = 0

    # Seleciona o elemento com o seletor CSS fornecido
    element = soup.select_one('#info_preco > span:nth-child(2)')

    # Verifica se o elemento existe antes de tentar acessar o atributo text
    if element is not None:
        # Obtém o texto do elemento
        text = element.text
        # Usa uma expressão regular para remover todos os caracteres não numéricos
        text = re.sub(r'[^\d,]', '', text).replace(',', '.')
        # Converte o texto para um float
        valor = float(text)
        status = "ativo"
    else:
        # Se o elemento não existe, verifica se o produto está indisponível
        element = soup.select_one('span.botao-commerce.botao-nao_indisponivel')
        if element is not None and "Não disponível" in element.text:
            valor = 0
            status = "inativo"
        else:
            # Se o produto não está indisponível, define valor como None ou algum valor padrão
            valor = None
            status = "desconhecido"

    return nome, nM, valor, status

def scrape_ziuc(soup):
    nome = 'Ziuc Direct Drive'
    
    # Seleciona o elemento com o seletor CSS fornecido
    element = soup.select_one('.col-lg-6.align-self-center > h4')

    # Verifica se o elemento existe antes de tentar acessar o atributo text
    if element is not None:
        # Obtém o texto do elemento
        text = element.text
        # Usa uma expressão regular para extrair o número do texto
        match = re.search(r'\d+', text)
        if match is not None:
            nM = int(match.group())
        else:
            nM = None  # ou algum valor padrão
    else:
        nM = None  # ou algum valor padrão

    # Seleciona o elemento com o seletor CSS fornecido
    element = soup.select_one('.col-lg-6.align-self-center > span.price')

    # Verifica se o elemento existe antes de tentar acessar o atributo text
    if element is not None:
        # Obtém o texto do elemento
        text = element.text
        # Remove o "R$" e substitui a vírgula por um ponto
        text = text.replace('R$', '').replace('.', '').replace(',', '.')
        # Converte o texto para um float
        valor = float(text)
    else:
        valor = None  # ou algum valor padrão

    status = 'ativo'

    return nome, nM, valor, status


# def scrape_site_y(soup):
#     nome = soup.select_one('.site-y-product-name').text
#     nM = soup.select_one('.site-y-product-nM').text
#     valor = float(soup.select_one('.site-y-product-price').text.replace('$', ''))
#     status_preco = soup.select_one('.site-y-product-status').text
#     return nome, nM, valor, status_preco