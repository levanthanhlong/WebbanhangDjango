// var loginLink = document.getElementById('loginLink');
// var signupLink = document.getElementById('registerLink');

// // var loggedIn = true; // Thay đổi giá trị này tùy thuộc vào trạng thái đăng nhập

// function isLoggedIn() {
//     return document.cookie.includes("csrftoken"); // Thay "sessionID" bằng tên cookie xác thực của bạn
// }
// // var loggedIn = isLoggedIn();
// var loggedIn = false;
// console.log(loggedIn);

// if (loggedIn) {
//   // Nếu đã đăng nhập, ẩn phần đăng nhập và đăng kí, hiển thị phần hồ sơ và đăng xuất
//   loginLink.style.display = 'none';
//   registerLink.style.display = 'none';
//   usernameLink.style.display = 'block';
  
// } else {
//   // Nếu chưa đăng nhập, hiển thị phần đăng nhập và đăng kí, ẩn phần hồ sơ và đăng xuất
//   loginLink.style.display = 'block';
//   registerLink.style.display = 'block';
//   usernameLink.style.display = 'none';
// }