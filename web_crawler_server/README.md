# PGA-Ebola-Project
0.database creation before scraping(first time only):      
run SQL command "CREATE TABLE web_crawler_tb (title VARCHAR(255), date DATE,link TEXT);"

1.install neccessary package:  
install python 2.x      
pip install pymysql

2.in main.py, modify following variables:      
path(to save scraped news content), 
database (as log) related hostname, database_name, username and password

3.run command "python main"
