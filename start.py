from flask import Flask, session, redirect, url_for, escape, request, render_template, flash,send_from_directory

import os
import _search_info

app  =  Flask(__name__)

@app.route('/')
def  index():
    allPackge_path="allpackge.ini"
    allVersion_product="allVersion_product.ini"
    allPackge_list=_search_info.gen_info(allPackge_path)
    allVersion_product_list=_search_info.gen_info(allVersion_product)
    return  render_template('index.html', allProduct=allVersion_product_list, allPackge=allPackge_list)
    #根据上面的选择反馈的版本号生成模块（文件夹名称）
@app.route('/show',methods=['POST', 'GET'])
def show():
    selected_allVersion = ""
    selected_allPackge = ""
    urllist = []
    if request.method == 'POST':
        try:
            selected_allPackge = request.form['select_allpackge']
            selected_allVersion = request.form['select_allversion']
            check_box = request.form['checkBox']
        except:
            print('verision and packge error')
        pngPath = os.getcwd() + "\\static\\images"
        allPngPath = os.getcwd() + "\\static\\all"
        list = os.listdir(pngPath)
        alllist = os.listdir(allPngPath)
        if check_box=="0":    #优先内存泄漏的
            for i in range(0,len(list)):
                fileName = selected_allVersion+"_"+selected_allPackge+"_"+str(i)+".png"
                if fileName in list:
                    url = url_for("static", filename="images/"+fileName)   #这里将urllist搞成二元组列表url[0]为图片，url[1]为excel表格
                    urllist.append(url)
        else:
            for i in range(0,len(alllist)):
                fileName = selected_allVersion+"_"+selected_allPackge+"_"+str(i)+".png"
                if fileName in alllist:
                    url = url_for("static", filename="all/"+fileName)
                    urllist.append(url)

        return render_template('show.html',urllist=urllist)
    else:
        return render_template('show.html')


if  __name__  ==  '__main__':

    app.run(host='0.0.0.0',  debug=True)