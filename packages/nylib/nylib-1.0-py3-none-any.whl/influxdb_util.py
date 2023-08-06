#! /usr/bin/env python
# -*- coding:utf-8 -*-

from influxdb import InfluxDBClient
import random


def getClient():
    client = InfluxDBClient("influxdb.navyran.top", 80, "", "", "mydb")  # 初始化
    return client



def showTables(client):
    result = client.query('show measurements;')  # 显示数据库中的表
    print("Result: {0}".format(result))


def test():
    client = InfluxDBClient("localhost", 8086, "", "", "")  # 初始化
    print(client.get_list_database())  # 显示所有数据库名称
    # client.create_database("testdb")  # 创建数据库
    # print(client.get_list_database())  # 显示所有数据库名称
    # client.drop_database("testdb")  # 删除数据库
    # print(client.get_list_database())  # 显示所有数据库名称


def insert(client):
    json_body = [
        {
            "measurement": "students",
            "tags": {
                "stuid": "s123"
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "score": random.randint(20,100)
            }
        }
    ]
    print(json_body)
    client.write_points(json_body)  # 写入数据，同时创建表


def dropTable(client, table):
    client.query("drop measurement " + table)  # 删除表


def query(client):
    # result = client.query('select * from students;')
    result = client.query('SELECT * FROM "stock" WHERE time >= 1541030294278ms;')
    print("Result: {0}".format(result))


def main():
    # test()
    client = getClient()
    # showDBNames(client)
    showTables(client)
    # insert(client)
    query(client)


if __name__ == '__main__':
    main()
