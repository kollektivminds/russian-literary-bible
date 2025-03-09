import os 
import codecs
import re
import json
import random
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
from IPython.display import HTML, display

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
    
# numerically sort dictionary by value
def sort_dict(dictionary, ascending=False):
    sorted_dict = {
    k: v for k, v in sorted(
        dictionary.items(), 
        key=lambda item: item[1], 
        reverse=True
        )
    }

    return sorted_dict

#!curl --silent https://xkcd.com/color/rgb.txt | grep -E '(\w+\s?\w?\s?)(#[[:alnum:]]{6})' > xkcd_colors.txt
xkcd_colors_list = './xkcd_colors.txt'
with open(xkcd_colors_list, 'r') as f: 
    xkcd_colors = f.readlines()
xkcd_colors_dict = {}
for color in [x.split('\t') for x in xkcd_colors]:
    xkcd_colors_dict.update({color[0]:color[1]})
    
def xkcd_color_picker():
    color_id = list(xkcd_colors_dict.items())[random.randint(0, len(xkcd_colors_dict)-1)]
    return color_id

cmap_colors = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

def cmap_color_picker():
    color_id = cmap_colors[random.randint(0, len(cmap_colors)-1)]
    return color_id

def display_side_by_side(*dfs, titles=()):
    html_str = ""
    if titles:
        for df, title in zip(dfs, titles):
            html_str += f"<h3>{title}</h3>"
            html_str += df.to_html()
    else:
        for df in dfs:
            html_str += df.to_html()
    html_str = f'<div style="display:flex;">{html_str}</div>'
    display(HTML(html_str))