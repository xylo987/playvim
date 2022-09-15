# :scream_cat: playvim

:bug:我用vim就是，没事的时候，玩玩配置娱乐一下，我不会用vim做所有的事。

![image](https://user-images.githubusercontent.com/111848062/190047018-d3ab0df0-9b6e-457d-a908-9ead09102ed1.png)

:joy:

:bug:安装

```bash
cd ~
git clone https://github.com/syz-lm/playvim .vim_runtime
echo 'source $HOME/.vim_runtime/__init__.vim' > .vimrc
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim +PlugInstall
```

:bug:一些私人的情趣

![image](https://user-images.githubusercontent.com/111848062/189804977-3cf0bdd1-0a15-4ff9-bc6e-22754fe118b7.png)

* `<F1>`: 打开配置
* `<F2>`: 文件树
* `<F3>`: 函数树
* `<F4>`: 预览【还没功能】
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

:bug:我的私人音乐盒子

* `<leader>1`: 启动音乐盒子服务器
* `<leader>2`: 命令行输入命令控制音乐盒子

:bug:补全的资料

![image](https://pic1.zhimg.com/80/v2-c4091188211694144634a8f11e3799b8_720w.jpg)

Good luck :cupid::corn::strawberry:
