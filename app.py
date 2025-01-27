from gnews import GNews
from googlenewsdecoder import gnewsdecoder
from newspaper import Article
from newspaper import Config
from transformers import pipeline
from tokenizers.decoders import WordPiece

pipe = pipeline("token-classification", model="dicta-il/dictabert-ner", device=0)
pipe.tokenizer.backend_tokenizer.decoder = WordPiece()
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 5
interval_time = 1

google_news = GNews(
    language='he',
    country='IL',
    period='60d',
    start_date=None,
    end_date=None,
    max_results=5,
)

news = google_news.get_news('bdo')

articles_title = [
   news[1]['title']
]
print(articles_title)
oracle = pipe(articles_title)
print(oracle)
source_urls = [
    news[1]['url']
    ]

for url in source_urls:
              
 decoded_url_dict = gnewsdecoder(url, interval=interval_time)

 decoded_url = decoded_url_dict.get('decoded_url', '')

if not decoded_url.startswith(('http://', 'https://')):
    decoded_url = 'https://' + decoded_url

article = Article(decoded_url, language='he', config=config)
article.download()
article.parse()
print(article.text)

