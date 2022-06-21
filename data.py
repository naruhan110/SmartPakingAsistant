import mysql.connector
from datetime import datetime

def creat_database():
   connection = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='nhan1691999',
      port='3306',
   )
   cursor=connection.cursor()
   cursor.execute("create database if not exists parking")
   return


def create_table(name=datetime.now().strftime("%d_%m_%Y")):
   connection = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='nhan1691999',
      port='3306',
      database='parking',
   )
   cursor = connection.cursor()
   # create table for each day date

   create_table = """create table if not exists data_"""+name+"""
            (
               `id` int NOT NULL AUTO_INCREMENT,
              `ticket` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8_unicode_ci NOT NULL,
              `lisence_plate` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8_unicode_ci NOT NULL,
              `time_come` time,
              `time_left` time,
              UNIQUE KEY `id_UNIQUE` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci"""
   cursor.execute(create_table)
   return

def insert_data(table, ticket, lisence, time_come):
   connection = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='nhan1691999',
      port='3306',
      database='parking',
   )
   cursor = connection.cursor()
   sql = "insert into {table} (ticket, lisence_plate, time_come) values (%s, %s, %s)".format(table=table)
   val = (ticket, lisence, time_come)
   cursor.execute(sql, val)
   connection.commit()
   print(cursor.rowcount, "data inserted")
   connection.close()
   return


def update_time_left(table, ticket, lisence, time_left):
   connection = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='nhan1691999',
      port='3306',
      database='parking',
   )
   cursor = connection.cursor()
   statement = "update {table} set time_left = {time_left} where ticket = {ticket} and lisence_plate = {lisence} and time_left is null".format(table=table, time_left=time_left, ticket=ticket, lisence=lisence)
   cursor.execute(statement)
   remain = cursor.fetchall()
   print(statement)
   connection.commit()
   connection.close()
   return


def searching(lisence, date=datetime.now().strftime("%d_%m_%Y")):
   connection = mysql.connector.connect(
      host='127.0.0.1',
      user='root',
      password='nhan1691999',
      port='3306',
      database='parking',
   )
   cursor = connection.cursor()

   statement = f"select * from data_{date} where lisence_plate = {lisence}"
   cursor.execute(statement)
   result = cursor.fetchall()
   return result

now = datetime.now()

date = now.strftime("%d_%m_%Y")

time = now.strftime("%H%M%S")

#creat_database()
create_table()
"""insert_data("data_"+date, '123', '213213', '222222')
update_time_left("data_"+date, '123', '213213', '232323')
"""
