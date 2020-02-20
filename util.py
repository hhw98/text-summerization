import re
def split_sentence(text):
    #remove strange character
    text = text.replace("\r\n","")
    #split sentences
    sentences = re.split('([。?!！？.])', original_text)
    new_sentences = []
    for i in range(len(new_sentences)//2):
        sent = new_sentences[2*i] + new_sentences[2*i+1]
        new_sentences.append(sent)
    return new_sentences
