import { create_flash, post } from "./modfunc.js";
document
  .getElementById("login-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // 阻止表单默认提交

    const email = document.querySelector("input[name='email']").value;
    const password = document.querySelector("input[name='password']").value; // 获取密码字段的值

    const formData = new FormData(); // 创建一个表单数据对象
    formData.append("email", email); // 添加电子邮件字段
    formData.append("password", password); // 添加密码字段

    const response = await post("/login/process", formData);

    if (response.message == "success") {
      // 登录成功，可能执行重定向或其他操作
      window.location.href = "/"; // 重定向到主页
    } else {
      const errorContainer = document.getElementById("error");
      errorContainer.innerHTML = ""; // 清空容器
      errorContainer.appendChild(create_flash(response.message));
    }
  });
