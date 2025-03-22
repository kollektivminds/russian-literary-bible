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
import multiprocessing as mp
from multiprocessing import Pool, Process
import pickle
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc
import tqdm
from tqdm.notebook import trange, tqdm
import time
import matplotlib.pyplot as plt
from IPython.display import HTML, display

# logging config
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', \
                    filename='logs/backend.log', \
                    filemode='w', \
                    encoding='utf-8', \
                    level=logging.DEBUG)

# natasha parameters
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

# token columns' names
tokenCols = ['p_id', 'start', 'stop', 'text', 'token_id', 'head_id', 'rel', 'pos', 'lemma', 'anim', 'aspect', 'case', 'degree', 'gender', 'mood', 'number', 'person', 'tense', 'verb_form', 'voice']

# cmap color names for picker
cmap_colors = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

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

# make a DataFrame of top (non-stopword) words by quantity, ranked
def GetRankDf(TokenDf, col='lemma', no_stop=True): 
    if no_stop: 
        sourceDf = TokenDf.loc[~TokenDf[tokenCols[9:]].isna().all(1)]
    else:
        sourceDf = TokenDf
    RankDf = sourceDf[col].value_counts().to_frame().rename(columns={col:'n'})
    RankDf.index.name = col
    RankDf['rank'] = np.arange(1,len(RankDf)+1)
    return RankDf

# make a regularized DataFrame of paragraphs from a raw text
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
    etree.ElementTree(root).write(writePath, \
                                  pretty_print=True, \
                                  xml_declaration=True, \
                                  encoding='windows-1251')
    
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
    
def add_stopword(origDf):
    # add stopword boolean, True if all attribute columns are null
    good_pos = ['NOUN', 'ADJ', 'VERB', 'PROPN']
    origDf['stopword'] = ~origDf.pos.isin(good_pos)
    TokenDfIdx = pd.Index(range(1, (origDf.shape[0]+1)), name='id')
    origDf.index = TokenDfIdx# = TokenDf.set_index(['p_id', 'token_id'])
    return origDf

def common_lemmas(parent, child):
    child_lemmas = []
    child_lemmas_count = 0

    for lemma in set(child):
        #print(lemma)
        if lemma in parent.unique():
            child_lemmas.append(lemma)
            child_lemmas_count += 1
        else:
            pass

    return f"Shared unique words between text and the Bible: "+str(child_lemmas_count)+", that's ~"+str(round(((child_lemmas_count/len(set(parent.unique())))*100),2))+"%"

def compare_list_frequency(*args,
                           consider_order=False,
                           consider_duplicates=True,
                           handle_unhashable=False,
                           key=None,
                           frequency_format="dict"):    
    list_hit_list = []
    for arg in args:
        list_hit_dict = {}
        other_args = args[:args.index(arg)] + args[args.index(arg)+1:]
        for word in set(arg):
            word_hit_count = 0
            for other_arg in other_args:
                word_hit_count += list(other_arg).count(word)
            if word_hit_count > 0:
                list_hit_dict[word] = word_hit_count
            #print(f"{word}: {list(bible_lemmas[:1000]).count(word)}")
        list_hit_list.append(list_hit_dict)

    return(list_hit_list)

def ListSplit(lst, numGroups, sort=True): 
    """Takes a list and a number and splits the 
    list into evenly divided n groups (as much as possible)"""
    # choose to sort list by ascending
    if sort: 
        lst.sort()
    # get length of list given to sort
    listLen = len(lst)
    # groupLen is the maximum number of items per group to allow for the most groups <= numGroups in a list (numGroups-1 OR numGroups)
    groupLen = (listLen//numGroups) + (listLen % numGroups > 0)
    # yield generator object of nested listed with length of numGroups 
    for i in range(0,len(lst), groupLen): 
        yield lst[i:i+groupLen]

def token_window(lemma_array, window_size):
    token_window_array = np.array([])
    token_window_array = np.array([np.array(lemma_array[i:i+window_size]) for i in range(len(lemma_array)-(window_size-1))])
    return token_window_array

def token_window_mp(lemma_array, window_size):
    #token_window_array = np.array([])
    token_window_array = enumerate([list(lemma_array[i:i+window_size]) for i in range(len(lemma_array)-(window_size-1))])
    return token_window_array

def get_sim_count(child_window_array, parent_window_array, order_matters=False):
    work_sim_count = 0
    work_sim = []
    for child_window in child_window_array:
        child_sim = {}
        #print(f"child window: {child_window}")
        child_window_sim_total_count = 0
        for parent_window in parent_window_array:
            #print(f"parent window: {parent_window}")
            child_window_sim_sub_count = 0
            for i in range(len(child_window)):
                if order_matters:
                    if child_window[1][i] == parent_window[1][i]:
                        child_window_sim_total_count+=1
                        child_window_sim_sub_count+=1
                else:
                    if child_window[1][i] in parent_window[1]:
                        #print(f"{child_window[i]} is in parent!")
                        child_window_sim_total_count+=1
                        child_window_sim_sub_count+=1
                    #else:
                        #print(f"{child_window[i]} is not in parent!")
            child_sim.update({parent_window[0]: child_window_sim_sub_count})
        #print(f"{child_window}: {child_window_sim_total_count}")
        work_sim.append({child_window_sim_total_count: child_sim})
    return work_sim

def dna_test_windows(child_lemmas, parent_lemmas, window_size=10):
    sim_counter = 0
    #sim_list = np.array([])
    parent_window_array = token_window(parent_lemmas, window_size)
    child_window_array = token_window(child_lemmas, window_size)
    sim_list = get_sim_count(child_window_array, parent_window_array)
    #print(sim_list)
    return sim_list

def dna_test_windows_mp(child_lemmas, parent_lemmas, window_size=10):
    #child_lemmas, parent_lemmas = cnp_lemmas[0], cnp_lemmas[1]
    #print(f"Child lemmas: {child_lemmas}")
    #print(f"Parent lemmas: {parent_lemmas[:10]}")
    sim_counter = 0
    sim_list = np.array([])
    parent_window_array = token_window_mp(parent_lemmas, window_size)
    child_window_array = token_window_mp(child_lemmas, window_size)
    sim_list = get_sim_count(child_window_array, parent_window_array)
    return sim_list

def window_count_sim_mp(child_window_array, parent_window_array, order_matters=False):
    sim_count_tuples = {}
    for (c_sub_array_id, c_sub_array_list) in child_window_array:
        c_sub_sim_count = 0
        for (p_sub_array_id, p_sub_array_list) in parent_window_array:
            c_p_sim_count = 0
            for i in range(len(c_sub_array_list)):
                if order_matters:
                    if c_sub_array_list[i] == p_sub_array_list[i]:
                        c_sub_sim_count += 1
                        c_p_sim_count += 1
                else:
                    if c_sub_array_list[i] in p_sub_array_list:
                        c_sub_sim_count += 1
                        c_p_sim_count += 1
            sim_count_tuples[(c_sub_array_id, p_sub_array_id)] = c_p_sim_count
    return sim_count_tuples