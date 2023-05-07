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

  Você recebe um pequeno texto, e resume o assunto do texto em uma linha.

  Sua resposta:
    - Deve ser escrita em uma linguagem simples;
    - Deve ser no máximo do tamanho de uma linha;
    - Deve ser escrita de forma que possa ser copiada e colada no google;
    - Não deve estar entre aspas para não ser interpretado de maneira literal pelo google.
  """

  return get_completion([
    {"role": "system", "content": prompt},
    {"role": "user",  "content": "Título: Após acordo, Orlando Silva entrega versão final do PL das Fake News com mudanças\nAutor(es): Gazeta Do Povo\nDate de publicação: None\nResumo: O deputado Orlando Silva (PCdoB-SP) protocolou na noite desta quinta-feira (27) a versão final do Projeto de Lei 2.630/2020 (leia aqui na íntegra), também conhecido como PL das Fake News.A votação da proposta pelo plenário da Câmara dos Deputados está prevista para ocorrer na próxima terça-feira (2).Mais cedo, Silva se reuniu com o presidente da Câmara, Arthur Lira (PP-AL), para definir os últimos pontos do texto.No início da semana, a Câmara dos Deputados aprovou o regime de urgência para a analise do PL.Entre as sanções estabelecidas para as redes sociais, está a suspensão temporária das atividades, medida que já constava na versão anterior.\nFonte: https://www.gazetadopovo.com.br/vida-e-cidadania/apos-acordo-orlando-silva-entrega-versao-final-do-pl-das-fake-news-com-mudancas/"},
    {"role": "assistant", "content": "PL das Fake News"},
    {"role": "user", "content": text},
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
    - Deve sempre chegar a uma conclusão sobre a veracidade do texto recebido;
    - Deve sempre começar com "Fake" ou "Real" (de acordo com sua conclusão) e pular duas linhas;
    - Deve explicar o porquê de sua conclusão.
    - Deve ser escrita em linguagem simples;
    - Deve ignorar as informações recebidas somente quando não tiverem ligação com o assunto a ser classificado;
    - Deve apontar as fontes que utilizou para chegar a sua conclusão (a menos que seja a mesma que originou o texto);
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
