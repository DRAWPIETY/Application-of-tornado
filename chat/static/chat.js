$(function(){
    n = $("#n").val();
    u = $("#u").val();
    username = $("#name").val();

    $("#send").click(function(){
        sendText();
    })
    $("#message").on("keypress", function(e) {
        if (e.keyCode == 13) {
            if ($("#message").val()){
                websocket.send($("#text").val());
                document.getElementById("message").value="";
            }else{
                alert("Can't send a void message!");
            }
            return false;
        }
            return  true;
      })

    function sendText(){    // 向服务器发送信息
        if ($("#message").val()){
            websocket.send($("#message").val());
            document.getElementById("message").value="";
        }else{
            alert("发送消息不能为空！");
        }
    }

    function requestText(){
        host = "ws://localhost:8888/chat/update/?n=" + n + "&u=" +u+ "&username="+username;
        websocket = new WebSocket(host);

        websocket.onopen = function(evt){};     // 建立连接
        websocket.onmessage = function(evt){    // 获取服务器返回的信息
            data = $.parseJSON(evt.data);
            if(data['from']=='system'){
                $('#inbox').append("<p style='width: 100%; text-align:center; font-size: 16px; color: green'>" + data['message'] + "</p>");
            }else if(data['from']==username){
                $('#inbox').append("<p style='width: 100%; text-align:right; font-size:15px'>" + username + ": <br>&emsp;" +"<span style='color: blue'>" + data['message'] + "</span>" + "</p>");
            }else{
                $('#inbox').append("<p style='width: 100%; text-align:left; font-size:15px'>" + data['from'] + ": <br>&emsp;" +"<span style='color: red'>" + data['message'] + "</span>" + "</p>");
            }
        }
        websocket.onerror = function(evt){};
    }
    requestText();   // 开始 websocket

})