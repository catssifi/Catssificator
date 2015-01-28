#!/usr/bin/python
# Copyright (c) 2015 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2014 Dec - 2015

from lib.utils import words,debug,get_sorted_turple_on_dict_by_value,get_word_tag_str,get_similar_words_with_word_tags,is_correct,edits1,is_known_word,is_in_the_list
from lib.loggable import Loggable
from textblob import TextBlob, Word
from ai.ai_reader import AIReader, map_word_tag_to,WORD_TYPE_LIST,WORD_TYPE
#_words_counts_model = AIDatabaseBuilder.Instance().load_words_counts_model()

THE_NUM_OF_TOP_WORD_TAGS_TO_RETRIEVED=2
THE_NUM_OF_TOP_SIMILAR_WORDS_TO_RETRIEVED=10

class Frequency_Occurence(object):
     def __init__(self, frequency, occurence):
         self.frequency = frequency
         self.occurence = occurence
         
     def add(self, frequency, occurence):
         self.frequency += frequency
         self.occurence += occurence
         
     def __lt__(self, other):
         return (self.frequency <= other.frequency) and (self.occurence < other.occurence)

#word_tags is a list of format: list: [[('JJ', 8), ('NN', 4)], list: [('NN', 4)]]
#It returns the list of the most predicted word_tag sorted, e.g. ['N', 'J']
def reduce_from_word_tags_list(word_tags_list):
    t_with_frequencies={}
    for word_tags in word_tags_list:
        if word_tags:
            for word_tag in word_tags:
                t = map_word_tag_to(word_tag[0])
                this_frequency = word_tag[1]
                if t in t_with_frequencies:
                    t_with_frequencies[t].add(this_frequency, 1)
                else:
                    t_with_frequencies[t] = Frequency_Occurence(this_frequency, 1)
    ts = map(lambda x: x[0], get_sorted_turple_on_dict_by_value(t_with_frequencies, reverse_the_result=True))
    return ts

def score_this_suggested_word(w_suggestion, adjacency_word_list, orig_word, is_this_current_word_spell_correct):
    r=AIReader.Instance()
    N=THE_NUM_OF_TOP_SIMILAR_WORDS_TO_RETRIEVED
    score=0.0
    this_suggested_word=w_suggestion[0]
    for t in WORD_TYPE_LIST():
        results_t=r.get_top_noun_similarity(this_suggested_word,N, t)
        if results_t:
            for word_similarity in results_t:
                if t in adjacency_word_list and word_similarity[0] in adjacency_word_list[t]:
                    score += word_similarity[1]
    if not is_this_current_word_spell_correct and score == 0.0:
        score=w_suggestion[1]   #take the default calculated score from the textblob
    return score

def build_word_list_by_tag(pos_tags):
    d = {}
    for pos_tag in pos_tags:
        t = map_word_tag_to(pos_tag[1])
        if not t in d:
            d[t] = list()
        d[t].append(str(pos_tag[0]))
    return d

def get_word_to_left_and_right(sps, i):
    return sps[i-1] if i > 0 else None, sps[i+1] if i < len(sps)-1 else None



COMPAREABLE_WORD_RAW=edits1('than')
def pick_the_mostly_grammar_correct_one(qualified_suggested_word_list, position_on_sps, sps):
    if not qualified_suggested_word_list:
        return None
    first_suggested_word = qualified_suggested_word_list[0][0]
    #Rule 1: Pick 'Stronger' over 'Strong' if there is a 'Than' following it
    if position_on_sps < len(sps)-1 and sps[position_on_sps+1][0] in COMPAREABLE_WORD_RAW and get_word_tag_str(first_suggested_word)=='JJ':
        #Ok, i should pick the 'er' one instead if there exists one 
        found=False
        for q_s_w in qualified_suggested_word_list:
            if q_s_w[0][-2:]=='er' and q_s_w[0][:2]==sps[position_on_sps][0][:2]:
                qualified_suggested_word_list=[q_s_w]   #found!
                found=True
                break
        if not found:
            new_fixed_word=None
            if first_suggested_word[-1:]=='e':
                new_fixed_word=first_suggested_word+'r'
            else:
                new_fixed_word=first_suggested_word+'er'
            new_fixed_word = Word(new_fixed_word).spellcheck()
            qualified_suggested_word_list=new_fixed_word
    
    #Rule 2: Switch to 'than' if the first choice is 'then' but the previous corrected word is JJN (like stronger, happier..etc)
    if first_suggested_word == 'then':
        index=is_in_the_list(qualified_suggested_word_list, 'than', nth=0)
        w_left, w_right = get_word_to_left_and_right(sps, position_on_sps)
        left_is_adjective_kind = (w_left and map_word_tag_to(get_word_tag_str(w_left[0]))==WORD_TYPE().ADJ)
        right_is_adjective_or_noun_kind = (w_right and (map_word_tag_to(get_word_tag_str(w_right[0]))==WORD_TYPE().NOUN or map_word_tag_to(get_word_tag_str(w_right[0]))==WORD_TYPE().ADJ))
        if index and (left_is_adjective_kind or right_is_adjective_or_noun_kind):
            qualified_suggested_word_list=[qualified_suggested_word_list[index]]
        
    return qualified_suggested_word_list

