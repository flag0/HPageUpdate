---

HpageUpdate.py
path.ini //配置hexo 文章及图片路径

---

**功能介绍**
简化hexo发稿流程小工具
简化hexo发文章流程，自动处理hexo文章图片与引用关系
**使用实例**

```
python HPageUpdate.py F:/g/代码空白区添加shellcode.md 代码空白区添加shellcode 编程开发 shellcode,PE 2019-6-25;22:00:03
```

即

```
python HpageUpdate.py PagePath title category tags1,tags2,,, year-moth-day;h:t:s
```

如果不填写时间，默认为当前时间

**path.ini**

```
md_blog_Image_Folder_path=F:\blog\themes\jacman\source\img\images\
md_blog_Page_Folder_path=F:\blog\source\_posts\
```

- `md_blog_Image_Folder_path` hexo图片存放路径
- `md_blog_Page_Folder_path` hexo 文章存放路径
