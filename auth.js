/*
  auth.js - kiểm tra đăng nhập dùng chung cho cả website.

  Cách dùng (đặt trong <head> của từng trang):
    <script src="../auth.js" data-require="user"></script>   -> phải đăng nhập
    <script src="../auth.js" data-require="admin"></script>  -> phải là tài khoản admin
    <script src="auth.js"></script>                          -> không chặn (dùng ở index.html)

  Đường dẫn "../auth.js" dùng cho trang nằm trong thư mục con (User, ADMIN),
  "auth.js" dùng cho trang nằm ở thư mục gốc (index.html, h.html).
*/
(function () {
  var script = document.currentScript;
  var need = script.getAttribute('data-require');

  // Thư mục chứa auth.js (thư mục gốc của web), tính từ đường dẫn của chính file này
  var root = new URL('.', script.src);
  var loginUrl = new URL('User/login.html', root).href;
  var homeUrl = new URL('index.html', root).href;

  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  var logged = read('isLoggedIn') === 'true';
  var isAdmin = logged && read('role') === 'admin';

  window.Auth = {
    isLoggedIn: function () { return logged; },
    isAdmin: function () { return isAdmin; },
    username: function () { return read('username') || ''; },
    logout: function () {
      try {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('username');
        localStorage.removeItem('role');
      } catch (e) {}
      location.href = homeUrl;
    }
  };

  if (!need) return;

  var allowed = need === 'admin' ? isAdmin : logged;
  if (!allowed) {
    // Ẩn trang ngay để người dùng không thấy nội dung nháy lên trước khi chuyển hướng
    document.documentElement.style.display = 'none';
    if (need === 'admin' && logged) {
      alert('Chỉ tài khoản admin mới được vào trang quản trị.');
    }
    location.replace(loginUrl);
  }
})();
