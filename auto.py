import subprocess
import os

# 检查当前目录是否为 Git 仓库
target_dir = '/Users/Kai/AIdiy'
os.chdir(target_dir)

if not os.path.isdir('.git'):
    print("脚本内置目标目录不是 Git 仓库，请修改脚本切换到正确的目录。")
    exit(1)

try:
    # 检查工作区是否有更改（未暂存更改）
    wt_diff = subprocess.run(['git', 'diff', '--quiet'], check=False)
    has_working_changes = wt_diff.returncode != 0
    #has_working_changes = False
except Exception as e:
    print(f"检查工作区更改时出错: {e}")
    exit(1)

if has_working_changes:
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("工作区有更改，已执行 git add。")
    except subprocess.CalledProcessError as e:
        try:
            error_output = e.stderr.decode() if e.stderr else ""
        except Exception:
            error_output = str(e)
        if not error_output:
            error_output = str(e)
        print(f"执行更新操作失败，原因如下: {error_output}")
        exit(1)
else:
    print("工作区没有新的更改，无需执行 git add。")

try:
    # 检查暂存区是否有需要 commit 的更改
    index_diff = subprocess.run(['git', 'diff', '--staged', '--quiet'], check=False)
    has_index_changes = index_diff.returncode != 0
except Exception as e:
    print(f"检查暂存区更改时出错: {e}")
    exit(1)

commit_message = "AutoCommit"

if has_index_changes:
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("本地提交成功。")
    except subprocess.CalledProcessError as e:
        try:
            error_output = e.stderr.decode() if e.stderr else ""
        except Exception:
            error_output = str(e)
        if not error_output:
            error_output = str(e)
        print(f"执行更新操作失败，原因如下: {error_output}")
        exit(1)
else:
    print("暂存区没有新的更改，无需执行git commit")
    
print("即将开始向远程仓库推送")
# 检查远程仓库是否存在
try:
    remotes = subprocess.run(['git', 'remote'], capture_output=True, text=True, check=True)
    if 'AIdiy' not in remotes.stdout.splitlines():
        print("远程仓库 'AIdiy' 不存在，请检查配置。")
        exit(1)
except subprocess.CalledProcessError as e:
    try:
        error_output = e.stderr.decode() if e.stderr else ""
    except Exception:
        error_output = str(e)
    if not error_output:
        error_output = str(e)
    print(f"执行更新操作失败，原因如下: {error_output}")
    exit(1)

try:
    # 获取当前分支名
    branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                   capture_output=True, text=True, check=True)
    current_branch = branch_result.stdout.strip()

    # 从远程仓库获取最新信息
    subprocess.run(['git', 'fetch', 'AIdiy'], check=True)

    try:
        subprocess.run(['git', 'push'], check=True)
        print("推送成功！")
    except subprocess.CalledProcessError as e:
        try:
            error_output = e.stderr.decode() if e.stderr else ""
        except Exception:
            error_output = str(e)
        if not error_output:
            error_output = str(e)
        if "merge conflict" in error_output.lower() or "conflict" in error_output.lower():
            print("git push 失败，检测到合并冲突。")
            print("请手动合并分支解决冲突后再尝试推送。")
        else:
            print(f"执行更新操作失败，原因如下: {error_output}")
except subprocess.CalledProcessError as e:
    try:
        error_output = e.stderr.decode() if e.stderr else ""
    except Exception:
        error_output = str(e)
    if not error_output:
        error_output = str(e)
    print(f"执行更新操作失败，原因如下: {error_output}")