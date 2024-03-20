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
