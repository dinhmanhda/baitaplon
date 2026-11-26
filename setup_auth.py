"""
setup_auth.py - chạy MỘT LẦN trong thư mục gốc của web (thư mục 'BTL Web').

Việc script làm:
  1. Thêm 1 dòng <script src="...auth.js"> vào <head> của các trang cần bảo vệ.
  2. Thay phần <script> ở cuối User/login.html bằng bản có kiểm tra tài khoản admin.

Chạy lại nhiều lần vẫn an toàn (trang nào đã có thì bỏ qua).
Nếu muốn hoàn tác: git checkout -- .   (khi đã commit trước đó)
"""
import os
import re

# (đường dẫn trang, quyền yêu cầu, đường dẫn tới auth.js)
PAGES = [
    ("User/home.html",           "user",  "../auth.js"),
    ("User/sanpham.html",        "user",  "../auth.js"),
    ("User/giohang.html",        "user",  "../auth.js"),
    ("User/lienhe.html",         "user",  "../auth.js"),
    ("h.html",                   "user",  "auth.js"),
    ("ADMIN/quanlikhachhang.html", "admin", "../auth.js"),
    ("ADMIN/quanlisanpham.html",   "admin", "../auth.js"),
]

LOGIN_SCRIPT = """<script>
    // Tài khoản quản trị. Muốn đổi mật khẩu admin thì sửa ở đây.
    const ADMIN_USER = 'admin';
    const ADMIN_PASS = 'admin123';

    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (username === '' || password === '') {
            alert('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!');
            return;
        }

        const isAdminName = username.toLowerCase() === ADMIN_USER;
        if (isAdminName && (username !== ADMIN_USER || password !== ADMIN_PASS)) {
            alert('Sai mật khẩu tài khoản admin!');
            return;
        }

        const box = document.getElementById('successAlert');
        box.style.display = 'block';

        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('username', username);
        localStorage.setItem('role', isAdminName ? 'admin' : 'user');

        setTimeout(function() {
            window.location.href = isAdminName ? '../ADMIN/quanlisanpham.html' : 'home.html';
        }, 2000);
    });
</script>"""


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def add_guard(path, need, src):
    if not os.path.exists(path):
        print("  [BỎ QUA] Không thấy file:", path)
        return
    html = read(path)
    if "auth.js" in html:
        print("  [ĐÃ CÓ ] ", path)
        return

    tag = '<script src="%s" data-require="%s"></script>' % (src, need)
    # Chèn ngay sau </title>; nếu không có thì chèn sau <head>
    m = re.search(r"</title>", html, re.IGNORECASE) or re.search(r"<head[^>]*>", html, re.IGNORECASE)
    if not m:
        print("  [LỖI    ] Không tìm thấy <head> trong:", path)
        return
    nl = "\r\n" if "\r\n" in html else "\n"
    html = html[:m.end()] + nl + "    " + tag + html[m.end():]
    write(path, html)
    print("  [ĐÃ THÊM] ", path, "(", need, ")")


def patch_login(path):
    if not os.path.exists(path):
        print("  [BỎ QUA] Không thấy file:", path)
        return
    html = read(path)
    if "ADMIN_USER" in html:
        print("  [ĐÃ CÓ ] ", path)
        return
    blocks = list(re.finditer(r"<script>.*?</script>", html, re.DOTALL | re.IGNORECASE))
    if not blocks:
        print("  [LỖI    ] Không tìm thấy khối <script> trong:", path)
        return
    last = blocks[-1]
    html = html[:last.start()] + LOGIN_SCRIPT + html[last.end():]
    write(path, html)
    print("  [ĐÃ SỬA ] ", path)


def main():
    if not os.path.exists("auth.js"):
        print("Không thấy auth.js ở thư mục hiện tại.")
        print("Hãy đặt auth.js và setup_auth.py ở thư mục gốc 'BTL Web' rồi chạy lại.")
        return

    print("Thêm kiểm tra đăng nhập vào các trang:")
    for path, need, src in PAGES:
        add_guard(path, need, src)

    print("Cập nhật trang đăng nhập:")
    patch_login("User/login.html")

    print("Xong.")


if __name__ == "__main__":
    main()
