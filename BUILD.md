# Standalone Build (No Python Required on Target)

本项目可以用 **PyInstaller** 打包成一个“自带 Python 运行时”的可执行文件。
打包后的程序在目标机器上 **无需安装 Python** 也能运行（但仍需要联网访问 API）。

> 注意：可执行文件 **跨平台不可通用**。  
> 你需要分别在 Windows / macOS / Linux 上各自打包一次。
> 
> **macOS 注意事项：**
> - macOS Intel (x64): 在 Intel Mac 上构建（任何 macOS 版本均可）
> - macOS Apple Silicon (ARM64): 在 M1/M2/M3/M4 Mac 上构建（任何 macOS 版本均可）
> - 两种架构的可执行文件不通用，取决于 CPU 架构而非 macOS 版本

## 本地打包（macOS/Linux）

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel

# 安装运行依赖
pip install .

# 安装打包依赖
pip install pyinstaller

# 执行打包（WebUI）
pyinstaller build/pyinstaller.spec
```

产物在：
- `dist/lfo-webui/`（目录模式）
- 运行：`./dist/lfo-webui/lfo-webui`

## 本地打包（Windows PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel

pip install .
pip install pyinstaller

pyinstaller build\pyinstaller.spec
```

运行：
- `dist\lfo-webui\lfo-webui.exe`

## 环境变量

运行可执行文件前需设置：
- `DEEPSEEK_API_KEY`（必填）
- 可选：`DEEPSEEK_BASE_URL`，`DEEPSEEK_MODEL`

可选：调整 WebUI 绑定地址/端口
- `LFO_HOST`（默认 127.0.0.1）
- `LFO_PORT`（默认 8501）

## GitHub Actions 自动构建

仓库内已提供 `.github/workflows/build-standalone.yml`，
会在 push tag 时分别构建 Windows / macOS (x64 + ARM64) / Linux 产物并上传为 artifacts。

**产物包含：**
- Windows x64
- Linux x64
- macOS Intel (x64) - 适用于 Intel Mac
- macOS Apple Silicon (ARM64) - 适用于 M1/M2/M3/M4 Mac

> **GitHub Actions 说明：**  
> - `macos-13` runner 使用 Intel x64 架构
> - `macos-14` runner 使用 Apple Silicon ARM64 架构
> - 这确保了 CI/CD 能够为两种架构分别构建原生可执行文件
