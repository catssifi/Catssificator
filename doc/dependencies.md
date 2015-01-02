####Dependencies
There are few dependencies should be installed automatically by the ./install.sh script:
<ol>
<li><b>PyStemmer</b>: The system uses this library to do the word stemmings.  For example, if the input word is 'ate', it will be reduced to 'eat', the stemmed form of a word.  If for some reason, the installation fails and If you wish to install it manually, please refer to <a href=doc/pystemmer.md target=_blank>this documentation</a>.</li>
<li><b>Torando</b>:  We use Torando (in which Facebook, Quora, FriendFeed..etc have been using as their production web servers) for its scalable and non-blocking web server capabilities on our interactive web UI need.   If for some reason, the installation fails and If you wish to install it manually, please refer to <a href=doc/torando.md target=_blank>this documentation</a>.</li>
<li><b>PyYAML</b>: It is for parsing the internal configurations.  If for some reason, the installation fails and If you wish to install it manually, please refer to<a href="http://pyyaml.org/wiki/PyYAML">here</a> for download and <a href="http://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank">here</a> for installation.</li>
</ol>