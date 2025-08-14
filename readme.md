<h1> Auto Scrap.py <h1>

<p> Esta é uma ferramenta desenvolvida para simplificar e parametrizar testes automaticos com selenium e python. <p>

## Dependencias
<ul>
    <li> <code> selenium </code></li>
    <li> <code> BeautifulSoup </code></li>
    <li> <code> json </code></li>
    <li> <code> os </code></li>
    <li> <code> time </code></li>
</ul>

## Como usar?
<p>
Para iniciar a ferramenta basta executar o comando :
<code>python3 rscrap.py</code> no seu terminal.<br>
</p>

## Funções disponiveis

<h3>Realizar Scrap de uma pagina 🔎 -> 🌎 -> ℹ️ </h3><br>
Esta opção solicita uma URL e realiza o scrap de um e salva em um arquivo JSON de sua preferencia ou com a data atual, caso nada seja informado. O arquivo ficará disponivel na pasta raiz do projeto. <br>

<h3>Buscar conteudo do Scrap 🔎 -> ℹ️ </h3><br>
Após a realização do <b>Scrap</b> da pagina, a opçào buscar conteudo irá ajudar a encontrar os metada dados de um determinado elementos em um dos arquivos de scrap. Primeiramente a função irá solicitar que o indice do arquivo desejado seja informado,logo em seguida ela irá solicitar q tipo de atributo será utilizado na busca <code>[tag, text_content, attributes, id, xpath]</code>. Finalmente será solicitado o termo a ser buscado e então a ferramenta irá retornar <b>todos</b> os elementos encontrados no arquivo json conforme o parametro e valor solicitados.<br>

<h3>Teste automatico Json 🤖 -> 🧮 </h3><br>
Esta opcão permite a realização do teste automatizado e também irá gerar arquivos de scrap automaticamente para toda ação de <code>seleção</code>, seja clique em ancoras ou botões. Para utilizar esta função, primeiramente é nescessário a criação dentro de test_scripts de um <code>".json"</code>, eg. <code>"test_login.json"</code>.. O conteudo do documento deve seguir uma formalização, indicando 2 elementos principais a <code>"url"</code> e o <code>"elements", onde ficará todos os elementos de ação</code>.

# Exemplo base do arquivo de test_login.json
```json
{
    "url" : "https://SuaUrl/rota.com",
    "elements" : [
     #Seus elementos aqui
     {
         "element"{}
     },
     {
         "element"{}
     }
     .
     .
     .
    ]
}
```
# Exemplo de input
Para isso basta inserir um element, informar sua tag como input e logo em seguida nos seus attributes, definir seu tipo, nome e valor q deseja inserir no campo.
````json
{
    "element": {
        "tag": "input",
        "attributes":{
            "type": "email",
            "name" :"email",
            "value" : "teste@teste.com"
        }
    }
},  
````

# Exemplo de button

````json
{
    {
        "element": {
            "tag": "button",
            "text_content" :"Entrar"
        }
    }
},  
````

# Exemplo de anchor link

````json
{
    "element": {
        "tag": "a",
        "text_content" : "Entrar"
    }
},
`````

# Exemplo de select
Como em alguns frameworks como no <code>Live wire<code> o select tem as opções carregadas de forma assincrona o mesmo não fica disponivel para seleção imediatamente. com isso é necessário trata-lo como se fosse um grupo de ações, onde se clica em um texto, neste caso em uma div, e logo em seguida o elemento terá a sua action, q será uma acão de clique para um button, baseado no seu text content

````json
{
    "element": {
        "tag" : "div",
        "text_content": "Selecione um Tipo de Estudo",
        "value": {
            "tag" : "div",
            "text_content": "Book"
        },
        "action" : {
            "tag" : "button",
            "text_content": "Adicionar Tipo de Estudo"
        }
    }
},
````

#Exemplo de radio

```json
{
    "element": {
        "input" :"feature_review",
        "type": "radio",
        "value": "Snowballing"  
    }
},  
````

#Exemplo de textarea

```json
{
    "element": {
        "textarea" :"objectives",
        "value" :"Objetivos do meu projeto q eu nao sei"
    }
},
````
