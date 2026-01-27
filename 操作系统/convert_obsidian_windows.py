#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 专用 Obsidian 图片引用转换工具
解决 Windows 路径和编码问题
"""

import os
import re
import shutil
import sys
from pathlib import Path, PureWindowsPath
import hashlib
import traceback

def sanitize_windows_filename(filename):
    """清理 Windows 文件名中的非法字符"""
    # Windows 文件名中不能包含的字符: <>:"/\|?*
    illegal_chars = r'<>:"/\\|\?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    
    # 去掉开头和结尾的空格和点
    filename = filename.strip(' .')
    
    # Windows 保留文件名
    reserved_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    
    name_without_ext = os.path.splitext(filename)[0].upper()
    if name_without_ext in reserved_names:
        filename = f"_{filename}"
    
    return filename

def get_file_hash(file_path):
    """计算文件的 MD5 哈希值，用于检测重复图片"""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read(65536)  # 只读取前64KB，提高速度
            hasher.update(buf)
            # 对于大文件，可以读取更多部分
            while len(buf) == 65536:
                buf = f.read(65536)
                hasher.update(buf)
    except Exception as e:
        print(f"  计算哈希错误 {file_path}: {e}")
        return None
    return hasher.hexdigest()

def create_unique_filename(target_dir, filename):
    """在目标目录中创建唯一的文件名，避免覆盖"""
    # 清理文件名
    filename = sanitize_windows_filename(filename)
    
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while (target_dir / new_filename).exists():
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return new_filename

def find_image_file(md_file, image_name):
    """在文档所在目录及其子目录中查找图片文件"""
    # Windows 路径不区分大小写，但 Python 区分，需要特殊处理
    search_dirs = [
        md_file.parent,  # 文档所在目录
        md_file.parent / "attachments",
        md_file.parent / "assets",
        md_file.parent / "images",
        md_file.parent.parent / "assets",  # 上一级的assets文件夹
    ]
    
    # 首先尝试精确匹配
    for search_dir in search_dirs:
        if search_dir.exists():
            for file in search_dir.rglob("*"):
                if file.name.lower() == image_name.lower():
                    return file
    
    # 如果没有找到，递归搜索整个文档目录
    for root, dirs, files in os.walk(md_file.parent):
        for file in files:
            if file.lower() == image_name.lower():
                return Path(root) / file
    
    return None

def normalize_windows_path(path_str):
    """标准化 Windows 路径，确保使用正斜杠"""
    # 将反斜杠转换为正斜杠，用于 Markdown 中的路径
    return path_str.replace('\\', '/')

def process_markdown_file(md_file, assets_base_dir):
    """处理单个 Markdown 文件"""
    try:
        # 使用 UTF-8 编码读取，处理中文等特殊字符
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 如果 UTF-8 失败，尝试其他编码
        try:
            with open(md_file, 'r', encoding='gbk') as f:
                content = f.read()
        except Exception as e:
            print(f"  无法读取文件 {md_file}: {e}")
            return content, []
    
    # 查找所有 ![[图片]] 引用
    # 支持带空格的图片名
    pattern = r'!\[\[([^\]]+?\.(?:png|jpg|jpeg|gif|bmp|svg|webp|tiff))\]\]'
    matches = re.findall(pattern, content, re.IGNORECASE)
    
    if not matches:
        return content, []
    
    # 为当前文档创建专门的图片文件夹
    # 清理文档名，确保文件夹名合法
    doc_name = sanitize_windows_filename(md_file.stem)
    
    # 如果文档名太长，截断
    if len(doc_name) > 50:
        doc_name = doc_name[:50] + "_" + hashlib.md5(doc_name.encode()).hexdigest()[:8]
    
    doc_assets_dir = assets_base_dir / doc_name
    doc_assets_dir.mkdir(exist_ok=True)
    
    # 收集需要复制的图片信息
    images_to_copy = []
    processed_images = {}  # 记录已处理的图片，避免重复
    
    # 替换内容
    def replace_callback(match):
        original_ref = match.group(0)
        image_name = match.group(1).strip()  # 去除可能的空格
        
        # 如果已经处理过相同的图片，直接使用之前的路径
        if image_name in processed_images:
            return processed_images[image_name]
        
        print(f"  查找图片: {image_name}")
        image_found = find_image_file(md_file, image_name)
        
        if not image_found:
            print(f"  ⚠ 未找到图片文件: {image_name}")
            # 如果找不到，保持原样但转换为标准语法
            processed_images[image_name] = f"![]({image_name})"
            return processed_images[image_name]
        
        # 计算图片哈希，检查是否已存在
        img_hash = get_file_hash(image_found)
        if img_hash is None:
            # 哈希计算失败，仍然复制
            img_hash = "unknown"
        
        # 检查在文档的assets文件夹中是否已有相同图片
        target_image_name = create_unique_filename(doc_assets_dir, image_name)
        target_path = doc_assets_dir / target_image_name
        
        # 检查是否需要复制
        copy_needed = True
        if target_path.exists():
            existing_hash = get_file_hash(target_path)
            if existing_hash and existing_hash == img_hash:
                copy_needed = False
                print(f"  跳过重复图片: {image_name}")
        
        if copy_needed:
            try:
                shutil.copy2(image_found, target_path)
                images_to_copy.append({
                    'source': image_found,
                    'target': target_path,
                    'name_in_doc': image_name
                })
                print(f"  复制图片: {image_found.name}")
            except Exception as e:
                print(f"  复制图片失败 {image_found}: {e}")
                processed_images[image_name] = f"![]({image_name})"
                return processed_images[image_name]
        
        # 生成相对路径（使用正斜杠）
        relative_path = normalize_windows_path(f"./assets/{doc_name}/{target_image_name}")
        
        new_ref = f"![]({relative_path})"
        processed_images[image_name] = new_ref
        return new_ref
    
    # 执行替换
    try:
        new_content = re.sub(pattern, replace_callback, content, flags=re.IGNORECASE)
    except Exception as e:
        print(f"  正则替换失败: {e}")
        return content, []
    
    return new_content, images_to_copy

def main():
    # 显示友好的 Windows 界面
    print("=" * 60)
    print("Windows Obsidian 图片转换工具")
    print("=" * 60)
    
    # 配置
    if len(sys.argv) > 1:
        source_dir = Path(sys.argv[1])
    else:
        # 获取当前脚本所在目录
        script_dir = Path(__file__).parent
        print(f"未指定目录，将处理当前目录: {script_dir}")
        print("或者输入要处理的目录路径: ", end="")
        user_input = input().strip()
        if user_input:
            source_dir = Path(user_input)
        else:
            source_dir = script_dir
    
    # 检查目录是否存在
    if not source_dir.exists():
        print(f"错误：目录不存在: {source_dir}")
        print("按 Enter 退出...")
        input()
        return
    
    # 创建assets文件夹（与source_dir同级）
    assets_base_dir = source_dir.parent / "assets"
    try:
        assets_base_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"创建 assets 文件夹失败: {e}")
        print("按 Enter 退出...")
        input()
        return
    
    print(f"处理目录: {source_dir}")
    print(f"图片将保存到: {assets_base_dir}")
    print("-" * 60)
    
    # 统计信息
    total_files = 0
    total_images = 0
    converted_files = 0
    
    # 收集所有.md文件
    md_files = list(source_dir.rglob("*.md")) + list(source_dir.rglob("*.markdown"))
    
    if not md_files:
        print("未找到 .md 或 .markdown 文件")
        print("按 Enter 退出...")
        input()
        return
    
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print("开始处理...\n")
    
    for md_file in md_files:
        total_files += 1
        relative_path = md_file.relative_to(source_dir)
        print(f"[{total_files}/{len(md_files)}] 处理: {relative_path}")
        
        try:
            # 跳过备份文件
            if md_file.suffixes[-1] == '.backup' or '.obsidian_backup' in md_file.name:
                print("  跳过备份文件")
                continue
            
            # 处理文件
            new_content, images_to_copy = process_markdown_file(md_file, assets_base_dir)
            
            if images_to_copy:
                # 实际上复制已经在处理函数中完成
                total_images += len(images_to_copy)
                
                # 保存修改后的内容
                backup_file = md_file.with_suffix(md_file.suffix + '.obsidian_backup')
                try:
                    if not backup_file.exists():
                        shutil.copy2(md_file, backup_file)
                        print(f"  已创建备份: {backup_file.name}")
                    
                    # 确保使用 UTF-8 编码写入
                    with open(md_file, 'w', encoding='utf-8', newline='') as f:
                        f.write(new_content)
                    
                    converted_files += 1
                    print(f"  ✓ 转换完成，处理 {len(images_to_copy)} 张图片")
                except Exception as e:
                    print(f"  保存文件失败: {e}")
            
            else:
                # 检查是否有图片引用但未找到文件
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if re.search(r'!\[\[[^\]]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp|tiff)\]\]', content, re.IGNORECASE):
                    print(f"  ⚠  发现图片引用但未找到对应文件")
                else:
                    print(f"  无图片引用，跳过")
        
        except Exception as e:
            print(f"  错误: {e}")
            traceback.print_exc()
            continue
    
    print("\n" + "=" * 60)
    print("转换完成！")
    print(f"扫描文件数: {total_files}")
    print(f"转换文件数: {converted_files}")
    print(f"处理图片数: {total_images}")
    print(f"图片存放位置: {assets_base_dir}")
    
    # 显示统计信息
    if converted_files > 0:
        print(f"备份文件: *.md.obsidian_backup")
        print("\n转换后的图片结构:")
        
        # 显示 assets 目录结构
        if assets_base_dir.exists():
            for item in sorted(assets_base_dir.iterdir()):
                if item.is_dir():
                    image_count = len([f for f in item.glob("*") if f.is_file()])
                    print(f"  {item.name}/ ({image_count} 张图片)")
    
    print("\n注意事项:")
    print("1. 原始文件已备份为 .obsidian_backup 文件")
    print("2. 图片路径已转换为相对路径，适合 Git 和网页使用")
    print("3. 建议在 VSCode 中打开确认转换结果")
    
    # 保持窗口打开
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()