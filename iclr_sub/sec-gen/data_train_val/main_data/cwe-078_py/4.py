def execute_commit(commit_msg):
    subprocess.run(['git', 'commit', '-m', commit_msg])