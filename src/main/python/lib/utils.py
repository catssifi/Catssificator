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
from datetime import datetime
from pytz import timezone
import pytz
from time import gmtime, strftime
import time
from os import listdir
from os.path import abspath, join, dirname, isfile
from collections import Counter

os.environ['TZ'] = 'UTC'
STOP_WORDS=[u'&', u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
STOP_WORDS_DICT = Counter(STOP_WORDS)

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
def does_list_a_all_exist_in_list_b(a, b, f):
    for x in a:
        this_x_founded_in_b=False
        for y in b:
            if f(x,y):
                this_x_founded_in_b=True
        if not this_x_founded_in_b:
            return False
    return True

def convert_list_to_dict(l):
    return Counter(l)   #converts to dictionary

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

def map_keys_to_the_values(values_without_key, keys):
    new_key_value_list=list()
    #keys=map(lambda x: x.replace('\'', '"'), keys)
    for value in values_without_key:
        new_tuple=list()
        i=0
        obj = {}
        for item in value:
            obj[keys[i]] = item if is_string(item) else str(item)
            i+=1
        new_key_value_list.append(obj)
    return new_key_value_list

##Cookie related ########################################
def remove_non_valid_chars(line):
    if line:
        line = line.replace('\n', '')
    return line

##Date/time part ########################################
def get_datetime():
    return strftime("%Y%m%d%H%M%S", gmtime())
def convert_date_to_s(d, format='%Y%m%d'):
    return d.strftime(format)
def convert_datetime_to_s(d, format='%Y-%m-%d %H:%M:%S'):
    return d.strftime(format)
def convert_s_to_date(s, format='%Y%m%d'):
    return datetime.strptime(s, format)

def convert_UTC_time_zone_to_Local_time_zone(utc_time, local_time_zone):
    return datetime.fromtimestamp( time.mktime(datetime.strptime(
                                    utc_time, "%Y-%m-%d %H:%M:%S").timetuple()) , pytz.timezone(local_time_zone))

#local_time_zone can be 'America/New_York'
def convert_UTC_time_zones_to_Local_time_zones_in_bulk(map_results, time_col_name, local_time_zone='UTC'):
    if map_results:
        for m in map_results:
            utc_time = m[time_col_name]
            local_time = convert_UTC_time_zone_to_Local_time_zone(utc_time, local_time_zone)
            m[time_col_name] = str(local_time) + ' ' + local_time_zone
            
    return map_results

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

def get_all_stop_words():
    return STOP_WORDS_DICT

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

def extract_head_tail(str, n=50, max_intact=150):
    if len(str) < max_intact or n > len(str)/2:
        return str
    else:
        return str[0:n]+'..........'+str[len(str)-n:len(str)]

def extract_head_tail_in_bulk(map_results, category_index):
    if map_results:
        for m in map_results:
            m[category_index] = extract_head_tail(m[category_index]) 
    return map_results

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
    if draw > 1 and length > 10:    #some bugs in the datalength script..so i have to hardcore it
        draw=draw-1
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
