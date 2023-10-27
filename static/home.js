import { post, get } from "./modfunc.js";

const dataElement = document.getElementById("userData");
getData();

async function getData() {
  dataElement.innerHTML = "";
  const items = await get("/getData");
  items.forEach((item, index) => {
    const new_div = document.createElement("div");
    const button = document.createElement("button");
    const text = document.createElement("p");

    button.innerText = "delete";
    // 添加按钮点击事件处理程序
    button.addEventListener("click", () => handleButtonClick(item));
    text.innerText = "pk:" + item["pk"] + ", sk:" + item["sk"];

    new_div.appendChild(button);
    new_div.appendChild(text);
    dataElement.appendChild(new_div);
  });
}

async function handleButtonClick(item) {
  console.log("Button for item " + item["sk"] + " was clicked");
  console.log(item);
  const formData = new FormData(); // 创建一个表单数据对象
  formData.append("pk", item["pk"]); // 添加电子邮件字段
  formData.append("sk", item["sk"]); // 添加密码字段
  await post("/deleteData", formData);
  await getData();
}
