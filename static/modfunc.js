// $("#button1").on("click", function () {
//   const num1 = $("#num1").val();
//   const num2 = $("#num2").val();
//   const data = JSON.stringify({ num1, num2 });
//   const item = $("#result");
//   post(data, item, "/api/add");
// });

// $("#button2").on("click", function () {
//   const num1 = $("#num1").val();
//   const num2 = $("#num2").val();
//   const data = JSON.stringify({ num1, num2 });
//   const item = $("#result2");
//   post(data, item, "/api/min");
// });

export async function post(data, url) {
  try {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data,
    };
    const response = await fetch(url, requestOptions);
    const req = await response.json();
    console.log(req);
    return req;
  } catch (error) {
    console.log("post_error");
    return "error";
  }
}
