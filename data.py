
import os
 
START_DATE = "2022-09-01"
END_DATE = "2023-07-31"


db_name = "news_data"
dir_path = (
    os.path.dirname(os.path.realpath(__file__))
    + "/data/"
    + START_DATE
    + "_"
    + END_DATE
    + "/"
)

db_path = dir_path+db_name+'.db'