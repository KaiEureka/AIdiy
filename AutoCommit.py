import subprocess

def auto_commit(commit_message):
    try:
        # 执行 git add . 命令
        subprocess.run(['git', 'add', '.'], check=True)
        # 执行 git commit -m "commit_message" 命令
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("提交成功！")
    except subprocess.CalledProcessError as e:
        print(f"提交失败: {e}")

if __name__ == "__main__":
    message = input("请输入提交信息: ")
    auto_commit(message)
