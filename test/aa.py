# https://rare-technologies.com/word2vec-tutorial/
from gensim.models import Word2Vec
embedding_model = Word2Vec(tokenized_contents, size=100, window = 2, min_count=50, workers=4, iter=100, sg=1)
print(embedding_model.most_similar(positive=["news"], topn=100))