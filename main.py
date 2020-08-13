class ClientList(object):
    cl_list = []

    def __init__(self):
       pass

    def ReadFromFile(self):
        f = open('clients.txt','rt')
        for line in f:
            if len(line) > 0:
                self.cl_list.append(line[0:len(line)-1].lower())
        f.close()

    def PrintAll(self):
        for a in self.cl_list:
            print(a)

    def FindByName(self, search_str:str) -> str:

        res:str = ""

        if (search_str == ""):
            return res

        for a in self.cl_list:
            pos = a.find(search_str.lower())
            if pos >= 0:
                res = a
                break
        return res         


class OneWork(object):
    client:str  = ""
    category:str = ""
    current_status:str = ""
    description:str = ""

    def PrintStatus(self):
        print("Client %s, status is %s, started at %s, descr='%s'\n" % (self.client, self.current_status, self.begin_at.strftime("%H:%M"), self.description))
        """ вывести длительность """

    def SaveAllInformation(self, out_file):
        out_file.write("#Начало:" + self.begin_at.strftime("%H:%M") + "\n")
        if self.stop_at != 0:
            out_file.write("#Конец:" + self.stop_at.strftime("%H:%M") + "\n")
        out_file.write("#Контрагент:" + self.client + "\n")
        out_file.write("#Категория:" + self.category + "\n")
        out_file.write("#Описание:" + self.description + "\n\n")
    
class ListOfWork(object):
    spisok = []

    def SaveToFile(self):
        pass

    def PrintStatuses(self):
        ind = 0
        for a in self.spisok:
            ind += 1
            if a.current_status == "stopped":
                continue
            print("work № %i" % ind)
            a.PrintStatus()
            

    def AddToSpisok(self, one_struct):
        self.spisok.append(one_struct)

    def PrintSpisok(self):
        for a in self.spisok:
            a.PrintAllInformation()

    def SaveSpisok(self, out_file):
        for a in self.spisok:
            a.SaveAllInformation(out_file)
    
    def ReadTempFile(self, tmp_filename):
        tmp_out = open(tmp_filename, 'rb')
        self.spisok = pickle.load(tmp_out)
        tmp_out.close()
    
    def SaveTempFile(self, tmp_filename):
        tmp_out = open(tmp_filename, 'wb')
        pickle.dump(self.spisok, tmp_out)
        tmp_out.close()


"""
Main program begins
"""

import argparse
import datetime
import os.path
import pickle
import sys

parser = argparse.ArgumentParser()
parser.add_argument("command", default="status", choices=['start','stop','pause','resume','status','finish', 'client-list'], help="Выполняемое действие")
parser.add_argument("-c", default="", required=False, help="Название контрагента для режима start")
parser.add_argument("-d", default="<пустое описание>", required=False, help = "Описание")
parser.add_argument("-cat", default="Программирование", required=False, help="Категория")
args = parser.parse_args()

cl = ClientList()
cl.ReadFromFile()

command = args.command
founded_client = ""
if (command == "start") :
    founded_client = cl.FindByName(args.c)
    if len(founded_client) == 0 :
        print("Не смогли определить клиента '" + args.c + "' по списку из файла")
    else :
        print("Нашли " + founded_client)

   
now = datetime.datetime.now()
short_date = now.strftime("%Y-%m-%d")

tmp_filename = "homework_" + short_date + ".tmp"

it_is_new_file = False
if os.path.isfile(tmp_filename) == False:
    it_is_new_file = True

lw = ListOfWork()

if it_is_new_file == False:
    lw.ReadTempFile(tmp_filename)

if command == "start":

    for a in lw.spisok:
        if a.current_status == "started":
            a.current_status = "paused"
            a.stop_at = now

    a = OneWork()
    a.client = founded_client
    a.category = args.cat
    a.description = args.d
    a.current_status = "started"
    a.begin_at = now
    a.stop_at = 0

    lw.AddToSpisok(a)
    lw.SaveTempFile(tmp_filename)

if command == "stop":

    if len(lw.spisok) == 0:
        print("Nothing to stop")
        sys.exit(1)

    if len(lw.spisok) == 1:
        for a in lw.spisok:
            if a.stop_at == 0:
                a.stop_at = now
                a.current_status = "stopped"
    else:
        lw.PrintStatuses()
        answer = int(input("Enter number:"))

        ind = 1
        for a in lw.spisok:
            if ind == answer:
                if a.stop_at == 0:
                    a.stop_at = now
                    a.current_status = "stopped"
                break
            ind += 1
    
    lw.SaveTempFile(tmp_filename)

if command == "finish":
    filename = "homework_" + short_date + ".txt"
    if os.path.isfile(filename) == False:
        it_is_new_file = True

    out = open(filename, 'at', newline="\r\n")
    if it_is_new_file:
        out.write("#Дата:" + now.strftime("%d.%m.%Y") + "\n\n")

    for a in lw.spisok:
        if a.stop_at == 0:
            a.stop_at = now
            a.current_status = "stopped"

    lw.SaveSpisok(out)
    out.close()

    if os.path.exists(tmp_filename):
        os.remove(tmp_filename)

if command == "pause":
    if len(lw.spisok) == 0:
        print("Nothing to pause")
        sys.exit(1)
    
    for a in lw.spisok:
        if a.current_status == "started": 
            a.stop_at = now
            a.current_status = "paused"
    
    lw.SaveTempFile(tmp_filename)

if command == "resume":
    if len(lw.spisok) == 0:
        print("Nothing to resume")
        sys.exit(1)
    
    founded_paused_work = False
    for a in lw.spisok:
        if a.current_status == "paused": 
            """ добавим новую работу в конец, а эту переведем в статус stopped """
            founded_paused_work = True

            break

    if founded_paused_work == False:
        print("Nothing to resume")
        sys.exit(1)

if command == "status":
    lw.PrintStatuses()

if command == "client-list":
    cl.PrintAll()