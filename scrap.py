# Bibliotecas utilizadas, 
# pip install selenium
# pip install beautifulsoup4
# json, selenium, BeautifulSoup, datetime


from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import time
        
        
lastUrl='primeira'

def print_yellow_alert(message="Alerta: Algo pode estar errado. ⚠️"):
    """
    Exibe uma mensagem de alerta em amarelo no console.
    """
    YELLOW = "\033[93m"  # Código ANSI para cor amarela
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{YELLOW}{message} ⚠️{RESET}")

def print_green_success(message="Sucesso: Operação concluída! ✅"):
    """
    Exibe uma mensagem de sucesso em verde no console.
    """
    GREEN = "\033[92m"   # Código ANSI para cor verde
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{GREEN}{message} ✅{RESET}")

def print_blue_info(message="Informação: Aqui estão os detalhes. ℹ️"):
    """
    Exibe uma mensagem informativa em azul no console.
    """
    BLUE = "\033[94m"    # Código ANSI para cor azul
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{BLUE}{message} ℹ️{RESET}")

def print_cyan_debug(message="Depuração: Informações adicionais. 🐞"):
    """
    Exibe uma mensagem de depuração em ciano no console.
    """
    CYAN = "\033[96m"    # Código ANSI para cor ciano
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{CYAN}{message} 🐞{RESET}")

def print_magenta_input(message="Entrada: Enviando sua resposta. ⌨️"):
    """
    Exibe uma mensagem de entrada em magenta no console.
    """
    MAGENTA = "\033[95m" # Código ANSI para cor magenta
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{MAGENTA}{message} ⌨️{RESET}")
    
def print_orange_click(message="Clique: Realizando ação. 🖱️"):
    """
    Exibe uma mensagem de clique em laranja no console.
    """
    ORANGE = "\033[38;5;208m"  # Código ANSI para cor laranja (não padrão, mas próximo)
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{ORANGE}{message} 🖱️{RESET}")
    
def print_pink_select(message="Seleção: Escolhendo uma opção. 📋"):
    """
    Exibe uma mensagem de seleção em rosa no console.
    """
    PINK = "\033[38;5;200m"  # Código ANSI para cor rosa (não padrão, mas próximo)
    RESET = "\033[0m"    # Código ANSI para resetar a cor

    print(f"{PINK}{message} 📋{RESET}")
        
def print_red_error(message="Erro. ❌"):
    """
    Exibe uma mensagem de erro em vermelho no console.
    """
    # Códigos ANSI para cor de texto
    RED = "\033[91m"  # Código para cor vermelha
    RESET = "\033[0m" # Código para resetar a cor para o padrão do terminal

    print(f"{RED}{message} ❌{RESET}")

def saveToFile(output,file_name = ""):
    """
    Salva o retorno em json em um arquivo
    output -> Dados q deseja salvar
    file_name = Vazio para salvar com a data || nome do arquivo desejado
    
    """
    
    
    
    if not file_name:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"page_content_{now}"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(output)
            print(f"\nDados salvos em {file_name}")
    else :
        file_name = f"{file_name}"
        if os.path.exists(file_name):
            print(f"\nO arquivo {file_name} já existe.")
        else:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(output)
                print(f"\nDados salvos em {file_name}")
            
def get_xpath(element):
    """
    Tenta construir o XPath de um elemento BeautifulSoup.
    É uma abordagem simplificada e pode não funcionar perfeitamente para todos os casos,
    especialmente com elementos irmãos idênticos sem atributos únicos.
    """
    path = []
    current_element = element
    while current_element and current_element.name != '[document]':
        tag = current_element.name
        if not tag: 
            break
        sibling_count = 0
        current_sibling = current_element
        while current_sibling is not None:
            if current_sibling.name == tag:
                sibling_count += 1
            current_sibling = current_sibling.previous_sibling
        
        if sibling_count > 1:
            path.insert(0, f"/{tag}[{sibling_count}]")
        else:
            path.insert(0, f"/{tag}")
        
        current_element = current_element.parent

    if path and path[0] == 'html': 
        path[0] = 'html'

    return ''.join(path)

