'''
    Author:PWND0U
    Ver:1.0
'''
from tkinter import *
import tkinter.filedialog
import json
from random import randint, uniform
from tkinter import ttk
import requests
import base64
import os

def encrypt(number):
    key = "xfvdmyirsg"
    numbers = list(map(int, list(str(number))))
    return_key = "".join([key[i] for i in numbers])
    return return_key


def pretty_print(jsonStr):
    print(json.dumps(json.loads(jsonStr), indent=4, ensure_ascii=False))


class Aipaoer(object):
    def __init__(self, IMEICode):
        self.IMEICode = IMEICode
        self.userName = ""
        self.userId = ""
        self.schoolName = ""
        self.token = ""
        self.runId = ""
        self.distance = 2400
        self.minSpeed = 2.0
        self.maxSpeed = 3.0
        self.shixiao = False

    def __str__(self):
        return str(self.__dict__).replace("\'", "\"")

    def check_imeicode(self):
        IMEICode = self.IMEICode
        url = "http://client3.aipao.me/api/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode={IMEICode}".format(
            IMEICode=IMEICode)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                okJson = rsp.json()
                self.token = okJson["Data"]["Token"]
                self.userId = okJson["Data"]["UserId"]
        except KeyError:
            print("IMEICode 失效")

    def get_info(self):
        token = self.token
        url = "http://client3.aipao.me/api/{token}/QM_Users/GS".format(token=token)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                okJson = rsp.json()
                self.userName = okJson["Data"]["User"]["NickName"]
                self.schoolName = okJson["Data"]["SchoolRun"]["SchoolName"]
                self.minSpeed = okJson["Data"]["SchoolRun"]["MinSpeed"]
                self.maxSpeed = okJson["Data"]["SchoolRun"]["MaxSpeed"]
                self.distance = okJson["Data"]["SchoolRun"]["Lengths"]
        except KeyError:
            print("Unknown error in get_info")

    def get_runId(self):
        token = self.token
        distance = self.distance
        url = "http://client3.aipao.me/api/{token}/QM_Runs/SRS?S1=40.62828&S2=120.79108&S3={distance}" \
            .format(token=token, distance=distance)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                self.runId = rsp.json()["Data"]["RunId"]
        except KeyError:
            print("Unknown error in get_runId")

    def upload_record(self):
        my_speed = round(uniform(self.minSpeed + 0.3, self.maxSpeed - 0.5), 2)
        my_distance = self.distance + randint(1, 5)
        my_costTime = int(my_distance // my_speed)
        my_step = randint(1555, 2222)
        print(my_speed, my_distance, my_costTime, my_step)
        myParams = {
            "token": self.token,
            "runId": self.runId,
            "costTime": encrypt(my_costTime),
            "distance": encrypt(my_distance),
            "step": encrypt(my_step)}
        url = "http://client3.aipao.me/api/{token}/QM_Runs/ES?" \
              "S1={runId}&S4={costTime}&S5={distance}&S6=A0A2A1A3A0&S7=1&S8=xfvdmyirsg&S9={step}".format(**myParams)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                # Label(main_box, text=str(self.IMEICode+"：" + self.userName+"：" + "成功!")).grid(row=rowIndex, column=0, columnspan=3)
                value = ["成功!",self.userName]
                tree.insert("", "end", text=self.IMEICode, values=value)
                print(self.userName + ": 成功!")
        except KeyError:
            # Label(main_box, text=str(self.IMEICode + "：失败")).grid(row=rowIndex, column=0, columnspan=3)
            value = ["失败!", self.userName]
            tree.insert("", "end", text=self.IMEICode, values=value)
            with open("失败.txt", "a+") as f:
                f.write(self.IMEICode + "\n")
            print("失败")


def selectPath():
    path_ = tkinter.filedialog.askopenfilename()
    global path_all
    path_all = ""
    path_all = path_
    path.set(path_)


def printPath():
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    imeicodes = [IMCode.get().strip(" ")[:32]]
    IMEICodes = []
    if imeicodes[0] == '':
        imeicodes.pop()
        if path_all != "":
            with open(path_all, "rb") as fp:
                IMEICodes = fp.readlines()
                for IMEICode in IMEICodes:
                    IMEICode = IMEICode.decode("utf8")
                    imeicodes.append(IMEICode[:32])
            fp.close()
        else:
            print("请选择任意一种方式运行程序")
        print("读入 IMEICode完成，共 {}".format(len(IMEICodes)))
        print(imeicodes)
    if not imeicodes:
        return
    for IMEICode in imeicodes:
        if IMEICode[0] == "#":
            print("跳过：" + IMEICode)
            continue
        aipaoer = Aipaoer(IMEICode)
        aipaoer.check_imeicode()
        aipaoer.get_info()
        aipaoer.get_runId()
        aipaoer.upload_record()
        # pretty_print(str(aipaoer))
    # print(path_all)


def main():
    ico = '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'
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(ico))
    tmp.close()
    global main_box
    main_box = Tk()
    global win_table
    win_table = Tk()
    main_box.title('阳光长跑程序 By:信息安全实验室 作者:PWND0U')
    main_box.iconbitmap(default='tmp.ico')
    win_table.iconbitmap(default='tmp.ico')
    main_box.geometry('380x130')
    main_box.resizable(width=False, height=True)
    global path
    path = StringVar()
    global IMCode
    IMCode = StringVar()
    TextName = StringVar()
    Label(main_box, text="目标路径: ").grid(row=0, column=0)
    Entry(main_box, textvariable=path).grid(row=0, column = 1)
    Button(main_box, text="路径选择", command=selectPath).grid(row=0, column=2)
    Label(main_box, text="IMEICode: ").grid(row=1, column=0)
    Entry(main_box, textvariable=IMCode).grid(row=1, column=1)
    Label(main_box, text="单独给自己跑请填入\n批量选择txt文件").grid(row=1, column=2)
    Button(main_box, text="开始跑步", command=printPath).grid(row=2, column=1)
    Label(main_box, text="By:信息安全实验室 作者:PWND0U ").grid(row=3, column=0, columnspan=2)
    Label(main_box, text="1.0").grid(row=3, column=2)
    win_table.title("结果：失败请查看当前目录底下(失败.txt) By:信息安全实验室 作者:PWND0U")
    win_table.geometry("400x230") 
    win_table.resizable(width=False, height=False)
    '''
    表格
    '''
    global tree
    tree = ttk.Treeview(win_table)
    tree["columns"] = ("Status", "备注") 
    tree.column("Status", width=100)
    tree.column("备注", width=100)
    tree.heading("Status", text="Status")
    tree.heading("备注", text="备注")
    tree.pack()
    os.remove("tmp.ico")
    main_box.mainloop()


if __name__ == "__main__":
    main()
