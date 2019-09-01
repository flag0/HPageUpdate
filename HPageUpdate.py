#coding=utf-8
import sys
import os
import time
import re
import shutil


"""
Author:flag0
email:root@flag0.com
"""

def if_Image_path(path):#判断图片路径是否为绝对路径 True return 1
    if ":" in path:
        return 1
    return 0

def Clear_Image_path(path):#清洗掉markdown语法字符，只剩下图片路径
    path = path[path.index("]")+2:-1]
    return path

def Relative_to_Absolute(Relative_path,md_File_path):#将相对路径转换为绝对路径
    path = md_File_path[:md_File_path.rindex("/")+1]
    Image_path = path + Relative_path
    Image_path = Image_path.replace("/","\\")
    return Image_path

def find_Images(path):#查找图片路径
    md_File = open(path,"rb+")
    md_File_contant = md_File.read()
    md_File_contant = str(md_File_contant,encoding="utf-8")
    res = re.compile("!\[.+?\)")
    Image_path_list = re.findall(res,md_File_contant)
    print("Image_list:",len(Image_path_list))
    return Image_path_list

def Image_Copy(md_blog_Image_Folder_path,Image_path,Relative_path):#图片复制
    Image_Folder_path = md_blog_Image_Folder_path + Relative_path[:Relative_path.rindex("/")].replace(".assets","")
    if (not os.path.exists(Image_Folder_path)):
        os.mkdir(Image_Folder_path)
        print("[+]mkdir "+Image_Folder_path)
    Image_path_c = Image_Folder_path + "\\"+Relative_path[Relative_path.rindex("/")+1:]
    try:
        shutil.copy(Image_path, Image_path_c)
        print("[+]Copy "+Image_path_c)
        return 1
    except:
        print("[-]Error Copy"+Image_path_c)
        return 0
def Copy_image_Folder(md_File_path,md_blog_Image_Folder_path):
    print("======start Copy images to Folder======")
    Image_path_list = find_Images(md_File_path)#获取正则匹配到的images列表
    for Image_path in Image_path_list:
        Image_path_y = Clear_Image_path(Image_path)
        if (not if_Image_path(Image_path_y)):
            Image_path = Relative_to_Absolute(Image_path_y,md_File_path)

        if os.path.exists(Image_path):
            Image_Copy(md_blog_Image_Folder_path, Image_path, Image_path_y)
        else:
            print("[-] Error "+Image_path+"not existence")


def Replace_md_Image_path(md_blog_Page_path):#from Page md image path replace to web image path
    md_Page = open(md_blog_Page_path,"r+",encoding="utf-8")#r+ w+ a+ 都是以读写的方式打开
    md_Page_content_list = md_Page.readlines()
    new_md_Page_content_list = []
    for md_Page_content in md_Page_content_list:
        if ("](" in md_Page_content):
            replace_content = "\\img\\images\\"+md_Page_content[md_Page_content.index("](")+2:-1].replace(".assets/","\\")
            md_Page_content = md_Page_content.replace(md_Page_content[md_Page_content.index("](") + 2:-1],replace_content)
        new_md_Page_content_list.append(md_Page_content)
    md_Page.seek(0)#定位到文件开头
    md_Page.truncate()#清空内容
    md_Page.writelines(new_md_Page_content_list)
    md_Page.close()

def Copy_md_Folder(md_File_path,md_blog_Page_Folder_path):
    print("======start Copy md to Folder======")
    md_File_name = md_File_path[md_File_path.rindex("\\")+1:]
    md_blog_Page_path = md_blog_Page_Folder_path + md_File_name
    print(md_File_path,md_blog_Page_path)
    try:
        shutil.copy(md_File_path,md_blog_Page_path)
    except:
        print("[-] Error:Copy_md_Folder False")
        exit(0)

    Replace_md_Image_path(md_blog_Page_path)
    return md_blog_Page_path

def Command(cmd):
    #'cd F://blog && hexo clean && hexo generate && hexo d'
    os.system(cmd)
    print("[+]===== {0} run Success=====".format(cmd))


def Hexo_Command():
    print("======start update to Github======")
    cmd_list = ["hexo clean","hexo g","hexo d"]#"hexo clean","hexo generate",
    for cmd in cmd_list:
        Command(cmd)
def add_data(md_blog_Page_path,Page_title,Page_category, Page_tag,Page_date):
    new_md_Page_content_list = []
    new_md_Page_content_list.append("---\n")
    new_md_Page_content_list.append("title: {0}\n".format(Page_title))
    new_md_Page_content_list.append("tags:\n")
    for tag in Page_tag:
        new_md_Page_content_list.append("- {0}\n".format(tag))
    new_md_Page_content_list.append("category:\n")
    new_md_Page_content_list.append("- {0}\n".format(Page_category))
    new_md_Page_content_list.append("date: {0}\n".format(Page_date))
    new_md_Page_content_list.append("---\n")

    md_Page = open(md_blog_Page_path, "r+", encoding="utf-8")  # r+ w+ a+ 都是以读写的方式打开
    md_Page_content_list = md_Page.readlines()
    new_md_Page_content_list += md_Page_content_list
    md_Page.seek(0)  # 定位到文件开头
    md_Page.truncate()  # 清空内容
    md_Page.writelines(new_md_Page_content_list)
    md_Page.close()
    return new_md_Page_content_list

def t_time():#取当前 时分秒
    year = time.localtime().tm_year
    mon = time.localtime().tm_mon
    day = time.localtime().tm_mday

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec
    time_strings = "%s-%s-%s %s:%s:%s" %(year,mon,day,hour,minute,second)
    return time_strings



if __name__ == '__main__':
    md_File_path = sys.argv[1]
    md_blog_Image_Folder_path = ""
    md_blog_Page_Folder_path = ""
    md_blog_path_list = open("path.ini","r+").readlines() # from ini get blog image path & page path
    Page_title = sys.argv[2]
    Page_category = sys.argv[3]
    Page_tag = []
    Page_tag_text = sys.argv[4]
    Page_tag = Page_tag_text.split(",")

    try:
        Page_date = sys.argv[5].replace(";"," ")
    except IndexError:
        Page_date = t_time()

    for line in md_blog_path_list:
        if("md_blog_Image_Folder_path=" in line):
            md_blog_Image_Folder_path = line[len("md_blog_Image_Folder_path="):].replace("\n","")
        if("md_blog_Page_Folder_path=" in line):
            md_blog_Page_Folder_path = line[len("md_blog_Page_Folder_path="):].replace("\n","")
    os.chdir(md_blog_Page_Folder_path)  # 改变当前工作目录到博客目录
    Copy_image_Folder(md_File_path,md_blog_Image_Folder_path)
    md_blog_Page_path = Copy_md_Folder(md_File_path,md_blog_Page_Folder_path)
    add_data(md_blog_Page_path, Page_title, Page_category, Page_tag, Page_date)
    Hexo_Command()
