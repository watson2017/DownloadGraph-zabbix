# DownloadGraph-zabbix
python 调用zabbix接口获取监控图表

使用python调用zabbix的API，将所需的图表自动下载下来。

代码结构:

![](https://upload-images.jianshu.io/upload_images/6868814-81b59b7d4b6a04f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/235)


- get_zabbix.py  入口文件
- download.py    将图片下载并插入到execl中的文件，此处略
- module.py      调用zabbix的API 获取图表信息文件
- get_value.py   读取环境变量文件
- config.ini     环境信息文件
