import os 
import codecs
import re
import json
import time
import logging
import numpy as np
import pandas as pd 
import natasha
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc
import tqdm
from tqdm.notebook import trange, tqdm
import time
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', \
                    filename='logs/backend.log', \
                    filemode='w', \
                    encoding='utf-8', \
                    level=logging.DEBUG)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

tokenCols = ['p_id', 'start', 'stop', 'text', 'token_id', 'head_id', 'rel', 'pos', 'lemma', 'anim', 'aspect', 'case', 'degree', 'gender', 'mood', 'number', 'person', 'tense', 'verb_form', 'voice']

# function for applying all of natasha's morphological tagger components to tokens to make a TokenDf
def nat_parse(textDf, textCol='text', columns=tokenCols): 
    t0 = time.time()
    # initialize collective token dataframe
    tokenDf = pd.DataFrame(columns=columns)
    # gather row list
    for an_id in tqdm(textDf.index.to_list(), desc="Text DF Index id"): 
        # initialize list of token data dicts 
        pDict = []
        # create Natasha Doc object with text
        doc = Doc(textDf.loc[an_id][textCol])
        # apply segmenter (sentenizer+tokenizer)
        doc.segment(segmenter)
        # apply morphology tagger 
        doc.tag_morph(morph_tagger)
        # apply lemmatizer
        for token in doc.tokens: 
            token.lemmatize(morph_vocab)
        # apply syntax parser
        doc.parse_syntax(syntax_parser)
        # apply NER tagger
        doc.tag_ner(ner_tagger)
        # gather all tokens' data (excluding punctuation which Natasha treats as tokens)
        for token in tqdm([x for x in doc.tokens if x.pos != 'PUNCT'], desc="Token id", leave=False): 
            start = token.start
            stop = token.stop
            text = token.text
            token_id = token.id
            head_id = token.head_id
            rel = token.rel
            pos = token.pos
            lemma = token.lemma
            # Animacy, Aspect, Case, Degree, Gender, Mood, Number, Person, Tense, VerbForm, Voice 
            # several to many for each token will be NoneType and throw an error 
            try: 
                anim = token.feats['Animacy']
            except: 
                anim = None
            try: 
                aspect = token.feats['Aspect']
            except: 
                aspect = None
            try: 
                case = token.feats['Case']
            except: 
                case = None
            try: 
                degree = token.feats['Degree']
            except: 
                degree = None
            try: 
                gender = token.feats['Gender']
            except: 
                gender = None
            try: 
                mood = token.feats['Mood']
            except: 
                mood = None
            try: 
                number = token.feats['Number']
            except: 
                number = None
            try: 
                person = token.feats['Person']
            except: 
                person = None
            try: 
                tense = token.feats['Tense']
            except: 
                tense = None
            try: 
                verb_form = token.feats['VerbForm']
            except: 
                verb_form = None
            try: 
                voice = token.feats['Voice']
            except: 
                voice = None
            #print(token)
            # make dictionary of all these things 
            tokenDict = {
                'p_id': an_id,
                'start': start, 
                'stop': stop, 
                'text': text, 
                'token_id': token_id, 
                'head_id': head_id, 
                'rel': rel, 
                'pos': pos, 
                'lemma': lemma, 
                'anim': anim, 
                'aspect': aspect, 
                'case': case, 
                'degree': degree, 
                'gender': gender, 
                'mood': mood, 
                'number': number, 
                'person': person, 
                'tense': tense, 
                'verb_form': verb_form, 
                'voice': voice
            }
            # append to dict list 
            pDict.append(tokenDict)
            # make DF for section 
            pDf = pd.DataFrame(pDict, columns=columns)
        # append section DF to collective DF
        tokenDf = pd.concat([tokenDf, pDf])
    t1 = time.time()
    logging.info(f"{t1-t0}")
    # return collective DF
    return tokenDf

def GetRankDf(TokenDf, col='lemma', no_stop=True): 
    if no_stop: 
        sourceDf = TokenDf.loc[~TokenDf[tokenCols[9:]].isna().all(1)]
    else:
        sourceDf = TokenDf
    RankDf = sourceDf[col].value_counts().to_frame().rename(columns={col:'n'})
    RankDf.index.name = col
    RankDf['rank'] = np.arange(1,len(RankDf)+1)
    return RankDf

def textRegularize(libTextsDf, w_id):
    chap_works = (6, 14, 22)
    # grab text
    textDf = libTextsDf.iloc[[w_id]]
    if w_id in chap_works:
        # split into chapters
        textDf = pd.DataFrame(data=textDf.text.str.split(r'\n\n').to_list()[0])
        # get chapter list
        chapTitles = textDf.iloc[::2][0].to_list()
        chapTexts = textDf.iloc[1::2][0].to_list()
        # add chapters to df
        textDf = pd.DataFrame(data={'chap':chapTitles, 'text':chapTexts})
        # clean chapter list of white space
        textDf.chap = textDf.chap.str.replace('\W', '', regex=True)
        # label parts
        textDf['part'] = ['1' if chap < 29 else '2' for chap in range(len(textDf.chap))]
        # break chapters into paragraphs
    textDf = textDf['text'].str.split(' \n', expand=True).stack().to_frame().reset_index().rename(columns={'level_0':'chapID','level_1':'para',0:'text'})
    #else:textDf = pd.DataFrame(data={'text':textDf.text.str.split(r'\n').to_list()[0]})
    # regularize
    textDf['text'] = textDf.text.str.replace('\n|\s{2,}', '')
    # remove white space paragraphs
    textDf = textDf.loc[~textDf.text.str.contains(r"^\W*$", regex=True)]
    #textDf['part'] = textDf.chapID.apply(lambda x: int('1') if x < 30 else int('2'))
    #textDf['chap'] = textDf.chapID.map(textDf['chapID'].to_dict())
    textDf['para'] = textDf['para'].apply(lambda x: x+1)
    textDf['paraID'] = range(1, len(textDf)+1)
    if w_id in chap_works:
        textDf['chapID'] = textDf['chapID'].apply(lambda x: x+1)
        return textDf
    else:
        return textDf[['text', 'paraID']]
    
# make XML from text
def makeXML(textTitle, textDf, textXmlDf):
    root = etree.Element("text")
    print(root.tag)
    pt = ch = cn = pa = pn = 0
    nameDict = textDf.chap.to_dict()
    for chap in chapList:
        #print(f"Chap {chap}")
        root.append(etree.Element("chapter", n=str(cn+1), name=nameDict.get(chap)))
        paraList = textXmlDf.loc[(textXmlDf['part'] == part) & (textXmlDf['chapID'] == chap)].index
        #print(paraList)
        for paragraph in paraList:
            #print(f"Paragraph {paragraph}")
            root[ch].append(etree.Element("paragraph", n=str(pn+1), name=str(pa+1)))
            paraText = textXmlDf.loc[paragraph].text
            #print(f"paraText: {paraText}")
            #print(f"pt = {pt}; ch = {ch}; paragraph = {paragraph}")
            root[ch][pa].text = paraText
            pa+=1
            pn+=1
        pa=0
        ch+=1
        cn+=1
    #print(etree.tostring(root, pretty_print=True, xml_declaration=True))
    writePath = '..site/texts/'+textTitle+'.xml'
    etree.ElementTree(root).write(writePath, pretty_print=True, xml_declaration=True, encoding='windows-1251')