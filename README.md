# Black-Hat-Python
一些方便的python版渗透工具。 在《Python黑帽子——黑客与渗透测试编程之道》的基础上做了些许改动 ~~不想用python2~~

- [Black-Hat-Python](#black-hat-python)
  - [nc3.py](#nc3py)
  - [proxy3.py](#proxy3py)
  - [ssh3_client.py](#ssh3clientpy)

## nc3.py

简易版netcat，功能如下：
```
   
   python nc3.py -t 192.168.0.1 -p 8989                         :连接远程192.168.0.1:8989端口
   python nc3.py -l -p 8989 -c                                  :在8989端口开shell
   
   python nc3.py -t 192.168.0.1 -p 8989 -f /sth_to_upload       :本地文件/sth_to_upload发给远程192.168.0.1:8989
   python nc3.py -l -p 8989 -u /home/test.txt                   :在8989端口接受文件并保存在/home/test.txt
   
   echo ABCDEDF |python nc3.py -t 192.168.0.1 -p 135            :send ABCDEDF to 192.168.0.1:135
```

环境配置：
   - python3
   - 无需第三方包

## proxy3.py

简易版proxy，功能如下：

```
    Usage:       python proxy3.py [localhost] [localport] [remotehost] [remoteport] [receive_first]
    Example:     python proxy3.py 127.0.0.1 9000 10.12.132.1 9000 False
    Structure:   localhost:localport <==> proxy3.py <==> remotehost:remoteport
    补充， receive_first可不管。
```

结果如下（自行调整命令行窗口大小，或修改`hexdump()`）：
```
   [==>] sent to remote.
   [<==] Received 289 bytes from remote.
   0000   48 54 54 50 2F 31 2E 31 20 32 30 30 20 4F 4B 0D    HTTP/1.1 200 OK.
   0010   0A 43 6F 6E 74 65 6E 74 2D 54 79 70 65 3A 20 74    .Content-Type: t
   0020   65 78 74 2F 68 74 6D 6C 3B 20 63 68 61 72 73 65    ext/html; charse
   0030   74 3D 55 54 46 2D 38 0D 0A 45 54 61 67 3A 20 22    t=UTF-8..ETag: "
   0040   63 64 32 33 38 34 66 38 36 37 39 62 65 34 39 35    cd2384f8679be495
   0050   62 37 34 31 36 65 32 31 38 63 66 38 66 38 35 65    b7416e218cf8f85e
   0060   22 0D 0A 43 61 63 68 65 2D 43 6F 6E 74 72 6F 6C    "..Cache-Control
   0070   3A 20 70 75 62 6C 69 63 2C 20 6D 61 78 2D 61 67    : public, max-ag
   0080   65 3D 33 31 35 33 36 30 30 30 0D 0A 45 78 70 69    e=31536000..Expi
```

注： 如果需要对请求包、响应包设置规则，可在`response_handler()`、`request_handler()`中补充你想要的规则。

环境配置：
   - python3
   - 无需第三方包

## ssh3_client.py

简易版ssh，需要 `paramiko` 插件
