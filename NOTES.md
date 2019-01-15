# Code Changes
Attempt to keep track of, mostly, major changes to the code fomr the book.

Due to the fact that both the internet, and various software, etc are constantly evolving, both minor and major changes to the given code were needed in order to get things working and deployed.

## Major
### in general  
######sql_conn:  
I have to use a different connector to MySQL. The book uses the package `MySQLdb`. In its place, I use `mysql.connector`.

### in ... retrieval

the url for downloading csvs from Yahoo! Finance has changed. Instead of direct construction of this URL, I've decided to employ a package for this.

The package is ...., and I used it in a previous script, when going through some examples by Sentdex (on YouTube).

Specifically this video ...

### in *insert_symbols.py*
[see here](/NOTES.md#sql_conn)

Personal modificaitons included ways to retry, and adding pausing/sleeping between requests.

## Minor
![MySQL icon](/z_other/MySQL_logo.png)
### in ..... for sql
The connector to the MySQL database had to be modified.
Specifically,

### MySQL database creation
a separate fle was made for the creation of each table in the sql database. In the book, these were held in one ddl file called <u>securities_master.sql</u>



[see here](/NOTES.md#sql_conn)