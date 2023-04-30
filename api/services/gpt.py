from os import getenv
import openai

openai.api_key = getenv("OPENAI_API_KEY")

def get_completion(messages: list):  
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
  )

  return response.choices[0].message.content 


def fix_summary(summary):  
  return get_completion([
    {"role": "system", "content": "Você melhora resumos oriundos de web scraping and extractive summarization.(Melhore apenas o resumo, mantenha as demais informações em seus lugares, fazendo apenas pequenas correções)"},
    {"role": "user", "content": summary}
  ])


def get_google_query(text):
  prompt = """
  Você escreve queries de busca para serem utilizadas no google.

  Você recebe um pequeno texto, e responde com o assunto do texto.

  Sua resposta:
    - Deve ser escrita em uma linguagem simples;
    - Deve ser no máximo do tamanho de uma linha;
    - Deve ser escrita de forma que possa ser copiada e colada no google;
    - Não deve estar entre aspas para não ser interpretado de maneira literal pelo google.
  """

  return get_completion([
    {"role": "system", "content": prompt},
    {"role": "user", "content": text}    
  ])

def get_gpt_analysis(text):
  prompt = """
  Você:
    - é um assistente de combate a notícias e informações falsas;
    - trabalha em conjunto com uma IA para classificar notícias como verdadeiras ou falsas.

  FakeNo-AI é a IA que te auxilia a classificar, ela é feita usando TfidfVectorizer e LogisticRegression e foi treinada com entorno de dez mil notícias de diversas categorias, chegando a oitenta por cento de acurária.

  Você deve elaborar um parágrafo em relação a sua conclusão sobre a veracidade da notícia ou informação que receber.

  Você vai receber as informações no seguinte formato:
  
  Texto: <informação ou notícia que deve ser classificada como real ou fake.>
  
  FakeNo-AI: <classificação feita pela IA: 'Fake' ou 'Real'.)>

  Google: <Três resumos do conteúdo dos três primeiros resultados de uma BREVE pesquisa no google, ao buscar sobre o assunto da notícia ou informação a ser classificada.>
  
  Sua resposta:
    - Deve começar seu parágrafo com "Fake" ou "Real", a depender de sua conclusão;
    - Deve ser escrita em linguagem simples;
    - Deve chegar a uma conclusão sobre a veracidade do texto recebido;
    - Deve explicar o porquê de sua conclusão.
    - Deve ignorar as informações recebidas somente quando não tiverem ligação com o assunto a ser classificado;
    - Deve apontar as fontes que utilizou para chegar a sua conclusão;
    - Deve sinalizar de maneira clara quando não tiver certeza em relação ao resultado de sua classificação.
  """

  return get_completion([
    {"role": "system", "content": prompt},
    {"role": "user", "content": text}    
  ])

def mount_user_prompt(text, ai_prediction, google_results):
  return '\n\n'.join([
    f"Texto: {text}",
    f"FakeNo-AI: {ai_prediction}",
    f"Google: {google_results}"
  ])
