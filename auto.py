import subprocess
import os

# 检查当前目录是否为 Git 仓库
if not os.path.isdir('.git'):
    print("当前目录不是 Git 仓库，请切换到正确的目录。")
else:
    # 检查是否有新的更改
    try:
        result = subprocess.run(['git', 'diff', '--quiet', '--exit-code'], check=False)
        has_changes = result.returncode != 0
    except Exception as e:
        print(f"检查更改时出错: {e}")
        exit(1)

    commit_message = "脚本自动提交"

    if has_changes:
        try:
            # 执行 git add 操作
            subprocess.run(['git', 'add', '.'], check=True)
            # 执行 git commit 操作
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("提交成功，开始推送...")
        except subprocess.CalledProcessError as e:
            if e.cmd[-1] == '.':
                error_step = "git add"
            elif e.cmd[1] == 'commit':
                error_step = "git commit"
            print(f"{error_step} 失败: {e}")
            exit(1)
    else:
        print("没有新的更改，直接开始推送...")

    try:
        # 执行 git push 操作
        subprocess.run(['git', 'push'], check=True)
        print("推送成功！")
    except subprocess.CalledProcessError as e:
        # 获取错误输出信息
        error_output = e.stderr.decode() if e.stderr else ""
        # 判断是否为合并冲突
        if "merge conflict" in error_output.lower() or "conflict" in error_output.lower():
            print("git push 失败，检测到合并冲突。")
            print("请手动合并分支解决冲突后再尝试推送。")
        else:
            print(f"git push 失败，原因如下: {error_output}")
