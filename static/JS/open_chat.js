function open_chat() {
  let target_id = $("#hidden-data").data("my-value");
  console.log(target_id);
  $.post("api/open_chat", { id: target_id });
  window.location.href = "inbox";
}
$(document).ready(() => {
  console.log($("#posalji_poruku"));
  $("#posalji_poruku").on("click", open_chat);
});
