def add_git(*file_list):
    subprocess.run(['git', 'add', *file_list], check=True)