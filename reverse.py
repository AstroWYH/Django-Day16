import os

def reverse_name(name):
    """将文件名（不包括扩展名）完全颠倒"""
    return name[::-1]

def reverse_file_names(directory):
    """递归将目录下的所有文件名颠倒，排除 .git 目录"""
    for root, dirs, files in os.walk(directory):
        # 排除 .git 目录
        if '.git' in root.split(os.sep):
            continue
        for filename in files:
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            if not ext:  # 如果没有扩展名，直接颠倒整个文件名
                new_name = reverse_name(name)
            else:
                new_name = reverse_name(name) + ext
            # 重命名文件
            os.rename(os.path.join(root, filename), os.path.join(root, new_name))

def restore_file_names(directory):
    """递归将目录下的所有文件名还原，排除 .git 目录"""
    for root, dirs, files in os.walk(directory):
        # 排除 .git 目录
        if '.git' in root.split(os.sep):
            continue
        for filename in files:
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            if not ext:  # 如果没有扩展名，直接颠倒整个文件名
                original_name = reverse_name(name)
            else:
                original_name = reverse_name(name) + ext
            # 重命名文件
            os.rename(os.path.join(root, filename), os.path.join(root, original_name))

# 示例用法
folder_path = r"E:\pycharm\pyweb\day16"

# 颠倒文件名
reverse_file_names(folder_path)

# 还原文件名
# restore_file_names(folder_path)