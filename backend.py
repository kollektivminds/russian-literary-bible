import re
import json
import time
import logging
import numpy as np
import pandas as pd 
import natasha
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', \
                    filename='backend.log', \
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
    for an_id in textDf.index: 
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
        for token in [x for x in doc.tokens if x.pos != 'PUNCT']: 
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