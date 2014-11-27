
from cos_recom import acrecommender
a=acrecommender(0)
a.loaddata("/Users/leilei/Documents/Python/data/ml-100k/")
a.acrecom('4',10)
