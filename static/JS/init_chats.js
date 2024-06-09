var socket;
function start_websocket() {
  var user_id = parseInt(
    document.getElementById("body").getAttribute("user_id"),
  );
  socket = new WebSocket(`ws://${window.location.host}/chat`);
  socket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let type = data["type"];
    let time = data["time"];
    console.log(time);
    if (type == "chat") {
      let msg = data["message"];
      $("#chat-box").prepend(
        `
				<div>
				<div class='time'>` +
          time +
          `</div>
				<div class="message">` +
          msg +
          `</div>
				</div>
				`,
      );
    } else {
      $("#unread").text(data["unread_msgs"]);
      get_chats(); // zameni sa pametnijom logikom ako oces ali ovo radi
    }
    console.log(data);
  };
  var currentChat = null;
  let list = document.getElementById("chats");
  list.addEventListener("click", (e) => {
    let chatid = parseInt(e.target.getAttribute("name"));
    let chatUserName = e.target.getAttribute("userChatName");
    $("#chatUserName").html(chatUserName);
    console.log(chatid);
    console.log(e.target.getAttribute("name"));
    console.log(e.target);
    if (currentChat != null) {
      socket.send(
        JSON.stringify({
          type: "close_chat",
        }),
      );
    }
    currentChat = chatid;
    socket.send(
      JSON.stringify({
        type: "open_chat",
        chat_id: chatid,
      }),
    );
    $.get("api/get_messages?id=" + chatid, function (response) {
      let messages = response["messages"];
      var str = "";
      for (let message of messages) {
        if (message["sender"] != user_id) {
          str =
            `
						<div>
						<div class='time'>` +
            message["time"] +
            `</div>
						<div class="message">` +
            message["text"] +
            `</div>
						</div>

						` +
            str;
        } else {
          str =
            `
						<div>
						<div class='time ml-auto'>` +
            message["time"] +
            `</div>
						<div class="message myMessage ml-auto">` +
            message["text"] +
            `</div>
						</div>
						` +
            str;
        }
      }
      $("#chat-box").html(str);
      document
        .getElementById("chat-form")
        .setAttribute("style", "visibility: visible !important;");
      get_chats(); // zameni sa pametnijom logikom ako oces ali ovo radi
    });
    setTimeout(refresh, 1000);
  });

  let form = document.getElementById("chat-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let message = e.target.newmsg.value;
    console.log(message);
    console.log(message == "");
    if (message == "") {
      return;
    }
    var currentdate = new Date();
    let time = currentdate.toISOString().split(".")[0];
    time = time.replace("T", "@");
    $("#chat-box").prepend(
      `
			<div>
			<div class="time ml-auto">` +
        time +
        `</div>
			<div class="message myMessage ml-auto">` +
        message +
        `</div>
			</div>`,
    );
    socket.send(
      JSON.stringify({
        type: "chat",
        message: message,
      }),
    );
    form.reset();
  });
}
function get_chats() {
  let str1 = "";
  $.get("api/get_chats", function (response) {
    let chats = response["chats"];
    console.log(chats);
    for (let chat of chats) {
      str1 += `
				<li class="list-group-item d-flex" name="${chat["id"]}" userChatName="${chat["user"]}">
				<div name="${chat["id"]}" userChatName="${chat["user"]}"> ${chat["user"]}</div>`;
      if (chat["messages_unread"] > 0) {
        str1 += `<div name="${chat["id"]}" userChatName="${chat["user"]}" class="badge bg-danger ml-auto"> ${chat["messages_unread"]} </div>`;
      }
      str1 += `</li>`;
    }
    $("#chats").html(str1);
  });
}
