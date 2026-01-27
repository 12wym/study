#!/usr/bin/env python3
# 简化版 - assets 放在当前目录
import os
import re
import shutil
from pathlib import Path

def convert_obsidian_in_current_dir():
    """在当前目录执行转换"""
    current_dir = Path.cwd()
    assets_dir = current_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    print(f"工作目录: {current_dir}")
    print(f"Assets 目录: {assets_dir}")
    print("-" * 40)
    
    # 处理所有 .md 文件
    for md_file in current_dir.glob("*.md"):
        print(f"处理: {md_file.name}")
        
        # 读取内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建文档专属目录
        doc_name = md_file.stem.replace(' ', '_')
        doc_assets = assets_dir / doc_name
        doc_assets.mkdir(exist_ok=True)
        
        # 查找并替换 ![[图片]] 引用
        def replace_image(match):
            img_name = match.group(1)
            # 清理文件名
            clean_name = img_name.replace(' ', '_')
            
            # 在当前目录查找图片
            for file in current_dir.glob("*"):
                if file.is_file() and (file.name == img_name or file.name.replace(' ', '_') == clean_name):
                    # 复制到 assets
                    target = doc_assets / clean_name
                    if not target.exists():
                        shutil.copy2(file, target)
                    
                    # 生成相对路径
                    rel_path = f"./assets/{doc_name}/{clean_name}"
                    return f"![]({rel_path})"
            
            # 如果没找到，返回清理后的文件名
            return f"![]({clean_name})"
        
        # 执行替换
        pattern = r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp))\]\]'
        new_content = re.sub(pattern, replace_image, content, flags=re.IGNORECASE)
        
        # 保存（先备份）
        if new_content != content:
            backup = md_file.with_suffix('.backup')
            if not backup.exists():
                shutil.copy2(md_file, backup)
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✓ 已更新")
    
    print("\n完成！")
    print(f"所有图片保存在: {assets_dir}")

if __name__ == "__main__":
    convert_obsidian_in_current_dir()
    input("按 Enter 退出...")