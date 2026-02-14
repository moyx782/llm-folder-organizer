# LLM Folder Organizer

一个基于 LLM（DeepSeek / OpenAI 兼容 API）的文件夹整理工具：扫描目标目录 -> 读取文件名/少量内容预览 -> 让模型输出结构化 JSON 分类 -> 生成/选择目标子目录 -> 移动或仅预览。

## 目录结构
- `src/llm_folder_organizer/`：核心代码
- `configs/`：配置文件（示例）
- `prompts/`：提示词模板
- `tests/`：测试
- `scripts/`：开发/打包脚本

## 快速开始
1) 安装依赖
```bash
pip install -e .
```

2) 配置环境变量（推荐）
```bash
export DEEPSEEK_API_KEY="your_key"
```

3) 干跑（只打印）
```bash
lfo scan /path/to/folder
```

4) 应用（移动文件）
```bash
lfo scan /path/to/folder --apply
```

## 安全建议
- 默认使用 `--dry-run`（未加 `--apply`）不会移动任何文件。
- 建议先在小文件夹试运行。
- 重要目录（如系统目录）请不要直接操作。

## GUI
需要系统自带 Tkinter（多数 Python 安装默认包含）。
启动 GUI：
```bash
lfo gui
```
或者：
```bash
python -m llm_folder_organizer.cli gui
```

## WebUI（推荐）
使用 Streamlit 提供浏览器界面。

安装依赖：
```bash
pip install -e .
```

启动 WebUI：
```bash
lfo web
```
或指定端口：
```bash
lfo web --host 127.0.0.1 --port 8501
```

然后在浏览器打开：
- http://127.0.0.1:8501

> WebUI 会从当前终端环境读取 `DEEPSEEK_API_KEY`。
> 建议先不勾选 Apply 做预览，确认无误后再勾选 Apply 执行移动。

## 打包（无需 Python 环境运行）
使用 PyInstaller 生成独立可执行文件。**跨平台需要在各自系统上分别构建**。

> **macOS 用户注意：** Intel Mac 和 Apple Silicon (M1/M2/M3) Mac 需要分别构建对应架构的可执行文件。

1) 安装打包工具
```bash
pip install pyinstaller
```

2) 构建 WebUI 可执行文件
```bash
bash scripts/build_webui.sh
```

3) 运行
- macOS/Linux: `dist/lfo-webui`
- Windows: `dist/lfo-webui.exe`

可选环境变量：
```bash
export LFO_HOST=127.0.0.1
export LFO_PORT=8501
export DEEPSEEK_API_KEY=your_key
```

## Standalone（无需 Python 环境）

你可以用 PyInstaller 把 WebUI 打包成可执行文件，使目标机器无需安装 Python 也能运行。

- 构建说明见：`BUILD.md`
- 本地一键构建脚本：
  - macOS/Linux：`bash scripts/build_local.sh`
  - Windows：`powershell -ExecutionPolicy Bypass -File scripts/build_local.ps1`

GitHub Actions 自动构建：
- push tag（例如 `v0.1.0`）会触发 `.github/workflows/build-standalone.yml`，生成多个平台的 artifacts：
  - Windows x64
  - Linux x64  
  - macOS Intel (x64)
  - macOS Apple Silicon (ARM64)
