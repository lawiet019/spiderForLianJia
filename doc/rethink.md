1.
problem:
* 在requests.get的部分遇到了错误requests.exceptions.SSLError: HTTPSConnectionPool
reason:
* SSL证书验证失败
solution:
* 安装相关package, ref:https://blog.csdn.net/qq_31077649/article/details/79013199
deep-in:
* HTTP 与 HTTPS https://www.cnblogs.com/wqhwe/p/5407468.html
* 公钥和私钥 (非对称加密)  https://blog.csdn.net/baidu_36327010/article/details/78659665

2.
problem:
* 请求因为网络问题出现错误捕获错误重复获取
solution:
* ```
  while count < 次数:
    try:
      获取连接
    except:
      处理错误
      count = count + 1
    else:
      pass
```
3.
problem:
* 导出项目所用的包而不导出环境中所有的包
solution:
* 安装pipreqs包
```
pip install pipreqs
```
* 在文件下运行
```
pipreqs ./
```
ref :https://www.cnblogs.com/bonelee/p/8183038.html

4.
problem:
* 在运行pipreqs的包的时候遇到错误 UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 2011: illegal multibyte sequence
reason:
* 由于读取文件编码错误
solution:
  修正pyreqs.py第74行的 encoding = encoding 为encoding ="utf-8"
5.
problem:
* 重拾git
solution :ref:http://www.cnblogs.com/specter45/p/github.html
