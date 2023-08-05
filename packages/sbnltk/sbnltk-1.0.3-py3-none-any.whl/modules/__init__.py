

__version__ ="1.0.1"

from modules.Bangla_translator import bangla_google_translator
from modules.NER import UncustomizeNER
from modules.Downloader import downloader
from sbnltk.sentimentAnalyzer import SentimentAnalyzer
from modules.Stemmer import stemmerOP
from modules.posTag import postag
from modules.sent2sent_embedding import sent2sent
from modules.Preprocessor import preprocessor
from modules.word2vec_embedding import word2vec