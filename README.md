# FreePiano-AutoPlay
# 环境依赖
必须为windows操作系统
```
win32api
win32con
win32gui
win32process
pythoncom
pyHook
```
# 乐谱撰写方式
将音乐文件写入到data中即可：

乐谱文件的格式为：

按键 按下时间 停顿时间

比如：

a 1 2

b 2 3

将按下a按键1s，随后停留2s。然后按下b按键2s，随后停留3s

# 启动方式
控制台命令进入到keyboard.py所在文件夹，python keyboard.py即可。也可以用pyinstaller打包成傻瓜式程序，那时候双击打开就可以。

# 控制方式
在freepiano处于前台的时候，不能控制，因为freepiano需要接受整个键盘输入作为钢琴键盘。切换到别的软件后。按下s为暂停，p为继续播放，q为退出，数字0到9对应data文件夹下面字典序前10的音乐文件。比如按下1，将播放1对应的音乐文件，当然需要切换回前台才能继续播放。
