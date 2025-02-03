import subprocess
import os

# 检查当前目录是否为 Git 仓库
if not os.path.isdir('.git'):
    print("当前目录不是 Git 仓库，请切换到正确的目录。")
    exit(1)

try:
    # 检查工作区是否有更改（未暂存更改）
    wt_diff = subprocess.run(['git', 'diff', '--quiet'], check=False)
    has_working_changes = wt_diff.returncode != 0
except Exception as e:
    print(f"检查工作区更改时出错: {e}")
    exit(1)

if has_working_changes:
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("工作区有更改，已执行 git add。")
    except subprocess.CalledProcessError as e:
        print(f"git add 失败: {e}")
        exit(1)
else:
    print("工作区没有新的更改，无需执行 git add。")

try:
    # 检查暂存区是否有需要 commit 的更改
    index_diff = subprocess.run(['git', 'diff', '--cached', '--quiet'], check=False)
    has_index_changes = index_diff.returncode != 0
except Exception as e:
    print(f"检查暂存区更改时出错: {e}")
    exit(1)

commit_message = "脚本自动提交"

if has_index_changes:
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("提交成功。")
    except subprocess.CalledProcessError as e:
        print(f"git commit 失败: {e}")
        exit(1)
else:
    print("暂存区没有新的更改，无需提交。")

try:
    # 获取当前分支名
    branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                   capture_output=True, text=True, check=True)
    current_branch = branch_result.stdout.strip()

    # 从远程仓库获取最新信息
    subprocess.run(['git', 'fetch'], check=True)

    # 比较当前分支与远程 AIdiy 分支是否有差异
    diff_result = subprocess.run(['git', 'diff', '--quiet', 'origin/AIdiy'], check=False)
    is_different = diff_result.returncode != 0

    if is_different:
        try:
            subprocess.run(['git', 'push', 'origin', f'HEAD:AIdiy'], check=True)
            print("推送成功！")
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode() if e.stderr else ""
            if "merge conflict" in error_output.lower() or "conflict" in error_output.lower():
                print("git push 失败，检测到合并冲突。")
                print("请手动合并分支解决冲突后再尝试推送。")
            else:
                print(f"git push 操作失败，原因如下: {error_output}")
    else:
        print("本地仓库与远程 AIdiy 分支无差异，无需推送。")

except subprocess.CalledProcessError as e:
    error_output = e.stderr.decode() if e.stderr else ""
    print(f"执行本地更新操作失败，原因如下: {error_output}")