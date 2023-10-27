import { create_flash, post } from "./modfunc.js";

const signupForn = document.getElementById("signupForm");

signupForn.addEventListener("submit", async function (event) {
  event.preventDefault(); // 阻止表单默认提交
  const formData = new FormData(signupForn); // 创建一个表单数据对象
  const response = await post("/createUser", formData);
  if (response.message == "success") {
    // 登录成功，可能执行重定向或其他操作
    window.location.href = "/"; // 重定向到主页
  } else {
    const errorContainer = document.getElementById("error");
    errorContainer.innerHTML = ""; // 清空容器
    errorContainer.appendChild(create_flash(response.message));
  }
});
