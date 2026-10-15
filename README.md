# AI 资料整理器

下载文件夹堆了上百个文件，一个学期没整理过；课程资料存了一堆，根本没时间看。

所以我做了这个小工具，让它干两件事：

1. **step1_sort.py** —— 把乱糟糟的文件夹按文件类型自动归类（图片 / 文档 / 视频 / 代码 / 安装包 / 压缩包）
2. **step2_summary.py** —— 把里面的文字资料交给 AI，自动生成中文摘要，汇总到一个 `summary.md` 里

## 怎么用

### 准备

- Python 3.13 以上（装的时候记得勾上 `Add Python to PATH`）
- step2 需要 DeepSeek 的 API key，在 <https://platform.deepseek.com> 申请
- 装依赖：`pip install openai`

### step1：整理文件夹

```bash
python step1_sort.py "要整理的文件夹路径"
```

默认是**预览模式**——只显示"这个文件会去哪"，不动你的文件。确认没问题后，把脚本里的 `DRY_RUN` 改成 `False` 再跑一次，才会真的整理。

### step2：生成 AI 摘要

```bash
python step2_summary.py "要处理的文件夹路径"
```

跑之前把脚本里 `API_KEY` 那行换成你自己的 key。跑完会在该文件夹里生成 `summary.md`，里面有每份资料的中文摘要。

## 几个安全措施

- 自动跳过隐藏文件、`desktop.ini`、Office 临时文件（`~$` 开头），不会搬走系统文件
- 同名文件自动改名，不会覆盖
- step2 会跳过自己生成的 `summary.md`，不会自己总结自己

## 关于这个项目

这是我人生第一个做完并且敢发出去的东西。代码很粗糙，功能也很小，但它是能跑的。

下一步打算加：批量处理 PDF、把摘要自动发到邮箱、做个图形界面。

作者是个大二学生，正在学 Python 和 AI，欢迎骂。
