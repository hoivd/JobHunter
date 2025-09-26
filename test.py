import subprocess
import os

# Đường dẫn file .tex
tex_file = "data.tex"

# Command để biên dịch file tex thành PDF
# Sử dụng pdflatex (có thể đổi thành xelatex/lualatex)
cmd = ["pdflatex", tex_file]

# Chạy lệnh
result = subprocess.run(cmd, capture_output=True, text=True)

# Kiểm tra kết quả
if result.returncode == 0:
    print("PDF được build thành công!")
else:
    print("Lỗi khi build PDF:")
    print(result.stdout)
    print(result.stderr)
