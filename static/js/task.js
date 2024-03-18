// イベント終了用
function finish_event(id, name){
$.ajax({
    method: 'post',
    url: '/finish_event',
    data: JSON.stringify({
    "id": id,
    "name": name
    }),
    contentType: 'application/json;charset=UTF-8',
    success: function(){
        window.location.href = '/thanks/0/' + name;
    }
});
}

//タスク終了用
function finish_task(id, name){
$.ajax({
    method: 'post',
    url: '/finish_task',
    data: JSON.stringify({
    "id": id,
    "name": name
    }),
    contentType: 'application/json;charset=UTF-8',
    success: function(){
        window.location.href = '/thanks/1/' + name;
    }
});
}
