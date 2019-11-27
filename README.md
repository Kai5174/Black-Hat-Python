# Black-Hat-Python
一些方便的python版渗透工具。 在《Python黑帽子——黑客与渗透测试编程之道》的基础上做了些许改动~~不想用python2~~。

# nc3.py

简易python3版netcat，功能如下：
```
   
   python nc3.py -t 192.168.0.1 -p 8989                                     :连接远程192.168.0.1:8989端口
   python nc3.py -l -p 8989 -c                                              :在8989端口开shell
   
   python nc3.py -t 192.168.0.1 -p 8989 -f /sth_to_upload                   :本地文件发给远程192.168.0.1:8989
   python nc3.py -l -p 8989 -u /home/test.txt                               :在8989端口等待文件上传
   
   echo ABCDEDF |python nc3.py -t 192.168.0.1 -p 135                        :send ABCDEDF to 192.168.0.1:135
```
