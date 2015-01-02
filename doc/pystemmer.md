#####Step 1: Download the PyStemmer at https://pypi.python.org/pypi/PyStemmer

<pre>
$ wget https://pypi.python.org/packages/source/P/PyStemmer/PyStemmer-1.3.0.tar.gz
</pre>

#####Step 2: Unzip it and cd into the unzipped directory

<pre>
$ <b>tar xvf PyStemmer-1.3.0.tar.gz</b>
x PyStemmer-1.3.0/libstemmer_c/src_c/stem_UTF_8_spanish.c
x PyStemmer-1.3.0/libstemmer_c/src_c/stem_ISO_8859_1_english.h
x PyStemmer-1.3.0/libstemmer_c/src_c/stem_UTF_8_finnish.c
x PyStemmer-1.3.0/libstemmer_c/src_c/stem_ISO_8859_1_italian.h
x PyStemmer-1.3.0/libstemmer_c/examples/
x PyStemmer-1.3.0/libstemmer_c/examples/stemwords.c
x PyStemmer-1.3.0/MANIFEST.in
x PyStemmer-1.3.0/benchmark.py
...
$ <b>cd PyStemmer-1.3.0</b>
</pre>

#####Step 3: Install PyStemmer

<pre>
~/PyStemmer-1.3.0$ <b>sudo python setup.py install</b>
</pre>

#####Step 4: Verify that PyStemmer has been installed sucessfully
<pre>
$ <b>python</b>
Python 2.7.6 (default, Sep  9 2014, 15:04:36)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> <b>import Stemmer</b>
>>> <b>print(Stemmer.algorithms())</b>
[u'danish', u'dutch', u'english', u'finnish', u'french', u'german', u'hungarian', u'italian', u'norwegian', u'porter', u'portuguese', u'romanian', u'russian', u'spanish', u'swedish', u'turkish']
>>>
</pre>

Then if u see all above, congrats! you have sucessfully installed PyStemmer and can continue with running Catssificator on your machine.