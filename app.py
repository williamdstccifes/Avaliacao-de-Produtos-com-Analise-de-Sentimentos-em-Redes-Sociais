### Comandos para executar a aplicação:
# pip install -r requirements.txt
# python app.py

# Importação das bibliotecas necessárias
import os
import googleapiclient.discovery
from langdetect import detect, LangDetectException
from googleapiclient.errors import HttpError
import re
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizer
from flask import Flask, request, render_template

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Defina sua chave de API do Google aqui
API_KEY = 'YOUR_API_KEY'

# Crie uma instância do serviço do YouTube
youtube_service = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Carregue o modelo BERT pré-treinado e o tokenizador
model_path = 'Modelo'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')

# Tamanho máximo de sequência
max_seq_length = 128

# Classe para representar os resultados de cada vídeo
class VideoResult:
    def __init__(self, video_title, video_description, total_positivos, total_negativos):
        self.video_title = video_title
        self.video_description = video_description
        self.total_positivos = total_positivos
        self.total_negativos = total_negativos

# Função para buscar vídeos de avaliações de produtos no YouTube
def search_product_review_videos(youtube, search_query, maxResults=1000):
    video_info = []
    kwargs = {
        'q': search_query,
        'type': 'video',
        'part': 'id,snippet',  # Solicite as informações de snippet (incluindo título e descrição)
        'maxResults': maxResults,
        'regionCode': 'BR',
    }

    results = youtube.search().list(**kwargs).execute()

    while results:
        for item in results['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_description = item['snippet']['description']
            video_info.append({'video_id': video_id, 'video_title': video_title, 'video_description': video_description})

        results = youtube.search().list_next(results, kwargs)

    return video_info

# Função para tratar e gravar os comentários em português brasileiro em um arquivo
def process_and_save_comments(youtube, video_id, product_keywords, output_file, model, tokenizer, max_seq_length, **kwargs):
    comments = []
    next_page_token = None  # Inicialize o próximo token de página

    # Crie uma expressão regular para fazer correspondência com as palavras-chave do produto
    product_regex = re.compile(r'|'.join(map(re.escape, product_keywords)), re.IGNORECASE)

    while True:
        try:
            results = youtube.commentThreads().list(videoId=video_id, **kwargs).execute()
        except HttpError as e:
            if e.resp.status == 403:
                print(f'Os comentários estão desabilitados para o vídeo com ID: {video_id}')
                return
            else:
                raise e

        for item in results.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            try:
                # Tente detectar o idioma do comentário
                if detect(comment) == 'pt':
                    # Use a expressão regular para verificar se o comentário menciona as palavras-chave do produto
                    if re.search(product_regex, comment):
                        # Limpeza básica de texto (remova caracteres especiais e espaços extras)
                        comment = re.sub(r'\W', ' ', comment)
                        comment = re.sub(r'\s+', ' ', comment).strip()

                        # Truncar ou preencher o comentário para o tamanho máximo de sequência
                        comment = comment[:max_seq_length]

                        # Classifique o comentário usando o modelo
                        inputs = tokenizer(comment, truncation=True, padding='max_length', max_length=max_seq_length, return_tensors="pt")
                        with torch.no_grad():
                            model.eval()
                            scores = model(**inputs)[0]
                        prob_pos = F.softmax(scores, dim=1)[:, 1]

                        # Suponha que prob_pos contenha a probabilidade da classe positiva
                        limiar_probabilidade = 0.5  # Você pode ajustar este limiar conforme necessário

                        # Verifique se a probabilidade da classe positiva é maior que o limiar
                        if prob_pos > limiar_probabilidade:
                            classe_resultante = "Positivo"
                        else:
                            classe_resultante = "Negativo"

                        comments.append((comment, classe_resultante, prob_pos.item()))

            except LangDetectException:
                # Lidar com erros de detecção de idioma
                pass

        # Verifique se há mais páginas de comentários
        next_page_token = results.get('nextPageToken')

        if next_page_token:
            kwargs['pageToken'] = next_page_token
        else:
            break

    # Grava os comentários em um arquivo de texto com classificação e probabilidade
    with open(output_file, 'a', encoding='utf-8') as file:
        for comment, classe, prob in comments:
            file.write(f'Comentário: {comment}\n')
            file.write(f'Classificação: {classe}\n')
            file.write(f'Probabilidade da classe positiva: {prob}\n\n')

    # Retorna o token de página para a verificação
    return next_page_token

# Rota para a página inicial com o formulário de pesquisa
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        product_keywords = request.form['product_keywords'].split(',')  # Converta as palavras-chave em uma lista
        return render_template('results.html', search_query=search_query, product_keywords=product_keywords)
    return render_template('index.html')

# Rota para exibir os resultados da pesquisa
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    product_keywords = request.form['product_keywords'].split(',')
    max_results = int(request.form['max_results'])  # Recupera a quantidade desejada de vídeos

    # Nome do arquivo de saída
    output_file = 'comentarios_classificados.txt'

    # Crie o arquivo de saída antes de usá-lo
    open(output_file, 'w').close()

    # Encontre vídeos de avaliações de produtos no Brasil e obtenha informações sobre eles
    video_info_list = search_product_review_videos(youtube_service, search_query, maxResults=max_results)

    # Lista para armazenar os resultados de cada vídeo
    video_results = []

    overall_total_positivos = 0
    overall_total_negativos = 0

    for video_info in video_info_list:
        video_id = video_info['video_id']
        video_title = video_info['video_title']
        video_description = video_info['video_description']

        print(f'Capturando e classificando comentários em português brasileiro para o vídeo com ID: {video_id}')

        page_token = None
        while True:
            page_token = process_and_save_comments(youtube_service, video_id, product_keywords, output_file, model, tokenizer, max_seq_length, part='snippet', textFormat='plainText', pageToken=page_token)

            if not page_token:
                break

        total_positivos = 0
        total_negativos = 0

        with open(output_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith('Classificação: Positivo'):
                    total_positivos += 1
                elif line.startswith('Classificação: Negativo'):
                    total_negativos += 1

        overall_total_positivos += total_positivos
        overall_total_negativos += total_negativos

        video_result = VideoResult(video_title=video_title, video_description=video_description, total_positivos=total_positivos, total_negativos=total_negativos)
        video_results.append(video_result)

    # Exiba os resultados na página de resultados, incluindo os totais
    return render_template('results.html', video_results=video_results, search_query=search_query, product_keywords=product_keywords, overall_total_positivos=overall_total_positivos, overall_total_negativos=overall_total_negativos)

# Execução do aplicativo Flask quando o script é executado
if __name__ == '__main__':
    app.run(debug=True)