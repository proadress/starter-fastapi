$(document).ready(function () {
  // 獲取當前網址
  const currentURL = window.location.pathname;
  console.log(currentURL);
  // 獲取HTML元素（例如一個<a>元素）
  const linkElement = document.getElementById(currentURL); // 請替換為實際的元素ID
  console.log(linkElement);
  if (linkElement) {
    setTimeout(function () {
      linkElement.className = "nav-link text-secondary";
    }, 0);
  }
});
