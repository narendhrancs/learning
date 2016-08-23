import matplotlib.pyplot as plt
import seaborn as sns
from sql_import import Csvtomysqldb as mysql
import numpy as np


# mysql = mysql()
# mysql.cursor.execute('use titanic;')
# mysql.cursor.execute("SELECT passenger_id,"
#                      "survived,"
#                      "pclass,"
#                      "age,"
#                      "sibsp,"
#                      "parch,"
#                      "fare "
#                      "FROM titanic.train;")
# data = np.asarray(mysql.cursor.fetchall())
# sns.corrplot(data)
# plt.show()



import mysql.connector as mysql
db = mysql.connect(host="localhost",
                                port=3306,
                                user="root",
                                passwd="6Zr7>z!giEdw"
                      )
cursor = db.cursor()
cursor.execute('use titanic;')
cursor.execute('select count(survived), survived from train group by survived, pclass;')
a=cursor.fetchall()
print a
