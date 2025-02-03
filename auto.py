import subprocess
import os

# 检查当前目录是否为 Git 仓库
if not os.path.isdir('.git'):
    print("当前目录不是 Git 仓库，请切换到正确的目录。")
else:
    # 获取用户输入的提交信息
    commit_message = "脚本自动提交"
    try:
        # 执行 git add 操作
        subprocess.run(['git', 'add', '.'], check=True)
        # 执行 git commit 操作
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("提交成功，开始推送...")
        # 执行 git push 操作
        subprocess.run(['git', 'push'], check=True)
        print("推送成功！")
    except subprocess.CalledProcessError as e:
        if e.cmd[-1] == '.':
            error_step = "git add"
        elif e.cmd[1] == 'commit':
            error_step = "git commit"
        else:
            error_step = "git push"
        print(f"{error_step} 失败: {e}")
