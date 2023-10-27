import { create_flash, gettoken, post, settoken } from "./modfunc.js";

const loginForm = document.getElementById("loginForm");
const errorContainer = document.getElementById("error");
let load = false;

loginForm.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const data = new FormData(loginForm);
  console.log(data);
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/auth/token", true);

  xhr.onload = (ev) => {
    const responseData = JSON.parse(xhr.responseText);
    if (xhr.status === 200) {
      settoken(`${responseData.token_type} ${responseData.access_token}`);
      fetch("/", {
        method: "GET",
        headers: {
          Authorization: gettoken(),
        },
      });
      //"/"; // 重定向到主页
    } else {
      errorContainer.innerHTML = ""; // 清空容器
      errorContainer.appendChild(create_flash(responseData.message));
    }
  };
  console.log(1);
  xhr.send(data);
});
