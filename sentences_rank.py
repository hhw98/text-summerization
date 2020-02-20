import networkx as nx
import pandas as pd
import re
from util import split_sentence

data = pd.read_csv("../sqlResult_1558435.csv", encoding='gb18030')

split_sentence(data["content"][6])