document.addEventListener("DOMContentLoaded", function() {
  // 获取当前页面的路径
  const currentURL = window.location.pathname;
  console.log(currentURL);

  // 获取HTML元素（例如一个<a>元素）
  const linkElement = document.getElementById(currentURL); // 请替换为实际的元素ID
  console.log(linkElement);

  if (linkElement) {
    setTimeout(function() {
      linkElement.className = "nav-link text-secondary";
    }, 0);
  }
});
