####Words stemming

In order to unify the search query for more accurate results, the system is capable of stemming a given word to its stemmed form.  For example, the word "played" will be stemmed to "play", "categories" will be to "categori".   Therefore, say, you have assigned a query "monitor repairment" to a category:Hardware, then later if you issue an inquiry, say, "repaired my macbook", you will get an answer category:Hardware as the system sees that the word "repaired" is equivalent to "repairment" in which they are stemmed to "repair".

<pre>
ken@ken-machine-mbp:~/Catssificator$ <b>./query.sh "repaired my macbookpro"</b>
Unfortunately, no category was found under the search query:repaired my macbookpro ...Please pick a category it should belong to:
1    Advertising                   2    Agriculture                   3    Art
4    Automotive                    5    Banking                       6    Berverages
...
...
...
<b>press control-c to exit</b>
ken@ken-machine-mbp:~/Catssificator$ <b>./query.sh "monitor repairment" "Hardware"</b>
ken@ken-machine-mbp:~/Catssificator$ <b>./query.sh "repaired my macbookpro"</b>
Hardware
</pre>