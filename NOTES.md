# Code Changes
Attempt to keep track of, mostly, major changes to the code fomr the book.

Due to the fact that both the internet, and various software, etc are constantly evolving, both minor and major changes to the given code were needed in order to get things working and deployed.

## Major
### in ... retrieval
the url for downloading csvs from Yahoo! Finance has changed. Instead of direct construction of this URL, I've decided to employ a package for this.

The package is ...., and I used it in a previous script, when going through some examples by Sentdex (on YouTube).

Specifically this video ...

Personal modificaitons included ways to retry, and adding pausing/sleeping between requests.

## Minor
![MySQL icon](https://media.licdn.com/dms/image/C4D0BAQFqVGAsoMsnNw/company-logo_200_200/0?e=1555545600&v=beta&t=gJsqIF24vS-zYYiHrnvvpuuaT1v03TfdF6n6xMsn-TY)
### in ..... for sql
The connector to the MySQL database had to be modified.
Specifically,

### .sql database creation
a separate fle was made for the creation of each table in the sql database. In the book, these were held in one ddl file called ...

