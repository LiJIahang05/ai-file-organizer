# -*- coding: utf-8 -*-
"""
第 1 周 · 第 2 步：AI 批量摘要器
------------------------------------------------
作用：把一个文件夹里的所有 .txt / .md 文件，逐个丢给 DeepSeek，让它写一段中文摘要，
      最后汇总输出到一个 summary.md 文件里。

跑之前要做三件事：
    1. 装库（只需做一次）：  pip install openai
    2. 申请 API key：        https://platform.deepseek.com  → API Keys → 创建
    3. 填 key：              把下面 API_KEY 那行的 "在这里粘贴你的key" 换成你的 key

怎么用：
    python step2_summary.py "要处理的文件夹路径"

输出：
    在该文件夹里生成一个 summary.md，里面有每个文件的摘要。
"""

import os
import sys

# ⚠️ 把引号里的内容换成你自己的 key（不要加空格）
API_KEY = "你的key"

# DeepSeek 的接口地址（官方固定值，不要改）
BASE_URL = "https://api.deepseek.com"

# 模型名。官方当前可选：deepseek-v4-flash（便宜、快）/ deepseek-v4-pro（强、贵）
MODEL = "deepseek-v4-flash"

# 你希望 AI 怎么总结。可以自己改这句话，这是这个工具"值钱"的地方
提示词模板 = """
请用中文写一段 100 字以内的摘要，说明这份资料讲了什么、有什么用。
要求：直接说重点，不要写"本文介绍了"这种套话。

资料内容如下：
{内容}
"""


def 读文件(路径):
    try:
        with open(路径, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"（读取失败：{e}）"


def 调AI(文本):
    from openai import OpenAI

    客户端 = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 太长的内容截断，省钱也防报错（最多送 6000 字）
    if len(文本) > 6000:
        文本 = 文本[:6000] + "\n（内容过长，已截断）"

    回应 = 客户端.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": 提示词模板.format(内容=文本)},
        ],
        stream=False,
    )
    return 回应.choices[0].message.content.strip()


def 主程序(目标文件夹):
    if API_KEY == "在这里粘贴你的key":
        print("❌ 你还没填 API key。打开本文件，改第 19 行的 API_KEY。")
        return
    if not os.path.isdir(目标文件夹):
        print(f"❌ 文件夹不存在：{目标文件夹}")
        return

    # 找出所有 txt / md 文件
    文件列表 = []
    for f in os.listdir(目标文件夹):
        if f.startswith("."):
            continue
        if f.lower() == "summary.md":
            continue
        if f.lower().endswith((".txt", ".md")):
            文件列表.append(os.path.join(目标文件夹, f))

    
    

    if not 文件列表:
        print("这个文件夹里没有 .txt 或 .md 文件。先放几个进去再跑。")
        return

    print(f"📂 找到 {len(文件列表)} 个文件，开始处理...\n")

    结果 = ["# 资料摘要汇总\n", f"> 共 {len(文件列表)} 份资料，由 DeepSeek 自动生成\n"]

    for 序号, 路径 in enumerate(文件列表, 1):
        文件名 = os.path.basename(路径)
        print(f"  [{序号}/{len(文件列表)}] 正在处理：{文件名}")

        内容 = 读文件(路径)
        if not 内容.strip():
            摘要 = "（空文件）"
        else:
            try:
                摘要 = 调AI(内容)
            except Exception as e:
                摘要 = f"（调用失败：{e}）"

        print(f"      -> {摘要[:40]}...\n")
        结果.append(f"\n## {文件名}\n\n{摘要}\n")

    输出路径 = os.path.join(目标文件夹, "summary.md")
    with open(输出路径, "w", encoding="utf-8") as f:
        f.write("\n".join(结果))

    print(f"✅ 完成！摘要已写到：{输出路径}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python step2_summary.py \"要处理的文件夹路径\"")
        sys.exit(1)
    主程序(sys.argv[1])
