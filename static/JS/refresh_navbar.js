function refresh() {
  $.get("api/get_unread", (response) => {
    data = response["count"];
    $("#unread").text(data);
  });
}
refresh();
let navbar_socket = new WebSocket(`ws://${window.location.host}/chat`);
navbar_socket.onmessage = function (e) {
  let data = JSON.parse(e.data);
  let type = data["type"];
  if (type == "update") {
    $("#unread").text(data["unread_msgs"]);
  }
};
