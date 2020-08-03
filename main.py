class ClientList(object):
    cl_list = []

    def __init__(self):
        """empty"""

    def ReadFromFile(self):
        f = open('clients.txt','rt')
        for line in f:
            if len(line) > 0:
                self.cl_list.append(line[0:len(line)-1].lower())
        f.close()

    def PrintAll(self):
        for a in self.cl_list:
            print(a)

    def FindByName(self, search_str):

        res = ""

        if (search_str == ""):
            return res

        for a in self.cl_list:
            pos = a.find(search_str.lower())
            if pos >= 0:
                res = a
                break
        return res         

"""
Main program begins
"""

cl = ClientList
ClientList.ReadFromFile(cl)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("command", default="status", choices=['start','stop','pause','resume','status'], help="Выполняемое действие")
parser.add_argument("-client", default="", required=False, help="Название контрагента для режима start и resume")
args = parser.parse_args()

command = args.command
if (command == "start") or (command == "старт") :
    founded_client = ClientList.FindByName(cl, args.client)
    if len(founded_client) == 0 :
        print("Не смогли определить клиента '" + args.client + "' по списку из файла")
    else :
        print("Нашли " + founded_client)

import datetime   
now = datetime.datetime.now()
str_time = now.strftime("%d-%m-%Y %H:%M") 
print(str_time)   