class SentenceCorrector(Loggable):
    
    _sentence_str = ''
    _sentence=None
    _reader=None
    
    def __init__(self, sentence_str):
        self._sentence_str  = sentence_str
        self._sentence = TextBlob(sentence_str)
        self._reader=AIReader.Instance()
    
    def suggest(self):
        wds = words(self._sentence_str)
        i=0
        sps=self._sentence.pos_tags
        word_list_by_tag=build_word_list_by_tag(sps)
        suggested_words=list()
        suggested_new_sps=list(sps)
        for w in sps:
            ww=Word(str(w[0])).spellcheck()
            is_this_current_word_spell_correct = False
            if is_correct(ww,str(w[0])):  #If it is correct, try to find all similar words to it
                ww=get_similar_words_with_word_tags(str(w[0]), deep_level=1)   #so far go for level 1 deep for speed
                is_this_current_word_spell_correct=True
            w_left, w_right = get_word_to_left_and_right(sps, i)
            word_tags_list=list()
            if w_left:
                word_tags_list.append(self._reader.get_top_word_tag(w_left[1], 1, THE_NUM_OF_TOP_WORD_TAGS_TO_RETRIEVED))       #get the top two word_tags next to this word
            if w_right:
                word_tags_list.append(self._reader.get_top_word_tag(w_right[1], -1, THE_NUM_OF_TOP_WORD_TAGS_TO_RETRIEVED))     #get the top two word_tags before to this word
            word_tag_predictions=reduce_from_word_tags_list(word_tags_list)
            current_try_pos=0
            still_not_found=True
            qualified_suggested_word_list={}
            while(current_try_pos < len(word_tag_predictions)):
                for w_suggestion in ww: #loop through each word suggestion from the textblob 
                    this_suggested_word = str(w_suggestion[0])
                    this_word_tag_mapped_to = map_word_tag_to(get_word_tag_str(this_suggested_word))
                    if word_tag_predictions[current_try_pos] == this_word_tag_mapped_to:    #found a match!!!
                        score=score_this_suggested_word(w_suggestion, word_list_by_tag, str(w[0]),is_this_current_word_spell_correct)
                        qualified_suggested_word_list[this_suggested_word] = score
                        still_not_found=False
                current_try_pos+=1
            if still_not_found: #still not found (that might mean our database doesn't have a good answer yet, now trying the second time with less-restrictive conditions
                for w_suggestion in ww: #loop through each word suggestion from the textblob
                    score=score_this_suggested_word(w_suggestion, word_list_by_tag, str(w[0]), is_this_current_word_spell_correct)
                    qualified_suggested_word_list[str(w_suggestion[0])] = score
                    
            qualified_suggested_word_list=get_sorted_turple_on_dict_by_value(qualified_suggested_word_list, reverse_the_result=True)
            qualified_suggested_word_list=pick_the_mostly_grammar_correct_one(qualified_suggested_word_list, i, suggested_new_sps)
            if qualified_suggested_word_list and str(w[0]) !=qualified_suggested_word_list[0][0] and qualified_suggested_word_list[0][1]>0.0:
                suggested_words.append((str(w[0]), qualified_suggested_word_list[0][0]))     #pick the top one
                suggested_new_sps[i] = (qualified_suggested_word_list[0][0], get_word_tag_str(qualified_suggested_word_list[0][0]))
            i+=1
        
        suggested_sentence_str=self._sentence_str
        if suggested_words:
            for suggested_word in suggested_words:
                suggested_sentence_str = suggested_sentence_str.replace(suggested_word[0], suggested_word[1])
        return suggested_sentence_str