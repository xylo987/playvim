function old_upload() {
    var files = document.querySelector('.upload').files;
    if (!files) return alert('未选择文件');
    var formdata = new FormData();
    for (var i = 0; i < files.length; i++) {
        formdata.append('fs', files[i]);
    }
    var xhr = new XMLHttpRequest();
    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var h = Math.ceil(e.loaded / e.total) * 100;
            console.log(h);
        }
    };
    xhr.upload.onload = function() {

    };
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4) {
            var data = JSON.parse(xhr.responseText);
            if (data.status == 200) 
                alert('全部上传成功');
            else if(data.status == 199)
                alert('部分上传成功');
            else if(data.status == 198)
                alert('全部上传失败')

            location.reload();
        }
    };
    xhr.open('POST', '/upload');
    xhr.send(formdata);
}

window.onload = function() {
    /*
    真的能被这个新API气死
    document.querySelector('#upload').onclick = function() {
        let fd = new FormData();
        let fs = document.querySelector('.upload').files;
        fd.append('mp3s', fs);
        fetch('/upload', {
            method: 'post',
            body: fd
        }).then(response => response.json())
        .then(function (data) {
            if (data.status == 200) {
                location.realod();
            }
        });
    };
    */
    document.querySelector('#upload').onclick = old_upload;

    fetch('/', {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'page': 1,
        })
    }).then(response => {
        return response.json();
    }).then(res => {
        let table = document.querySelector('#pl > table');
        let table_html = '<tr> <th class="left">名字</th>\
            <th class="right">操作</th> </tr>';
        console.log(res);
        for (let i = 0; i < res.data.length; i++) {
            let music = res.data[i];
            title = music[1];
            index = music[0];
            table_html += '<tr><td class="left" i="' + index + '">' + title + '</td>\
                <td class="right"><button class="del" i="' + index + '">删除</button>\
                <button class="rename" i="' + index + '">更名</button></td></tr>';
        }
        table.innerHTML = table_html;
    });

    document.querySelector('table').onclick = function(e) {
        let play_doms = document.querySelectorAll('td')
        for (let i = 0; i < play_doms.length; i++) {
            let play_dom = play_doms[i];
            if (e.target == play_dom) {
                let index = play_dom.getAttribute('i');
                let audio = document.querySelector('audio');
                audio.src = '/play?index=' + index;
                audio.play();
                break;
            }
        }

        let del_doms = document.querySelectorAll('#pl > table > \
            tbody > tr > td > .del');
        for (let i = 0; i < del_doms.length; i++) {
            let del_dom = del_doms[i];
            if (e.target == del_dom) {
                let index = del_dom.getAttribute('i');
                let cf = confirm('确定要删除?');
                if (cf == true) {
                    fetch('/del?index=' + index
                    ).then(response => 
                        response.json()
                    ).then(function(res) {
                        console.log(res);
                        if (res.status == 200) {
                            location.reload();
                        }
                    });
                }
                break;
            }
        }

        let rename_doms = document.querySelectorAll('#pl > table >\
                                                tbody >  tr > td > .rename');
        for (let i = 0; i < del_doms.length; i++) {
            let rename_dom = rename_doms[i];
            if (e.target == rename_dom) {
                let new_name = prompt('请输入新的名称：');
                if (new_name) {
                    let index = rename_dom.getAttribute('i');
                    fetch('/rename?index=' + index + '&new_name=' + new_name
                    ).then(response => 
                        response.json()
                    ).then(function(res) {
                        if (res.status == 200) location.reload();
                    });
                }
            }
        }
    };
};
