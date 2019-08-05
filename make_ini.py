import os

def devices_info(file_path):
    try:
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                devices_name=line
                line=f.readline()
    except FileNotFoundError:
        print(file_path + " has lost")
    return devices_name
def deal_hprof(info):   #返回type
    line=info.split('/')
    type_size=line[5]
    type=type_size.split('_')[0]
    if type == 'system':
        type='system_server'
    return type
def analyze_hprofinfo(hprof_path):
    type = []
    try:
        with open(hprof_path, 'r') as f:
            line = f.readline()
            while line:
                eachline = line.split()    #六个元素
                type.append(deal_hprof(eachline[4]))   #存放在列表
                line=f.readline()
    except FileNotFoundError:
        print(hprof_path + " has lost")
    return type    #返回包名列表
def deal_verision(devices_name):
    verision = ""
    if len(devices_name.split())==2:
        verisioninfo=devices_name.split()[1]
        verision=verisioninfo.split('(')[0]
    return verision
def deal_product(devices_name):
    product = ""
    if len(devices_name.split())==2:
        productinfo=devices_name.split()[0]
        product=productinfo.split('-')[0]
    return product
def deal_product_version(devices_name):
    res=""
    if len(devices_name.split())==2:
        product_version=devices_name.split('\n')[0]
        str1=product_version.split()[0]
        str2=product_version.split()[1]
        res=str1+"_"+str2
    return res
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
#这里需要添加一个参数记录行数。最后要将这个参数返回
def insert_excal(folder, filename, verision_info):   #filename就是日志路径
    allVersion_product = []   #所有的
    if os.path.exists(folder+"\\devicesInfo.txt"):
        devices_name=devices_info(folder+"\\devicesInfo.txt")  #An的信息
        product_version = deal_product_version(devices_name)
        allVersion_product.append(product_version)
    all_packge_list = analyze_modulelist(folder+"\\module.ini")
    return (all_packge_list,allVersion_product)
def delete_repeat(list):
    res_list = []
    for i in list:
        if not i in res_list:
            res_list.append(i)
    return res_list
def write_info(path, serials):
    try:
        with open(path,'w') as f:
            for serial in serials:
                if serial!="":
                    f.write(serial+"\n")
    except:
        print(path + "has lost")

def main(folder,version):     #当前目录和version
    list = os.listdir(folder) #传入的参数为当前目录
    count = 0
    res_allPackge = []
    res_allVersion_product = []
    for i in range(0, len(list)):
        path = os.path.join(folder, list[i])  # 访问文件夹下所有文件
        if os.path.isdir(path):  # 文件是否是一个目录
            a = insert_excal(path, list[i], version)
            res_allPackge = res_allPackge + a[0]
            res_allVersion_product = res_allVersion_product + a[1]
            count += 1
    allPackge_list = delete_repeat(res_allPackge)
    allVersion_product = delete_repeat(res_allVersion_product)
    allPackge_path = "..\\venv\\allpackge.ini"
    allVersion_product_path = "..\\venv\\allVersion_product.ini"
    write_info(allPackge_path,allPackge_list)
    write_info(allVersion_product_path,allVersion_product)
    print("succeed!")

if __name__ == '__main__':
    main("//10.176.166.7/data","")