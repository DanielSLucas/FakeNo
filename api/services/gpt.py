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
    {"role": "user",  "content": "Título: TOP DEZ PROVAS INEGÁVEIS QUE A TERRA É PLANA\nAutor(es): \nDate de publicação: None\nResumo: Se a Terra fosse curvada e girando os oceanos da água estariam fluindo para baixo para nivelar e cobrindo a terra.A água permanece plana porque a terra é plana!Na realidade, a terra é plana e aviões apenas voam em nível plano e chegam ao seu destino facilmente porque a terra não está se movendo.Gravidade é uma farsa: http://beforeitsnews.com/strange/2015/07/flat-earth-gravity-is-a-axax-2461410.htmlTudo em nossa terra plana é naturalmente organizado por densidade e massa10) Os capitães de navio em navegação de grandes distâncias no mar nunca precisaram de fator a suposta curvatura da Terra em seus cálculos.O Pólo Sul não existe; Verdade na Antártica: http://www.atlanteanconspiracy.com/2015/06/south-pole-does-not-exist.html?m=1Mundo verdadeiro: Terra planaHttp://www.atlanteanconspiracy.com/2015/08/200-proofs-earth-is-not-spinning-ball.html?m=1Terra Geocêntrica PlanaHttps://flatgeocentricearth.wordpress.com/Marés de terra planas e o electromagnetismo do sol e da luahttps://youtu.be/_pauQitNEM0\nnFonte: http://sociedadeterraplana.com.br/?p=208"},
    {"role": "assistant", "content": "teoria da Terra plana"},
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
    - Deve usar sintaxe html para formatar o texto quando necessário.
  """

  return get_completion([
    {"role": "system", "content": prompt},
    {"role": "user",  "content": gpt_analysis_input_example},
    {"role": "assistant", "content": gpt_analysis_output_example},
    {"role": "user", "content": text}    
  ])

def mount_user_prompt(text, ai_prediction, google_results):
  return '\n\n'.join([
    f"Texto: {text}",
    f"FakeNo-AI: {ai_prediction}",
    f"Google: {google_results}"
  ])

gpt_analysis_input_example = """
Texto:
Título: TOP DEZ PROVAS INEGÁVEIS QUE A TERRA É PLANA
Autor(es): 
Date de publicação: None
Resumo: Se a Terra fosse curvada e girando os oceanos da água estariam fluindo para baixo para nivelar e cobrindo a terra.
A água permanece plana porque a terra é plana!
Na realidade, a terra é plana e aviões apenas voam em nível plano e chegam ao seu destino facilmente porque a terra não está se movendo.
Gravidade é uma farsa: http://beforeitsnews.com/strange/2015/07/flat-earth-gravity-is-a-axax-2461410.htmlTudo em nossa terra plana é naturalmente organizado por densidade e massa10) Os capitães de navio em navegação de grandes distâncias no mar nunca precisaram de fator a suposta curvatura da Terra em seus cálculos.
O Pólo Sul não existe; Verdade na Antártica: http://www.atlanteanconspiracy.com/2015/06/south-pole-does-not-exist.html?m=1Mundo verdadeiro: Terra planaHttp://www.atlanteanconspiracy.com/2015/08/200-proofs-earth-is-not-spinning-ball.html?m=1Terra Geocêntrica PlanaHttps://flatgeocentricearth.wordpress.com/Marés de terra planas e o electromagnetismo do sol e da luahttps://youtu.be/_pauQitNEM0
Fonte: http://sociedadeterraplana.com.br/?p=208

FakeNo-AI: Fake

Google: # Resultado 1:
Título: Terra plana – Wikipédia, a enciclopédia livre
Autor(es): 
Date de publicação: None
Resumo: Gravura Flammarion (1888), representando um viajante que chegou ao limite de uma Terra plana e espreita através do firmamentoO modelo da Terra plana é uma concepção arcaica do formato da Terra como um plano ou disco.
[2][3][4][5]Apesar do fato científico e das evidências óbvias da esfericidade da Terra, teorias de conspiração pseudocientíficas da Terra plana são defendidas pelas sociedades modernas da Terra plana e,[6] cada vez mais, por indivíduos não afiliados que utilizam as mídias sociais.
[47][48][49]Muitos do início da época medieval de Purana apresentam uma cosmologia da Terra plana.
[52]Antiga EuropaOs antigos povos nórdicos e germânicos acreditavam numa cosmografia da Terra plana, com a Terra cercada por um oceano e uma árvore colossal (Yggdrasil) ou um pilar (Irminsul) no centro.
"[67] A crença universal em uma Terra plana é confirmada por uma enciclopédia chinesa contemporânea a partir de 1609, que ilustra uma Terra plana que se estende sobre o plano diametral do horizonte de um céu esférico.
Fonte: https://pt.wikipedia.org/wiki/Terra_plana

# Resultado 2:
Título: Ciência - Teoria da Terra Plana está cada vez mais popular
Autor(es): Por Carolina Cunha Da Novelo Comunicação
Date de publicação: None
Resumo: Perceber a Terra como plana não quer dizer que ela realmente deve ser plana.
Até uma viagem de cruzeiro está sendo organizada por representantes da Conferência Internacional da Terra Plana, que querem ver de perto o limite do planeta.
A crença na Terra Plana não significa necessariamente uma falta de acesso à informação ou à educação formal.
Ressurgimento de uma teoria antigaNo século 19, apareceu o primeiro movimento moderno a defender a Terra Plana.
As ideias de Rowbotham foram incorporadas pela Sociedade da Terra Plana (Flat Earth Society), um grupo fundado em 1956 pelo astrônomo inglês Samuel Shenton.
Fonte: https://vestibular.uol.com.br/resumo-das-disciplinas/atualidades/ciencia---teoria-da-terra-plana-esta-cada-vez-mais-popular.htm

# Resultado 3:
Título: 5 experimentos simples para verificar que a Terra não é plana
Autor(es): Https Www.Facebook.Com Bbcnews
Date de publicação: None
Resumo: 5 experimentos simples para verificar que a Terra não é plana21 dezembro 2019Crédito, Getty ImagesPode parecer mentira, mas em pleno século 21 ainda é necessário insistir que a Terra é redonda, algo que se sabe há mais de 2 mil anos.
Algumas teorias da conspiração que afirmam que a Terra é plana continuam se espalhando.
Estas são algumas maneiras simples de comprovar que a Terra é redonda e rebater essas ideias dos terraplanistas.
Se a Terra fosse plana e você olhasse para longe, veria a mesma paisagem se estivesse no chão ou na copa da árvore.
Além disso, se a Terra fosse plana, seríamos capazes de ver o Sol ainda que fosse de noite.
Fonte: https://www.bbc.com/portuguese/curiosidades-50823002
"""

gpt_analysis_output_example='Fake\n\nCom base no texto recebido e um breve busca no Google, pode-se afirmar que a teoria da Terra plana é falsa. A ideia de que a Terra é plana é uma concepção arcaica que foi refutada pela ciência, evidências óbvias e experimentos simples. Além disso, há diversas teorias de conspiração pseudocientíficas que sustentam essa ideia, o que é uma clara indicação de falta de embasamento científico. Portanto, a notícia que traz afirmações sobre a Terra plana é falsa.<br/><b>Referências</b>: <a href="https://pt.wikipedia.org/wiki/Terra_plana">1</a>, <a href="https://vestibular.uol.com.br/resumo-das-disciplinas/atualidades/ciencia---teoria-da-terra-plana-esta-cada-vez-mais-popular.htm">2</a>, <a href="https://www.bbc.com/portuguese/curiosidades-50823002">3</a>'
