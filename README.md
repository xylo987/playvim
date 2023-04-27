# :scream_cat: playvim

:bug:我用vim就是，没事的时候，玩玩配置娱乐一下，我不会用vim做所有的事。

:joy:

:bug:安装

```bash
cd ~
git clone https://github.com/xylo987/playvim .vim_runtime
echo 'source $HOME/.vim_runtime/__init__.vim' > .vimrc
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim +PlugInstall
```

安装完毕之后需要设置`pythonthreehome`的值，具体需要借助搜索引擎。

:bug:一些私人的情趣

![image](https://user-images.githubusercontent.com/111848062/189804977-3cf0bdd1-0a15-4ff9-bc6e-22754fe118b7.png)

* `<F1>`: 进入配置目录
* `<F2>`: 文件树
* `<F3>`: 函数树
* `<F4>`: 进入snippets目录
* `<F5>`: 运行【仅仅支持Python, Rust】
* `<F6>`: 调试【还没功能】
* `<F7>`: 新命令行
* `<F8>`: 前命令行
* `<F9>`: 后命令行
* `<F10>`: 关闭一个命令行
* `<F11>`: 暂时无
* `<F12>`: 隐藏终端
* `<C-]>`: 代码补全【vim自动补全看后面的信息图片】
* `<Tab>`: 代码片段补全【需要学snippets的写法】
* `<leder>r`: 以buffer目录打开nerdtree

:bug:我的私人音乐盒子

![image](https://user-images.githubusercontent.com/111848062/190531667-2fca3bb8-dedc-4f04-a119-3d0ae10bba12.png)

* `<leader>1`: 启动音乐盒子服务器
* `<leader>2`: 命令行输入命令控制音乐盒子
* `<leader>3`: 启动音乐盒子后台管理服务

![image](https://user-images.githubusercontent.com/111848062/190531503-ad9ee5e4-c85b-45da-8222-f0d65b00af47.png)

:bug:我的私人聊天工具

![image](https://user-images.githubusercontent.com/111848062/190949651-058800ba-a6e9-4818-9b59-81d5f24dedd0.png)

* `<leader>4`: 配置通讯服务器信息
* `<leader>5`: 启动服务器，如果服务器在远程，就不用启动，直接启动客户端连接聊天即可
* `<leader>6`: 启动客户端

:bug:

:joy:

:bug:补全的资料

![image](https://pic1.zhimg.com/80/v2-c4091188211694144634a8f11e3799b8_720w.jpg)

Good luck :cupid::corn::strawberry:
