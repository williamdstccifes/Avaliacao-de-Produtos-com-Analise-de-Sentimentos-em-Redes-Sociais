# Tutorial para Executar o Código

Este tutorial fornecerá instruções passo a passo sobre como configurar e executar o código disponível neste repositório.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado o Python em seu sistema. Você pode baixar o Python em [python.org](https://www.python.org/).

## Passos para Executar o Código

### Clone o Repositório:

Abra um terminal.

Execute o seguinte comando para clonar o repositório:

```
git clone https://github.com/williamdstccifes/Avaliacao-de-Produtos-com-Analise-de-Sentimentos-em-Redes-Sociais
```

### Instale as Dependências:

Navegue até o diretório do projeto:

```
cd Avaliacao-de-Produtos-com-Analise-de-Sentimentos-em-Redes-Sociais
```

Execute o seguinte comando para instalar as dependências listadas no arquivo "requirements.txt":

```
pip install -r requirements.txt
```

### Configure a Chave de API do Google:

Abra o arquivo app.py em um editor de texto.

Procure a linha que contém a variável "API_KEY" e substitua "YOUR_API_KEY" pela sua própria chave de API do Google. Você pode obter uma chave de API em Google Developers Console.

### Execute o Aplicativo Flask:

Ainda no terminal, execute o seguinte comando para iniciar o aplicativo Flask:

```
python app.py
```

O aplicativo será iniciado e estará disponível em "http://127.0.0.1:5000/".

### Acesse o Aplicativo no Navegador:

Abra um navegador da web e acesse [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

O aplicativo exibirá uma página inicial com um formulário de pesquisa.

### Realize uma Pesquisa:

Preencha o formulário de pesquisa com as informações desejadas, incluindo a consulta de pesquisa, palavras-chave do produto e a quantidade desejada de vídeos.

Clique no botão de pesquisa.

### Visualize os Resultados:

O aplicativo exibirá os resultados da pesquisa, incluindo informações sobre os vídeos e a classificação dos comentários.

### Encerre o Aplicativo:

Quando terminar de usar o aplicativo, volte ao terminal e pressione "Ctrl + C" para encerrar a execução do aplicativo Flask.


---
Isso conclui o tutorial para configurar e executar o código. Certifique-se de ter todas as dependências instaladas e seguir os passos corretamente. Se você encontrar problemas ou tiver dúvidas, consulte a documentação das bibliotecas utilizadas ou entre em contato com o desenvolvedor do código.
