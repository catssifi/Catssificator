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
import collections
from lib.utils import debug, real_lines,get_file_name_from_path,get_line_and_md5_from_file, words,get_datetime, sentences
from lib.singleton import Singleton
from lib.loggable import Loggable 
from ai.ai_base import AIBase,AI_DB_Constants
from ai.ai_reader import AIReader,map_word_tag_to

# return true if the word is worth being added to the similarity pool
non_interesting_word_tags=set()
non_interesting_word_tags.add('VBZ')
non_interesting_word_tags.add('IN') 
def is_interesting_word_tag(wt):
    if wt in non_interesting_word_tags:
        return False
    if wt[0:1]=='N' or wt[0:1]=='V' or wt[0:2]=='JJ':
        return True

def filter_out_only_the_interesting_words_by_tag(sentence):
    tags=sentence.pos_tags
    pos=0
    new_interesting_words=list()
    for t in tags:
        if is_interesting_word_tag(t[1]):
            new_interesting_words.append((str(t[0]).lower(), str(t[1]), pos))
        pos+=1
    return new_interesting_words



        
#This function calculates the distance score based on how far the this_pos is from the target_pos
#It returns a value x between 0 < x < 1 where the greater the value the closer it is and the lesser the value the further it is
_POS_SCALE=1.0
def get_distance_score(this_pos, target_pos):
    v = _POS_SCALE / float(abs(target_pos-this_pos))
    return v

@Singleton
class AIBuilder(AIBase):
    
    _reader = None
    
    def __init__(self):
        self._reader = AIReader.Instance()
        #self._db = 
    
    #This is danergous! it should be called with very caution
    def reset_whole_database(self):
        self._db.earse_db()
        self._db.init_database()
    
    def add_noun_noun_simarility(self, noun_list):
        noun_x=None
        noun_x_pos=None
        with self._lock_noun_noun_simarility:
            for noun_x_with_pos in noun_list:        # noun_x_with_pos will be of format (word, abs. pos)
                noun_x=noun_x_with_pos[0]
                noun_x_pos=noun_x_with_pos[2]
                doc = self._reader.get_noun_similarity(noun_x)
                noun_ys = filter(lambda x: x[0]!=noun_x, noun_list)
                noun_ys = map(lambda x: (x[0], x[1], get_distance_score(x[2], noun_x_pos)), noun_ys)
                nn=None
                if doc:
                    doc[AI_DB_Constants.field_noun_ys_map] = self._build_noun_nouns_structure(doc[AI_DB_Constants.field_noun_ys_map],
                                                                    noun_ys)
                    self._db.update(doc)
                else:
                    nys = self._build_noun_nouns_structure(None, noun_ys)
                    doc = dict(noun_x=noun_x, noun_ys=nys)
                    self._db.add_to_noun_noun_map(doc)
    
    def _ensure_position_starts_at_zero(self, tag_list):
        if tag_list[0][0] > 0:
            s=tag_list[0][0]
            tag_list = map(lambda x: (x[0]-s,x[1]), tag_list)
        return tag_list
    
    #tag_list is of format, e.g. [(0, 'NN'), (1, 'VBZ'), (2, 'DT'), (3, 'NN')], where the number x is the position
    def add_word_tag(self, tag_list):
        tag_list=self._ensure_position_starts_at_zero(tag_list)
        with self._lock_word:
            for word_tag_with_position in tag_list:
                position = word_tag_with_position[0]
                word_tag = word_tag_with_position[1]
                doc = self._reader.get_word_tag(word_tag)
                position_list = map(lambda x: (x[0]-position,x[1]), filter(lambda x: x[0]!=position, tag_list)) #translate the abs. postion to relative positon 
                wp=None
                if doc:
                    doc[AI_DB_Constants.field_word_tag_map] = self._build_word_tag_map(doc[AI_DB_Constants.field_word_tag_map], position_list)
                    self._db.update(doc)
                else:
                    wp = self._build_word_tag_map(None, position_list)
                    doc = dict(word_tag=word_tag, word_tag_map=wp)
                    self._db.add_to_word_tag_map(doc)
    
    #position_list: [(1, 'VBZ'), (2, 'DT'), (3, 'NN')], 
    # meaning to add a record with the next word is 'VBZ', the second next word is 'DT' ...etc to the current word, word        
    def _build_word_tag_map(self, existing_word_tag_map, position_list):
        if existing_word_tag_map:
            for p in position_list:
                if p[0] in existing_word_tag_map:
                    pp = existing_word_tag_map[p[0]]
                    if p[1] in pp:
                        pp[p[1]] = pp[p[1]] + 1
                    else:
                        pp[p[1]] = 1
                else:
                    existing_word_tag_map[p[0]] = { p[1]: 1 }
            return existing_word_tag_map
        else:
            d={}
            for p in position_list:
                d[p[0]] = { p[1]: 1 }
            return d
    
    def _build_noun_nouns_structure(self, existing_n_n_structure, noun_ys):
        noun_ys = noun_ys if isinstance(noun_ys, (list)) else [noun_ys] #make sure noun_ys is a list
        d={}
        if existing_n_n_structure:
            d=existing_n_n_structure
        for noun_y in noun_ys:
            t = map_word_tag_to(noun_y[1])
            if t in d:
                if noun_y[0] in d[t]: 
                    d[t][noun_y[0]] = noun_y[2] + d[t][noun_y[0]]
                else:
                    d[t][noun_y[0]] = noun_y[2]
            else:
                d[t] = {}
                d[t][noun_y[0]] = noun_y[2]
        return d
        
    def _create_tag_list(self, pos_tags):
        tag_list = list()
        for i in range(0, len(pos_tags)):
            tag_list.append((i, str(pos_tags[i][1]))) #also convert the unicode strings to string 
        return tag_list
    
    def process_message(self, msg_str):
        ss = sentences(msg_str)
        self._process_sentences(ss)
    
    def _process_sentences(self, sentences):
        for sentence in sentences:            
            tag_list = self._create_tag_list(sentence.pos_tags)
            self.add_word_tag(tag_list)
            
            interesting_word_turple_list = filter_out_only_the_interesting_words_by_tag(sentence)     #get all the noun* sequences
            self.add_noun_noun_simarility(interesting_word_turple_list )    #add the noun to noun similarity statistics
    
    #This method is to process the file and stores all stats into the nosql database
    def add_build_from_file(self, file_path):
        file_name=get_file_name_from_path(file_path)
        (all_contents_in_one_line,md5_str) = get_line_and_md5_from_file(file_path)
        db = self._db
        if not db.get_from_processed_file(md5_str):
            #model = self._build_words_count(words(all_contents_in_one_line))
            #inserted = self._db.insert_or_replace_words_count(model)
            doc={}
            doc[AI_DB_Constants.field_md5]=md5_str
            doc[AI_DB_Constants.field_file_path]=file_name
            doc[AI_DB_Constants.field_processed_date]=get_datetime()
            self.process_message(all_contents_in_one_line)
            return db.add_to_processed_path(doc)
        else:
            self.warn('file: %s has been processed...' %(file_path))
            return None
    
    def get_db(self):
        return self._db
    
    '''
    
    def _build_words_count(self, line):
        model = collections.defaultdict(lambda: 1)
        for f in line:
            model[f] += 1
        return model
    
    
    def load_words_counts_model(self):
        d={}
        results = self._db.select_words_counts()
        if results:
            for item in results: 
                d[item[0]]=item[1]
        self._words_counts_model = d
        return d
    '''