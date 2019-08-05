import xlsxwriter
import numpy as np 
import sys
import os
from matplotlib import pyplot as plt 
def deal_product(devices_name):
    product = ""
    if len(devices_name.split())==2:
        productinfo=devices_name.split()[0]
        product=productinfo.split('-')[0]
    return product
def deal_verision(devices_name):
    verision = ""
    if len(devices_name.split())==2:
        verisioninfo=devices_name.split()[1]
        verision=verisioninfo.split('(')[0]
    return verision
def deal_product_version(devices_name):
    res=""
    if len(devices_name.split())==2:
        product_version=devices_name.split('\n')[0]
        str1=product_version.split()[0]
        str2=product_version.split()[1]
        res=str1+"_"+str2
    return res
def analyze_versionInfo(file_path):
    try:
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                devices_name = line
                line = f.readline()
    except FileNotFoundError:
        print(file_path + " has lost")
    return devices_name
def analyze_deviceInfo(file_path):    #获取机名的基础上加上版本号
    devSn = []
    count = 0
    try:
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                eachline = line.split()
                if len(eachline) == 1 and len(eachline[0]) == 16 :
                    devSn.insert(count, eachline[0])
                    count += 1
                line = f.readline()
    except FileNotFoundError:
        print(file_path + " has lost")
    return devSn
def deal_hprof(info):   #返回type
    line=info.split('/')
    type_size=line[5]
    type=type_size.split('_')[0]
    if type == 'system':
        type='system_server'
    return type
def analyze_hprofinfo(hprof_path):
    type_size = []
    try:
        with open(hprof_path, 'r') as f:
            line = f.readline()
            while line:
                eachline = line.split()    #六个元素
                type=deal_hprof(eachline[4])
                if type not in type_size:
                    type_size.append(type)   #存放在列表
                line=f.readline()
    except FileNotFoundError:
        print(hprof_path + " has lost")
    return type_size
def analyze_modulelist(file_path):
    mod_list = []
    count = 0
    try:
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:    
                eachline = line.split()       #默认以空格分割	
                if len(eachline) == 1 and count != 0:
                    mod_list.insert(count, eachline[0])  #一直往后插入，不适用count直接用inset可以么？
                count += 1
                line = f.readline()     
    except FileNotFoundError:
        print(file_path + " has lost")                
    return mod_list

def analyze_logfile(data_path): 
    x = []
    y = []
    
    count = 0
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                eachline = line.split() 
                #print(eachline)
                if len(eachline) == 6 and eachline[0] == "TOTAL:" :
                    try:                        
                        y.insert(count, int(eachline[1])/1024)
                        x.insert(count, count+1)
                        count += 1
                    except ValueError:
                        print("invalid digital " + eachline[1])
                line = f.readline()
    except FileNotFoundError:
        print(data_path + " has lost")
    return (x,y)

def draw_pic(x,y,title,lable_x,lable_y,pic_path):    
    plt.xlabel(lable_x) 
    plt.ylabel(lable_y)  
    max_val = int(max(y)+5)    
    min_val = 0 if min(y)<5  else int(min(y)-5)    
    sp = int((max_val-min_val)/5)
    plt.ylim((min_val,max_val))    #设置y轴范围
    my_y_ticks = np.arange(min_val, max_val, sp)   #sp是步长，(min_val-max_val是范围)
    plt.title(title) 
    plt.yticks(my_y_ticks)   
    plt.plot(x,y)   #画图
    plt.savefig(pic_path) 
    plt.close()
    
def parseBaseInfo(strFilePath):
    info = []
    if len(strFilePath)==0:
        return info
    
    basePath = strFilePath.split("\\")   
    if len(basePath) < 1 :
        print("bad arg1,usage: data_proc.py folderpath")
        return    
    logFolder = basePath[len(basePath)-1]
    
    if len(logFolder) == 0:
        print("bad arg2,usage: data_proc.py folderpath")
        return info
        
    infoFolder = logFolder.split("_")
    if len(infoFolder) != 3:
        print("bad arg3,usage: data_proc.py folderpath")
        return info
        
    info.insert(0, infoFolder[1])
    info.insert(1, infoFolder[2])
    return info
def deal_data(data):   #将数据处理后输出为一个excel
    list = []
    max_data=max(data)
    ave_data=sum(data)/len(data)
    speed_up=((data[-1]+data[-2]+data[-3]+data[-4]+data[-5]+data[-6])/6-(data[0]+data[1]+data[2]+data[3]+data[4]+data[5])/6)/(len(data)/6)
    list.append(max_data)
    list.append(ave_data)
    list.append(speed_up)
    return list
