import requests
import networkx as nx
import pandas as pd
import re
import jieba
import math
from termcolor import colored, cprint
import webcolors

rhy_words = []

def rhymes(word = "sun"):
    base_url = 'https://api.datamuse.com/words'
    params = { 'rel_rhy':word }
    results = requests.get(base_url, params).json()
    global rhy_words
    for r in results:
        rhy_words.append(r['word'])
		
def get_rhymes():
    global rhy_words
    return rhy_words
	
	

#summarization
stopwords_path = r"C:\Users\hyh6hhy\Downloads\项目二\update\stopwords.txt"
def split_sentence(text):
    #remove strange character
    text = text.replace("\r\n","")
    #split sentences
    sentences = re.split('([。?!！？.])', text)
    new_sentences = []
    for i in range(len(sentences)//2):
        sent = sentences[2*i] + sentences[2*i+1]
        new_sentences.append(sent)
    return new_sentences
def get_stop_words(stopwords_file):
    stop_words = []
    for line in open(stopwords_file, 'r', encoding='utf-8'):
        stop_words.append(line.replace('\n', ''))
    return stop_words

#Chinese
def get_token(sent):
    #remove punctuation for Chinese
    sent = re.findall(r'[\d|\w]+', sent)
    stopwords = get_stop_words(stopwords_path)
    #Chinese
    words = list(jieba.cut("".join(sent)))
    #remove stopwords
    words = list(set(words) - set(stopwords))
    return words

#English
def get_token(sent):

    stopwords = get_stop_words(stopwords_path)
    words = list(sent.split())
    #remove stopwords
    words = list(set(words) - set(stopwords))
    return words




        


# In[57]:


def sentences_ranking(text, title):
    #get sentences graph
    sentences, sentences_graph, title_flag = get_connect_graph_by_weight_text_rank(text, title)
    #get sentence rank
    ranking_sentences = nx.pagerank(sentences_graph)

    #sort except for title
    if title_flag:
        ranking_sentences.pop(0)

    sorted_ranking_sentences = sorted(ranking_sentences.items(), key = lambda x:x[1], reverse = True)
    return sorted_ranking_sentences, sentences


# In[58]:


def get_connect_graph_by_weight_text_rank(text, title):
    """
    text : text body for one news
    title: title for one news
    """
    #text preprocess
    sentences = split_sentence(text)
    tokens = [get_token(s) for s in sentences]
    #title preprocess
    title_flag = False
    #if title:
    #    title_token = get_token(title)
    #    if title_token:
    #        title_flag = True
    #        tokens.insert(0, title_token)
    #        sentences.insert(0, title)
    #add edges
    sentences_graph = nx.Graph()
    for ii, sentence in enumerate(tokens):
        for i in range(ii+1, len(tokens)):
            if len(set(tokens[i])) < 5:
                continue
            num_same_words = len(set(tokens[ii]).intersection(set(tokens[i])))
            #double weight for first sentence
            if ii == 0:
                similarity = 2 * num_same_words / (math.log(len(tokens[ii])) + math.log(len(set(tokens[i])))) 
            else:
                similarity = num_same_words / (math.log(len(tokens[ii])) + math.log(len(set(tokens[i]))))
            
            sentences_graph.add_edges_from([(ii, i)],weight = similarity)
    return sentences, sentences_graph, title_flag
	

# In[106]:


def get_summarization_by_textrank(text, title = None, left_num = 4):
    """
    text : text body of news
    title: title of news
    summary ratio : ratio of sentence number between text body and summary
    """
    if text == None:
        print("please input text !")
        return None
    #get sentence ranking
    ranking_sentences_id, sentences = sentences_ranking(text, title)
    
    print("The number of text : ", len(ranking_sentences_id))
	
    #summarization_level = int(int(level_ratio)/5*len(ranking_sentences_id))
	
    left_num = int(left_num)
    
    #sentence_candidates = ranking_sentences_id[:left_num]
	
    sentence_candidates = {s[0]:webcolors.rgb_to_hex((255, int(245/left_num)*i, int(245/left_num)*i)) for i,s in enumerate(ranking_sentences_id[:left_num])}
    sentence_candidates.update({s[0]:webcolors.rgb_to_hex((255, 255, 255)) for i,s in enumerate(ranking_sentences_id[1+left_num:])})
    
    print("The number of summarization: ", len(sentence_candidates))
 
    #print(sentence_candidates)
    #print([(sentences[s],sentence_candidates[s]) for s in sorted(sentence_candidates)])
	
    return ([(sentences[s],sentence_candidates[s]) for s in sorted(sentence_candidates)]), "".join([(sentences[s[0]]) for s in sorted(ranking_sentences_id[:left_num])])
	
	
#