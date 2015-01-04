#!/usr/bin/python 
# Copyright (c) 2014-2015 Ken Wu
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
import operator
import logging
import os
import shutil
import json
import Stemmer
import string
import random
import sys
from time import gmtime, strftime
from os import listdir
from os.path import abspath, join, dirname, isfile

def get_logger(name):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(name+"--")
    return logger

def copy_dictionary(d):
    dd = {}
    for k, v in d.items():
        dd[k]=v
    return dd

def is_string(x):
    return isinstance(x, basestring)

##Algorithms part ####################################
def get_categories_with_n_highest_score(categories_org, n=1):
    log.debug("Getting categories: %s with %s highest score..." % (categories_org,n)) 
    categories=copy_dictionary(categories_org)
    indcies=list()
    for i in range(0, n):
        if not categories:
            break
        k, value = max(categories.iteritems(), key=operator.itemgetter(1))
        indcies.append((k,value))   #append both the key and value
        del categories[k]
    return indcies

def generate_token(len):
    datetimestr=get_datetime()
    #pydevd.settrace()
    token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(len))
    return datetimestr+'_'+token

##Cookie related ########################################
def remove_non_valid_chars(line):
    if line:
        line = line.replace('\n', '')
    return line

##Date/time part ########################################
def get_datetime():
    return strftime("%Y%m%d%H%M%S", gmtime())

##DEBUG related #########################################
def debug():
    try:
        if not r'/usr/local/share/pysrc' in sys.path:
            sys.path.append(r'/usr/local/share/pysrc') #assuming this is the pydev installation path
        import pydevd
        pydevd.settrace()
    except: 
        pass

##File/io part ########################################
def get_base(p):
    return join(abspath(dirname('__file__')), p)

def del_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        log.info("Dir: %s removed!" % dir_path) 

def clear_dir(dir_path):
    del_dir(dir_path)
    os.mkdir(dir_path)       

def del_file(path):
    if os.path.exists(path):
        os.remove(path)
        log.info("File: %s removed!" % path)

def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        log.info("Dir: %s created!" % dir_path)

def is_path_exist(p):
    return os.path.exists(p)

def real_lines(file_path, is_critical=False):
    file = None
    try:
        file = open(file_path, 'r')
        lines = file.readlines()
        return lines
    except:
        errro_str='Failed reading the file: %s' % file_path
        if is_critical:
            log.error(errro_str)
        else:
            log.info(errro_str)
        return None
    finally:
        if file:
            file.close()
    
def read_contents_from_dir(dir_p):
    onlyfiles = [ f for f in listdir(dir_p) if isfile(join(dir_p,f)) ]
    contents = []
    for file in onlyfiles:
        lines_list=real_lines(dir_p+'/'+file)
        lines=reduce(lambda x,y: x+y,lines_list)
        contents.append(lines)
    return contents
        
##Json part ########################################   
def get_json_value(json_str, field_name):
    decoded = json.loads(json_str)
    return decoded[field_name]

def dumps(data):
    return json.dumps(data)
        
##Natural language processing part ########################################   
stemmer = Stemmer.Stemmer('english')

def stem_all_words(word_list):
    stemmed_words = list()
    for word in word_list:
        stemmed_words.append(stemmer.stemWord(word))
    return stemmed_words

def stem_word(word):
    return stemmer.stemWord(word)
        
##Torando package util methods ############################################
def get_httpfile(httpfile, field):
    value_str = httpfile[field]
    #if field == 'body':
    #    if value_str[0:5] == 'str: ':   #torando tends to prepend 'str: ' to the uploaded content, so i stripped it out
    #        value_str = value_str[5:]
    return value_str
## String processing part #################################################
def convert_to_str(s):
    return str(s)

def rindex(str, s):
    try:
        return str[str.rindex(s)+1:].strip()
    except:
        return str       

def extract_head_tail(str, n=10, max_intact=50):
    if len(str) < max_intact or n > len(str)/2:
        return str
    else:
        return str[0:n]+'..........'+str[len(str)-n:len(str)]

def unescape(s):
    s = convert_to_str(s)
    s = s.replace("%20", " ")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

##Reports related #############################################

#It is converting the datatable's draw to the offset which is suitable to the sql palace
def convert_draw_to_offset(draw, length):
    if is_string(draw):
        draw=int(draw)
    if is_string(length):
        length=int(length)
    return (draw) * length

def convert_to_offset_to_draw(offset, length):
    if is_string(offset):
        offset=int(offset)
    if is_string(length):
        length=int(length)
    return (offset / length) + 1

##SQL util stuffs #############################################
#cols must be a type of list
def columnize_in_sql_way(cols):
    if cols:
        if is_string(cols):
            return cols
        else:
            return reduce(lambda x,y: str(x)+','+str(y), cols)
    else:
        return '*'

def build_ordered_by_sql_clause(ordered_column, ordered_direction):
    sql_ordered_by_str=''
    if ordered_column:
        sql_ordered_by_str='ORDER BY ' + ordered_column
        if ordered_direction:
            sql_ordered_by_str+= ' ' + ordered_direction
    return sql_ordered_by_str

log = get_logger("Utils") 