def extract_element_data(element, desired_fields=None):
    """
    Extrai informações de um elemento BeautifulSoup: tag, texto, ID e classes.
    desired_fields = None || [?'tag', ?'text_content', ?'id', ?'classes', ?'attributes', ?'xpath']
    """
    data = {}
    
    if 'tag' in desired_fields:
        data['tag'] = element.name
    
    if 'text_content' in desired_fields:
        data['text_content'] = element.get_text(strip=True)
    
    if 'id' in desired_fields:
        data['id'] = element.get('id', None)
    
    if 'classes' in desired_fields:
        data['classes'] = element.get('class', [])
    
    if 'attributes' in desired_fields:
        attrs = {}
        for attr, value in element.attrs.items():
            if attr not in ['id', 'class']: 
                attrs[attr] = value
        data['attributes'] = attrs
        
    if 'xpath' in desired_fields:
        data['xpath'] = get_xpath(element)
      
    return data

def scrape_page_to_json(url, fields_to_extract=None):
    """
    Navega até uma URL, extrai todo o conteúdo HTML,
    e o converte para um formato JSON estruturado.
    fields_to_extract = None || [?'tag', ?'text_content', ?'id', ?'classes', ?'attributes', ?'xpath']
    """
    driver = webdriver.Chrome()

    try:
        print(f"Navegando para: {url}")
        driver.get(url)
        driver.implicitly_wait(5) 

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        page_data = {
            "url": url,
            "title": soup.title.get_text(strip=True) if soup.title else None,
            "elements": []
        }

        for element in soup.find_all(True): 
            if element.name :
                element_info = extract_element_data(element, desired_fields=fields_to_extract)
                if element_info :
                    page_data["elements"].append(element_info)

        return json.dumps(page_data, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None
    finally:
        driver.quit()
    
def generate_file_name(url):
    """
    Gera um nome de arquivo baseado na URL.
    Remove caracteres especiais e espaços.
    """
    base_name = url.split('//')[-1] # Extrai o domínio
    base_name = base_name.replace('.', '_').replace('/', '_')  # Substitui pontos e barras por underlines
    return f"{base_name}.json"   
        
def scrape_page_in_progress(driver, url, fields_to_extract):
    """
    Realiza a extração de dados enquanto está executando uma tarefa
    fields_to_extract = None || [?'tag', ?'text_content', ?'id', ?'classes', ?'attributes', ?'xpath']
    """
    driver.get(url)
    driver.implicitly_wait(30)
    
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    page_data = {
            "url": url,
            "title": soup.title.get_text(strip=True) if soup.title else None,
            "elements": []
    }

    for element in soup.find_all(True): 
        if element.name :
            element_info = extract_element_data(element, desired_fields=fields_to_extract)
        if element_info :
            page_data["elements"].append(element_info)

    json_output =  json.dumps(page_data, indent=4, ensure_ascii=False)
    file_name = generate_file_name(url)
    saveToFile(json_output, file_name)
    return file_name
        
def search_json_data(json_file_path, search_field, search_term):
    """
    Busca ocorrências de um termo em um campo específico dentro de um arquivo JSON de dados raspados.

    :param json_file_path: Caminho para o arquivo JSON de entrada.
    :param search_field: O campo (chave) JSON onde a busca será realizada
                         (ex: 'title', 'tag', 'text_content', 'id', 'classes', 'xpath', 'attributes').
    :param search_term: O termo a ser procurado (case-insensitive para strings).
    :return: Uma lista de dicionários contendo as ocorrências encontradas.
    """
    found_occurrences = []
    search_term_lower = str(search_term).lower()

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{json_file_path}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar o JSON do arquivo '{json_file_path}'. Verifique a formatação.")
        return []
    if search_field == 'title':
        if data.get('title') and search_term_lower in str(data['title']).lower():
            found_occurrences.append({"type": "page_title", "value": data['title'], "url": data.get('url')})
        elif not data.get('title') and data.get('elements'):
            print(f"Aviso: Campo '{search_field}' não encontrado no nível raiz. Procurando nos elementos...")
            pass 

    if data.get('elements'):
        for element in data['elements']:
            if search_field == 'classes':
                if element.get('classes'):
                    for css_class in element['classes']:
                        if search_term_lower in str(css_class).lower():
                            found_occurrences.append(element)
                            break
            elif search_field == 'attributes':
                if element.get('attributes'):
                    for attr_value in element['attributes'].values():
                        if search_term_lower in str(attr_value).lower():
                            found_occurrences.append(element)
                            break 
            else:
                if element.get(search_field) is not None:
                    field_value = str(element[search_field]).lower()
                    if search_term_lower in field_value:
                        found_occurrences.append(element)
    return found_occurrences

def search_tag(json_file_path, field_name, text_content, return_attr, debug = False):
    """
    Busca uma tag específica em um arquivo JSON de dados raspados e retorna um atributo específico.

    :param json_file_path: Caminho para o arquivo JSON de entrada.
    :param field_name: O nome da tag a ser buscada (ex: 'input', 'button', 'a').
    :param text_content: O conteúdo de texto a ser buscado dentro da tag.
    :param return_attr: O atributo a ser retornado (ex: 'xpath', 'id', 'name').
    :param debug: Se True, imprime informações de depuração.
    :return: O valor do atributo encontrado ou None se não encontrado.
    """
    if debug:
        print(f"Buscando no arquivo {json_file_path}")
        print(f"Buscando a tag {field_name}")
        print(f"Buscando o termo {text_content}")
        print(f"Buscando retornando o {return_attr}")
        print("Buscando..")
    
    results = search_json_data(json_file_path, 'text_content', text_content)
    
    for result in results:
        
        if result.get('tag') == field_name:
            if result.get('text_content') and text_content.lower() == result.get('text_content').lower():
                if debug:
                    print_red_error(result)
                    print(f"Atributo : {return_attr} : {result.get(return_attr)}")
                    print("\n")
                return result.get(return_attr)

def search_field(json_file_path, elem , return_attr, debug = False):
    
    tag = elem.get('tag')
    type = elem.get('attributes').get('type')
    name = elem.get('attributes').get('name')
    wireModel = elem.get('attributes').get('wire:model')
    if wireModel:
        attributeType = "wire:model"
        name = wireModel
    else:
        attributeType = "name"
    
    if place_holder := elem.get('attributes').get('placeholder'):
        place_holder = elem.get('attributes').get('placeholder')
    if debug:
        print(f"Buscando no arquivo {json_file_path}")
        print(f"Buscando o elemento:  {elem}")
    if debug:
        print(f"Buscando o placeholder {place_holder}")
        print(f"Buscando a tag {tag}")
        print(f"Tipo de elemento {type}")
        if name:
            print(f"Buscando o name {name}")
        if not name:
            print(f"Buscando o wire:model {wireModel}")
    
            
    results = search_json_data(json_file_path,'attributes', type)
    for result in results:
        if result.get('tag') == tag:
            if result.get('attributes').get('type') == type:
                if result.get('attributes').get(attributeType) == name:
                    if debug:
                        print_red_error(result)
                        print_blue_info(f"Atributo : {return_attr} : {result.get(return_attr)} Tipo : {type}")
                    return result.get(return_attr)
                elif place_holder:
                    if result.get('attributes').get('placeholder') == place_holder:
                        if debug:
                            print_cyan_debug(result)
                            print_blue_info(f"Atributo : {return_attr} : {result.get(return_attr)} Tipo : {type}")
                        return result.get(return_attr)

def load_test_script_json(json_file):
    try:
        with open(f"./test_scripts/{json_file}", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{json_file}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar o JSON do arquivo '{json_file}'. Verifique a formatação.")
        return []
    return data

def findElement_xpath(scrap_file, element, debug = False):
        elem = element.get('element')
        tag = elem.get('tag')
        if debug:
            print_green_success(f"Elemento {elem}")
            print_yellow_alert(f"Tag: {tag}")
        if (tag == 'select' or tag == 'div' and elem.get('value') and elem.get('value') != {}):
            text_content = elem.get('text_content')
            get_xpath = search_tag(scrap_file, tag,text_content ,'xpath',debug=False)
            nested_value = elem.get('value')
            nested_select_tag = elem.get('value').get('tag')
            nested_select_text_content = elem.get('value').get('text_content')
            nested_xpath = search_tag(scrap_file, nested_select_tag, nested_select_text_content, 'xpath', debug=False)
            
        if(elem.get('action') and elem.get('action') != {}):
            nested_action = elem.get('action')
            nested_action_tag = nested_action.get('tag')
            nested_action_text_content = nested_action.get('text_content')
            action_xpath = search_tag(scrap_file, nested_action_tag, nested_action_text_content, 'xpath', debug=False)
            
            # get_xpath_select = search_tag(scrap_file, tag, text_content, 'xpath', debug=False)
            if debug:
                print_green_success("Select:")
                print_cyan_debug(get_xpath)
                print(f"Valor do select: {nested_value}")
                print(f"Tag do select: {nested_select_tag}")
                print(f"Texto do select: {nested_select_text_content}")
                print_cyan_debug(f"XPath do select: {nested_xpath}")
                print(f"Tag da action : {nested_action_tag}")
                print(f"Texto da action : {nested_action_text_content}")
                print_cyan_debug(f"XPath da action: {action_xpath}")
            if get_xpath:
                elem.update({'xpath': get_xpath})
                elem.update({'nested_xpath': nested_xpath})
                elem.update({'action_xpath': action_xpath})
                elem.update({'mode': 'select'})
                return elem
        elif (elem.get('text_content') and elem.get('text_content') != ''):
            text_content = elem.get('text_content')
            get_xpath = search_tag(scrap_file,tag,text_content,'xpath', debug=False)
            if debug:
                print_orange_click("Botao ou Ancora:")
                print_cyan_debug(get_xpath)
            if get_xpath:
                elem.update({'xpath': get_xpath})
                elem.update({'mode': 'click'})
                return elem
        elif (elem.get('attributes') and elem.get('attributes') != {}):
            get_xpath = search_field(scrap_file, elem ,'xpath',False)
            if debug:
                print_magenta_input("Input:")
                print_cyan_debug(get_xpath)
            if get_xpath:
                elem.update({'xpath': get_xpath})
                elem.update({'mode': 'input'})
                return elem
    
def click_elements_by_xpath_json_load(test_script_file,start_scrap = False, keep_alive = False, max_scrolls=5):
    number_of_try = 0
    data = load_test_script_json(test_script_file)    
    url = data.get('url')
    print(f"url: {url}")
    driver = webdriver.Chrome()
    if (start_scrap == False):
        print_yellow_alert("Arquivo de scrape inicial não informado ! Gerando automaticamente !")
        start_scrap = scrape_page_in_progress(driver,url,['tag', 'text_content', 'attributes','id', 'xpath'])
    time.sleep(1)
    elements = data.get('elements')  
    try:
        driver.get(url)
        for element in elements:
            number_of_try += 1
            print_blue_info(f"\nEtapa: {number_of_try}/{len(elements)}")
            tag = element.get('element').get('tag')
            print_green_success(f"Buscando no arquivo {start_scrap}")
            elem_find = findElement_xpath(start_scrap, element, debug = True)
            xpath = elem_find.get('xpath')
            mode = elem_find.get('mode')    
            driver.implicitly_wait(5)
            if not xpath:
                print("Elemento sem XPath, pulando...")
                continue
            time.sleep(1)
            print_cyan_debug(f"Buscando pelo elemento: {tag} no driver... 🔎")
            elem = driver.find_element("xpath", xpath)
            if(mode == 'click'):
                for attem in range(max_scrolls):
                    try:
                        print_orange_click()
                        text_content = element.get('element').get('text_content')
                        print_blue_info(f"Elemento encontrado: {tag} com texto: {text_content}")
                        time.sleep(1)
                        driver.implicitly_wait(2)
                        elem.click()
                        print_green_success(f"Elemento com XPath '{xpath}' clicado com sucesso ✅")
                    except Exception as e:
                        print_red_error(f"Erro ao clicar no elemento: NÃO ENCONTRADO ❌")
                        script = "scroll(0,900)"
                        print("Rolando até em baixo")
                        driver.execute_script(script)
                        print_yellow_alert("Tentando novamente após 1 segundo ⏳")
                        time.sleep(1)
                        elem.click()
                        print_green_success(f"Elemento com XPath '{xpath}' clicado com sucesso ✅")
                    finally:
                        elem = None
                        print_yellow_alert("Resetando Scroll")
                        time.sleep(1)
                        script = "scroll(0,0)"
                        driver.execute_script(script)
                        start_scrap = scrape_page_in_progress(driver, driver.current_url, ['tag', 'text_content', 'attributes','id', 'xpath'])                        
                        print_green_success(f"Scrape realizado com sucesso! Arquivo: {start_scrap}")
                    break
            elif(mode == 'input'):
                for attem in range(max_scrolls):
                    try:
                        print_magenta_input()
                        elem_name = element.get('element').get('attributes').get('name')
                        elem_input_value = element.get('element').get('attributes').get('value')
                        print_magenta_input(f"Elemento encontrado: {tag} nome: {elem_name} <- {elem_input_value}")
                        time.sleep(1)
                        elem.clear()
                        elem.send_keys(elem_input_value)
                        print_green_success(f"Campo preenchido: {elem_name} <- {elem_input_value} com sucesso ✅")
                    except Exception as e:
                        print_red_error(f"Erro ao preencher o campo: NÃO ENCONTRADO ❌")
                        script = "scroll(0,900)"
                        print("Rolando até em baixo")
                        driver.execute_script(script)
                        print_yellow_alert("Tentando novamente após 1 segundo ⏳")
                        time.sleep(1)
                    finally:
                        print_yellow_alert("Resetando Scroll")
                        script = "scroll(0,0)"
                        driver.execute_script(script)
                        time.sleep(1)
                    break
            elif(mode == 'select'):
                for attem in range(max_scrolls):
                    try:
                        print_orange_click("Try")
                        print_pink_select()
                        
                        print_blue_info(f"Abrindo select...")
                        time.sleep(1)
                        elem.click()
                        elem_select = driver.find_element("xpath", elem_find.get('nested_xpath'))
                        print_yellow_alert("Aguardando 2 segundos para o select abrir...")
                        time.sleep(1)
                        print_blue_info("Select aberto, selencionando item")
                        elem_select.click()
                        elem_action = driver.find_element("xpath", elem_find.get('action_xpath'))
                        print_yellow_alert("Aguardando 2 segundos para clicar na ação...")
                        time.sleep(1)
                        elem_action.click()
                        print_green_success(f"Elemento com XPath '{xpath}' clicado com sucesso ✅")
                        print_green_success(f"Opção com o  '{elem_find.get('nested_xpath')}'clicado com sucesso ✅")
                        time.sleep(1)
                    except Exception as e:
                        print_orange_click("Exception")
                        print_red_error(f"Erro ao clicar no SELECT: NÃO ENCONTRADO ❌")
                        
                        script = "scroll(0,900)"
                        print("Rolando até em baixo")
                        driver.execute_script(script)
                        
                        print_yellow_alert("Tentando novamente após 1 segundo ⏳")
                        print_blue_info(f"Abrindo select...")
                        time.sleep(1)
                        elem.click()
                        
                        elem_select = driver.find_element("xpath", elem_find.get('nested_xpath'))
                        print_yellow_alert("Aguardando 2 segundos para o select abrir...")
                        time.sleep(1)
                        elem_select.click()
                        
                        print_blue_info("Select aberto, selencionando item")
                        elem_action = driver.find_element("xpath", elem_find.get('action_xpath'))
                        print_yellow_alert("Aguardando 2 segundos para clicar na ação...")
                        time.sleep(1)
                        elem_action.click()
                        
                        print_green_success(f"Elemento com XPath '{xpath}' clicado com sucesso ✅")
                        print_green_success(f"Opção com o  '{elem_find.get('nested_xpath')}'clicado com sucesso ✅")
                    finally:
                        print_orange_click("Finally")
                        print_yellow_alert("Resetando Scroll")
                        time.sleep(1)
                        script = "scroll(0,0)"
                        driver.execute_script(script)
                        
                        start_scrap = scrape_page_in_progress(driver, driver.current_url, ['tag', 'text_content', 'attributes','id', 'xpath'])                        
                        print_green_success(f"Scrape realizado com sucesso! Arquivo: {start_scrap}")
                    break
    except Exception as e:
        print_red_error(f"Erro ao clicar nos elementos: Numero te tentativas excedido ❌")
        print_red_error("Excedido o numero de tentativas, o teste falhou 😭 ")
        return False
    finally:
        print_green_success("O teste foi um sucesso 🥳🥳🥳🥳")
        if(keep_alive):
            print("A janela permanecerá aberta para inspeção manual.⚠️")
            input("Pressione Enter para fechar o navegador e encerrar... ⚠️")
        driver.quit()
        
def menu():
    print_green_success("Esta ferramenta está em desenvolvimento, ela pode apresentar bugs, ou falhas !")
    print_yellow_alert("Caso seu teste não rode de primeira, tente executar novamente pois os arquivos de scrape podem não ter sidos salvos")
    print("Escolha uma opção:")
    print("[0]-> Realizar Scrap de uma pagina 🔎 -> 🌎 -> ℹ️")
    print("[1]-> Buscar conteudo do Scrap 🔎 -> ℹ️")
    print("[2]-> Teste automatico Json 🤖 -> 🧮")
    opt = input("Digite o numero: ")
    action(int(opt))
    
def action(action):
    if action == 0:
        url = input("Digite a URL para fazer o scrap: ")
        fields = ['tag', 'text_content', 'attributes', 'id', 'xpath']
        json_output = scrape_page_to_json(url, fields)
        if json_output:
            file_name = input("Digite o nome do arquivo para salvar (ou deixe vazio para usar a data): ")
            saveToFile(json_output, file_name)
            
    elif action == 1:
        print("Arquivos no diretório atual:")
        files = os.listdir('.')
        file_names = []
        for item in files:
            if os.path.isfile(item):
                if(item.split(".")[-1] == "json"):
                    file_names.append(item)
        for file_name in file_names:
            print(f"[{file_names.index(file_name)}]-{file_name}")
        json_file = input("Informe o numero do arquivo JSON para buscar: ")
        json_file = file_names[int(json_file)]
        new_search = 1
        while(new_search == 1):
            print_green_success(f"ARQUIVO SELECIONADO -> {json_file}")
            fields = ['tag', 'text_content', 'attributes', 'id', 'xpath']
            for field in fields:
                print(f"[{fields.index(field)}] - {field}")
            field = input("Campo para buscar (ex: tag, text_content, id, classes, attributes, xpath, title): ")
            field = fields[int(field)]
            term = input("Termo a ser buscado: ")
            results = search_json_data(json_file, field, term)
            if results:
                print_green_success(f"Encontrado(s) {len(results)} resultado(s):")
                for res in results:
                    print(json.dumps(res, indent=4, ensure_ascii=False))
                new_search = int (input("Deseja realizar outra busca ?\n[1]-Sim\n[2]-Não\nDigite apenas numero : "))
            else:
                print_red_error("Nenhum resultado encontrado.") 
                new_search = int (input("Deseja realizar outra busca ?\n[1]-Sim\n[2]-Não\nDigite apenas numero : "))
            
    elif action == 2:
        print_green_success("Iniciando Teste automatizado")
        print("Buscando arquivos de teste...")
        print("Arquivos no diretório atual:")
        files = os.listdir('./test_scripts')
        file_names = []
        if not files:
            print_red_error("Nenhum arquivo de teste encontrado, por favor crie um na pasta test_scripts ")
            return False
        for item in files:
            if(item.split(".")[-1] == "json"):
                file_names.append(item)
        for file_name in file_names:
                print(f"[{file_names.index(file_name)}]-{file_name}")
        opt = int(input("Informe o numero do arquivo q deseja executar: "))
        selected_file = file_names[opt]
        alive = int (input("Deseja manter o navegador aberto após o teste ?\n[1]-Sim\n[2]-Não\nDigite apenas numero : "))
        if(alive == 1):
            alive = True
        else :
            alive = False
        click_elements_by_xpath_json_load(selected_file,False, alive)
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    

    menu()