def parseSingleFolder(parPath, num, allNum):       #如果存在hprof文件然后将hprof文件里出问题的包名提取出来
    bInfo = parseBaseInfo(parPath)
    if len(bInfo) == 0:
        print("bad arg,usage: data_proc.py folderpath")
        return (num,allNum)
    #print(bInfo)
    
    devSerNo = analyze_deviceInfo(parPath+"\\devicesInfo.txt")
    #print(devSerNo)
    modlist = []
    modlist_all = analyze_modulelist(parPath+"\\module.ini")
    if os.path.exists(parPath+"\\hprof_record.txt"):
        modlist = analyze_hprofinfo(parPath+"\\hprof_record.txt")
    #print(modlist)
    versionInfo = analyze_versionInfo(parPath+"\\devicesInfo.txt")
    product_version = deal_product_version(versionInfo)
    pngSavePath = "..\\venv\\static\\images"   #有内存泄漏嫌疑的图
    allPngSavePath = "..\\venv\\static\\all"  #全部的图
    for dev in devSerNo:
        for mod in modlist:
            logFile = parPath+"\\"+mod+"\\"+dev+"_"+mod+".txt"
            if os.path.exists(logFile) == False:
                #print(logFile+" not exist")
                continue
            rslt = analyze_logfile(logFile)  #rslt是一个元组，两个元素是两个列表
            if len(rslt[0]) != 0:
                if max(rslt[1]) > 500:   #记录如果峰值>500
                    print("\033[1;35m phone:"+dev+" module:"+mod+" has data" + " maxvalue:" + str(max(rslt[1])) + "  file:" + logFile + "\033[0m!")
                    title = "phone:"+dev+"\n module:"+mod+"\n testtime:"+bInfo[0]+" ipaddr:"+bInfo[1]
                    pngPath = pngSavePath+"\\"+product_version+"_"+mod+"_"+str(num)+".png"
                    #draw_pic(rslt[0],rslt[1],title,"time(10 Minutes)","RssMem(M)",pngPath)
                    workbook=xlsxwriter.Workbook(pngSavePath+"\\"+product_version+"_"+mod+"_"+str(num)+".xlsx")
                    worksheet=workbook.add_worksheet()
                    worksheet.write(0, 0, product_version)
                    worksheet.write(0, 1, mod)
                    a=deal_data(rslt[1])
                    for j in range(0,len(a)):
                        worksheet.write(0,j+4,a[j])
                    workbook.close()
                    num += 1

                elif max(rslt[1]) > 200:
                    #print("phone:"+dev+" module:"+mod+" has data" + " maxvalue:" + str(max(rslt[1]))  + "  file:" + logFile )
                    title = "phone:"+dev+"\n module:"+mod+"\n testtime:"+bInfo[0]+" ipaddr:"+bInfo[1]
                    pngPath = pngSavePath+"\\"+product_version+"_"+mod+"_"+str(num)+".png"
                    #draw_pic(rslt[0],rslt[1],title,"time(10 Minutes)","RssMem(M)",pngPath)
                    workbook = xlsxwriter.Workbook(
                        pngSavePath + "\\" + product_version + "_" + mod + "_" + str(num) + ".xlsx")
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0,0,product_version)
                    worksheet.write(0,1,mod)
                    a = deal_data(rslt[1])
                    for j in range(0, len(a)):
                        worksheet.write(0, j+4, a[j])
                    workbook.close()
                    num += 1
    for dev in devSerNo:
        for mod in modlist_all:
            logFile = parPath+"\\"+mod+"\\"+dev+"_"+mod+".txt"
            if os.path.exists(logFile) == False:
                #print(logFile+" not exist")
                continue
            rslt = analyze_logfile(logFile)  #rslt是一个元组，两个元素是两个列表
            if len(rslt[0]) != 0:
                if max(rslt[1]) > 500:   #记录如果峰值>500
                    print("\033[1;35m phone:"+dev+" module:"+mod+" has data" + " maxvalue:" + str(max(rslt[1])) + "  file:" + logFile + "\033[0m!")
                    title = "phone:"+dev+"\n module:"+mod+"\n testtime:"+bInfo[0]+" ipaddr:"+bInfo[1]
                    pngPath = allPngSavePath+"\\"+product_version+"_"+mod+"_"+str(allNum)+".png"
                    #draw_pic(rslt[0],rslt[1],title,"time(10 Minutes)","RssMem(M)",pngPath)
                    workbook = xlsxwriter.Workbook(
                        allPngSavePath + "\\" + product_version + "_" + mod + "_" + str(allNum) + ".xlsx")
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, product_version)
                    worksheet.write(0, 1, mod)
                    a = deal_data(rslt[1])
                    for j in range(0, len(a)):
                        worksheet.write(0, j+4, a[j])
                    workbook.close()
                    allNum += 1

                elif max(rslt[1]) > 200:
                    #print("phone:"+dev+" module:"+mod+" has data" + " maxvalue:" + str(max(rslt[1]))  + "  file:" + logFile )
                    title = "phone:"+dev+"\n module:"+mod+"\n testtime:"+bInfo[0]+" ipaddr:"+bInfo[1]
                    pngPath = allPngSavePath+"\\"+product_version+"_"+mod+"_"+str(allNum)+".png"
                    #draw_pic(rslt[0],rslt[1],title,"time(10 Minutes)","RssMem(M)",pngPath)
                    workbook = xlsxwriter.Workbook(
                        allPngSavePath + "\\" + product_version + "_" + mod + "_" + str(allNum) + ".xlsx")
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, product_version)
                    worksheet.write(0, 1, mod)
                    a = deal_data(rslt[1])
                    for j in range(0, len(a)):
                        worksheet.write(0, j+4, a[j])
                    workbook.close()
                    allNum += 1
    return (num,allNum)
    
def main(argv):
    list = os.listdir(argv[1])
    count = 0
    num = 0
    allNum = 0
    for i in range(0,len(list)):
        path = os.path.join(argv[1], list[i])  #访问文件夹下所有文件
        if os.path.isdir(path):   #文件是否是一个目录
            res_num = parseSingleFolder(path, num, allNum)   #path是外部传入的参数
            num = res_num[0]
            allNum = res_num[1]
            count += 1
    print("deal "+str(count)+" upload folder")
    
if __name__ == '__main__' : 
    main(sys.argv)

    
    
