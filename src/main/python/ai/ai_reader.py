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

from lib.utils import enum, switch
from lib.singleton import Singleton
from ai.ai_base import AIBase, _get_top,AI_DB_Constants

_WORD_TYPE = enum(NOUN='N', VERB='V', ADJ='J', UN_MAPPED='*')

def WORD_TYPE():
    return _WORD_TYPE

def WORD_TYPE_LIST():
    return (_WORD_TYPE.NOUN, _WORD_TYPE.VERB, _WORD_TYPE.ADJ)

#word_tag can be either VBN or NN or VBD
def map_word_tag_to(word_tag):
    wt= word_tag[0:1]
    for case in switch(wt):
        if case(_WORD_TYPE.NOUN):
            return _WORD_TYPE.NOUN
        if case(_WORD_TYPE.VERB):
            return _WORD_TYPE.VERB
        if case(_WORD_TYPE.ADJ):
            return _WORD_TYPE.ADJ
        if case():
            return _WORD_TYPE.UN_MAPPED

@Singleton
class AIReader(AIBase):

    #This should be the entry point of getting the most similar words for a given word, w
    def get_top_noun_similarity(self, noun_x, level=1, word_type=_WORD_TYPE.NOUN):
        noun_x=noun_x.lower()
        r = self.get_noun_similarity(noun_x)
        if r:
            r = self.get_top_n_n_similarity(r, level=level, word_type=word_type)
        return r
    
    def get_noun_similarity(self, n, level=1):
        return self._none_if_empty_else_doc(self._db.get_from_noun_noun(n))
        
    def get_word_tag(self, w):
        r = self._db.get_from_word_tag(w)
        return self._none_if_empty_else_doc(r) 
    
    def get_top_n_n_similarity(self, m, level, word_type):
        return _get_top(AI_DB_Constants.field_noun_ys_map, m, word_type, level)

    def get_top_word_tag(self, word_tag, nth,level):
        m=self.get_word_tag(word_tag)
        return _get_top(AI_DB_Constants.field_word_tag_map, m, nth, level)
    
    def _none_if_empty_else_doc(self, o, oo=None):
        if oo:
            return o['doc'][oo] if o else None
        else:
            return o['doc'] if o else None
    