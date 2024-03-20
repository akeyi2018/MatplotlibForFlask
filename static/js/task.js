function finish_event(id, name) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/finish_event');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.location.href = '/thanks/0/' + name;
        }
    };
    xhr.send(JSON.stringify({
        "id": id,
        "name": name
    }));
}

// タスク終了用
function finish_task(id, name) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/finish_task');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.location.href = '/thanks/1/' + name;
        }
    };
    xhr.send(JSON.stringify({
        "id": id,
        "name": name
    }));
}


function changeBackgroundColor(num) {
    console.log(num);
    switch(num) {
        case 0:
            document.body.style.backgroundColor = '#A57A5F';
            break;
        case 1:
            document.body.style.backgroundColor = '#795341';
            break;
        case 2:
            document.body.style.backgroundColor = '#694337';
            break;
        case 3:
            document.body.style.backgroundColor = '#54342A';
            break;
        case 4:
            document.body.style.backgroundColor = '#3A2016';
            break;
        default:
            document.body.style.backgroundColor = '#A57A5F';
            break;
    }
}