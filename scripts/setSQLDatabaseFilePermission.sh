# If it happens to have the following error, please execute this script to set the correct permision on the SQLite database file
#   File "/Users/ken/workspace/category-classificator/src/main/python/backend/database.py", line 220, in execute
#    c.execute(sql_statement)
#    OperationalError: attempt to write a readonly database
# refer to http://serverfault.com/questions/57596/why-do-i-get-sqlite-error-unable-to-open-database-file

sudo chmod 664 database.db