import matplotlib
import csv as csv
import mysql.connector as mysql


class Csvtomysqldb():
    def __init__(self):
        self.db = mysql.connect(host="localhost",
                                port=3306,
                                user="root",
                                passwd="6Zr7>z!giEdw"
                      )
        self.cursor = self.db.cursor()

    def csv_loader_train(self):
        csv_data = csv.reader(file('data/train.csv'))
        next(csv_data, None)
        self.cursor.execute('use titanic;')
        self.cursor.execute('TRUNCATE `titanic`.`train`;')
        for row in csv_data:

            for i in range(0,11):
                if row[i] == '':
                    row[i] = 'NULL'

            query = '''INSERT INTO train(
                                    passenger_id,
                                    survived,
                                    pclass,
                                    name,
                                    sex,
                                    age,
                                    sibsp,
                                    parch,
                                    ticket,
                                    fare,
                                    cabin,
                                    embarked)
                                    VALUES({id},
                                            {survived},
                                            {pclass},
                                            '{name}',
                                            "{sex}",
                                            {age},
                                            {sibsp},
                                            {parch},
                                            "{ticket}",
                                            {fare},
                                            "{cabin}",
                                            "{embarked}");'''.format(id=row[0],
                                                                    survived=row[1],
                                                                    pclass=row[2],
                                                                    name=str(self.db.escape_string(row[3])),
                                                                    sex=row[4],
                                                                    age=row[5],
                                                                    sibsp=row[6],
                                                                    parch=row[7],
                                                                    ticket=row[8],
                                                                    fare=row[9],
                                                                    cabin=row[10],
                                                                    embarked=row[11])
            self.cursor.execute(query)
            self.db.commit()

    def csv_loader_test(self):
        csv_data = csv.reader(file('data/test.csv'))
        next(csv_data, None)
        self.cursor.execute('use titanic;')
        self.cursor.execute('TRUNCATE `titanic`.`test`;')
        for row in csv_data:

            for i in range(0,10):
                if row[i] == '':
                    row[i] = 'NULL'

            query = '''INSERT INTO test(
                                    passenger_id,
                                    pclass,
                                    name,
                                    sex,
                                    age,
                                    sibsp,
                                    parch,
                                    ticket,
                                    fare,
                                    cabin,
                                    embarked)
                                    VALUES({id},
                                            {pclass},
                                            '{name}',
                                            "{sex}",
                                            {age},
                                            {sibsp},
                                            {parch},
                                            "{ticket}",
                                            {fare},
                                            "{cabin}",
                                            "{embarked}");'''.format(id=row[0],
                                                                    pclass=row[1],
                                                                    name=str(self.db.escape_string(row[2])),
                                                                    sex=row[3],
                                                                    age=row[4],
                                                                    sibsp=row[5],
                                                                    parch=row[6],
                                                                    ticket=row[7],
                                                                    fare=row[8],
                                                                    cabin=row[9],
                                                                    embarked=row[10])
            self.cursor.execute(query)
            self.db.commit()


    def csv_loader_genderclassmodel(self):
        csv_data = csv.reader(file('data/genderclassmodel.csv'))
        next(csv_data, None)
        self.cursor.execute('use titanic;')
        self.cursor.execute('TRUNCATE `titanic`.`genderclassmodel`;')
        for row in csv_data:

            query = '''INSERT INTO genderclassmodel(
                                    passenger_id,
                                    survived)
                                    VALUES({id},
                                            {survived}
                                            );'''.format(id=row[0],
                                                        survived=row[1])
            self.cursor.execute(query)
            self.db.commit()



    def csv_loader_gendermodel(self):
        csv_data = csv.reader(file('data/gendermodel.csv'))
        next(csv_data, None)
        self.cursor.execute('use titanic;')
        self.cursor.execute('TRUNCATE `titanic`.`gendermodel`;')
        for row in csv_data:

            query = '''INSERT INTO gendermodel(
                                    passenger_id,
                                    survived)
                                    VALUES({id},
                                            {survived}
                                            );'''.format(id=row[0],
                                                        survived=row[1])
            self.cursor.execute(query)
            self.db.commit()



if __name__== '__main__':
    a=Csvtomysqldb()
    a.csv_loader_train()
    a.csv_loader_test()
    a.csv_loader_genderclassmodel()
    a.csv_loader_gendermodel()
    a.cursor.close()


