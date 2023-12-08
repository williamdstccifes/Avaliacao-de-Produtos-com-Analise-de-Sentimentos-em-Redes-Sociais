# Treinamento do Modelo de Análise de Sentimentos

Este tutorial fornece instruções para executar o treinamento do modelo de análise de sentimentos. O código utiliza a biblioteca Transformers da Hugging Face com o modelo BERT em português pré-treinado.

## Começando

Essas instruções permitirão que você execute o treinamento do modelo em sua máquina local para fins de desenvolvimento e teste.

### Pré-requisitos

Antes de começar, certifique-se de ter instalado o Python em seu sistema. Você pode baixar o Python em [python.org](https://www.python.org/).

### Instalação

Abra um terminal e execute o seguinte comando para instalar as dependências necessárias:

```
pip install matplotlib numpy pandas plotly torch scikit-learn transformers tqdm
```

### Conjunto de Dados

O conjunto de dados utilizado para o treinamento pode ser encontrado [aqui](https://www.kaggle.com/code/viniciuscleves/an-lise-de-sentimento-com-bert/input). Certifique-se de baixar o arquivo "imdb-reviews-pt-br.csv" e colocá-lo no mesmo diretório do script.

### Executando o Treinamento

Execute o seguinte comando para iniciar o treinamento:

```
python treinamento_analise_sentimentos.py
```

Durante o treinamento, o script exibirá informações sobre a perda (loss) e a acurácia do modelo. O treinamento pode levar algum tempo, dependendo do hardware disponível.

Ao final do treinamento, o modelo será salvo no diretório "Modelo".

## Avaliação do Modelo

O script também inclui uma avaliação do modelo na fase de teste, exibindo uma curva ROC e a acurácia em diferentes thresholds. Além disso, é possível realizar a classificação de sentimentos em frases personalizadas após o treinamento.

## Inferência com Modelo Treinado

Para realizar inferências com o modelo treinado em novos textos, você pode usar o seguinte código como exemplo:

```
# Importação do modelo treinado para realizar a classificação de sentimentos em frases
from transformers import BertForSequenceClassification, BertTokenizer

# Carregamento do modelo e tokenizador treinados
model_path = 'Modelo'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')

# Exemplo de classificação de sentimento em uma frase personalizada
texto_personalizado = "Este é um ótimo exemplo de como usar o modelo de linguagem."
inputs = tokenizer(texto_personalizado, return_tensors="pt")

# Inferência do modelo na frase personalizada
with torch.no_grad():
    model.eval()
    scores = model(**inputs)[0]

# Cálculo da probabilidade da classe positiva
prob_pos = F.softmax(scores, dim=1)[:, 1]

# Definição de um limiar de probabilidade para a classificação
limiar_probabilidade = 0.5

# Classificação final com base no limiar
if prob_pos > limiar_probabilidade:
    classe_resultante = "Positivo"
else:
    classe_resultante = "Negativo"

# Impressão do resultado da classificação
print(f"Texto classificado como: {classe_resultante}")
print(f"Probabilidade da classe positiva: {prob_pos.item()}")
```

Certifique-se de substituir o texto personalizado com o que deseja classificar.


---
Este tutorial fornece as etapas necessárias para treinar um modelo de análise de sentimentos em textos em português e realizar inferências com o modelo treinado. Certifique-se de seguir as instruções e ajustar conforme necessário para atender aos seus requisitos específicos.
