<img src="doc/category-classificator.png">
##About Category-Classificator (a.k.a. Catssificator)

#Offical release is coming soon .. Please stay tune!

This software implements an A.I. system with advanced machine learning techniques that reads any given input and determines what category(ies) it should belong to based on what it has learned previously.  In a novel way, it implements the Natural language processing on a machine-learning way.

####Dependencies
There are few dependencies that are needed to be installed/configured first in order to run the program:
<ol>
<li><b>Mac/Linux environments:</b> Currently, the out of the box configuration can be run on any Mac or linux machines.  For window machines, at least python and bash scripts are required.</li>
<li><b>Python 2.x</b>: It is fully tested in python 2.x environments.  For python 3.x, i am really not sure yet.</li>
<li><b>PyStemmer</b>: The system uses this library to do the word stemmings.  For example, if the input word is 'ate', it will be reduced to 'eat', the stemmed form of a word.  To install it, please refer to <a href=doc/pystemmer.md target=_blank>this documentation</a>.</li>
<li><b>Torando</b>:  We use Torando (in which Facebook, Quora, FriendFeed..etc have been using as their production web servers) for its scalable and non-blocking web server capabilities on our interactive web UI need.   To install it, please refer to <a href=doc/torando.md target=_blank>this documentation</a>.</li>
<li><b>PyYAML</b>: It is for parsing the internal configurations.  Please refer <a href="http://pyyaml.org/wiki/PyYAML">here</a> for download and <a href="http://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank">here</a> for installation.</li>
</ol>

###How to run
To start with, the system is configured with 20 pre-defined categories.  you can always change it at config/category.txt 

First run the A.I. server as (and let it run in the background and do not stop it):
<pre>
$ ./start_server.sh
</pre>

Then in another terminal, run an inquire query, say "Android cell phone latest price" as:
<pre>
$ <b>./query.sh "Android cell phone latest price"</b>
Unfortunately, no category was found under the search query:Android cell phone latest price ...Please pick a category it should belong to:
1    Advertising                   2    Agriculture                   3    Art
4    Automotive                    5    Banking                       6    Berverages
7    Business                      8    Economics                     9    Education
10   Fashion                       11   Hardware                      12   Mobile_Devices
13   Robotics                      14   Science                       15   Social_Media
16   Sports                        17   Technology                    18   Television
19   Travel                        20   Weather
Please enter a category number: <b>12</b>
THANKS.  It has been recorded.
$
</pre>
Notice that when you issue an inquiry to the system and, if the system does not have any previous knowledge about it, it will ask you what category it should belong to.  So in the above example, since it is the first time you ask the system about 'Android phone price', it has no previous knowledge about it and then it will prompt you for the category.  Therefore, replying as 12 (Mobile_Devices) and the system will remember this (internally it will be stored in the file system for future analysis).  Next time let say you inquire something related to Android or phone, it will be able to figure out it should belong to Mobile Devices category, as followed:

<pre>
$ ./query.sh "where to buy phone"
Mobile_Devices
</pre>

#####Advanced capabilities
There are also advanced capabilities, as of today, <a href="doc/usage.md#words-stemming" target=_blank>words stemming</a>, included in the system.  Please refer to the <a href="doc/usage.md" target=_blank>useage document</a> for more information.

####(Optional) Pre-populate some data into the system  
I have prepared also a script that populated some search queries with its pre-defined category.  Please run it to load it to the system so that it does not start from zero
<pre>
$ ./script/populate-knowledge.sh
</pre>

After that, if we ask something like, "drink tonight", it should automatically figure out it is a Berverages category
<pre>
$ ./query.sh "drink tonight"
Beverages
</pre>

###Testings - for developors only
#####Travis-ci build status:
This version of Catssificator has been tested using Python series 2.6 and 2.7. Builds are checked with <a href="https://travis-ci.org/wwken/category-classificator" target="_blank">travis</a>:<br/>
[![Build Status](https://travis-ci.org/wwken/category-classificator.svg)](https://travis-ci.org/wwken/category-classificator)
#####Run the unit-tests locally:
In the src/test/ folder, there are various test cases that make sure the program won't break easily.  To run all test cases, do:
<pre>
$ scripts/unit-tests/run-all-unit-tests.sh
</pre>
Notice that Nose (https://nose.readthedocs.org/en/latest/) , is needed in order to run the tests.  Please install it beforehand.


###Algorithms - How I appoarch it
I will describe it later


