# -*- coding: utf-8 -*-
"""
第 1 周 · 第 1 步：下载文件夹自动归位器
------------------------------------------------
作用：把一个乱糟糟的文件夹（比如"下载"）里的文件，按类型自动分到子文件夹里。
不需要联网、不需要 API key、不需要装任何第三方库。纯 Python 自带功能。

怎么用：
    python step1_sort.py "C:/Users/你的用户名/Downloads"          ← 预览（不动文件）
    python step1_sort.py "C:/Users/你的用户名/Downloads" --run     ← 真的整理

它会做：
    图片 -> 图片/ 文件夹
    文档 -> 文档/ 文件夹
    视频 -> 视频/ 文件夹
    压缩包 -> 压缩包/ 文件夹
    代码 -> 代码/ 文件夹
    其他 -> 其他/ 文件夹

安全设计：不加 --run 就永远只是预览，不会动你的任何文件。
"""

import os
import sys
import shutil

# True = 只打印计划，不动文件（安全）；False = 真的移动文件
DRY_RUN = True

# 只有在命令里写了 --run，才真的动手。写完就把它从参数列表里删掉，
# 免得后面把它误当成文件夹路径。
if "--run" in sys.argv:
    DRY_RUN = False
    sys.argv.remove("--run")

# 类型 -> 目标文件夹名。可以自己加
RULES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "视频": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "音频": [".mp3", ".wav", ".m4a", ".flac", ".ogg"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".json", ".c", ".cpp", ".java", ".ipynb"],
    "安装包": [".exe", ".msi", ".dmg", ".apk"],
}


def 判断类型(文件名):
    """根据扩展名判断这个文件该去哪个文件夹"""
    扩展名 = os.path.splitext(文件名)[1].lower()
    for 文件夹名, 扩展名列表 in RULES.items():
        if 扩展名 in 扩展名列表:
            return 文件夹名
    return "其他"


def 主程序(目标文件夹):
    if not os.path.isdir(目标文件夹):
        print(f"❌ 这个文件夹不存在：{目标文件夹}")
        return

    print(f"📂 开始扫描：{目标文件夹}\n")
    统计 = {}

    for 文件名 in os.listdir(目标文件夹):
        完整路径 = os.path.join(目标文件夹, 文件名)

        # 跳过文件夹，只处理文件
        if not os.path.isfile(完整路径):
            continue
        # 跳过脚本自己，防止把自己移走
        if 文件名 == os.path.basename(__file__):
            continue
        # 跳过隐藏文件、Windows 系统文件（desktop.ini）、Office 临时文件（~$开头）
        if 文件名.startswith("."):
            continue
        if 文件名.lower() == "desktop.ini" or 文件名.startswith("~$"):
            continue

        目标子文件夹 = 判断类型(文件名)
        目标路径 = os.path.join(目标文件夹, 目标子文件夹)

        print(f"  {文件名}  ->  {目标子文件夹}/")

        if not DRY_RUN:
            os.makedirs(目标路径, exist_ok=True)
            # 如果同名文件已存在，自动在名字后加数字，避免覆盖
            最终路径 = os.path.join(目标路径, 文件名)
            if os.path.exists(最终路径):
                名字, 扩展 = os.path.splitext(文件名)
                编号 = 1
                while os.path.exists(最终路径):
                    最终路径 = os.path.join(目标路径, f"{名字}_{编号}{扩展}")
                    编号 += 1
            shutil.move(完整路径, 最终路径)

        统计[目标子文件夹] = 统计.get(目标子文件夹, 0) + 1

    print("\n📊 汇总：")
    for 文件夹名, 数量 in sorted(统计.items(), key=lambda x: -x[1]):
        print(f"  {文件夹名}: {数量} 个文件")

    if DRY_RUN:
        print("\n⚠️  上面只是预览，文件还没动。")
        print("    确认没问题后，在命令最后加 --run 再跑一次，就会真的整理。")
    else:
        print("\n✅ 整理完成！")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python step1_sort.py \"要整理的文件夹路径\"")
        print("例子：python step1_sort.py \"C:/Users/15638/Downloads\"")
        sys.exit(1)
    主程序(sys.argv[1])
