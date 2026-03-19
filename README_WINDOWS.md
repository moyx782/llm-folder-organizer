# LLM Folder Organizer - Windows 便携版使用说明

## 🚀 快速开始

### 方式一：一键启动（推荐）

1. **双击运行** `启动.bat`
2. 等待自动安装依赖（首次运行需要 1-2 分钟）
3. 浏览器会自动打开 http://localhost:8501
4. 在左侧输入 API Key 即可使用

### 方式二：手动安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境
.venv\Scripts\activate.bat

# 安装
pip install -e .

# 启动
lfo web
```

## 🔑 API Key 配置

在 WebUI 左侧边栏的 **"API 配置"** 部分输入：
- **API Key**: 你的 DeepSeek API Key（或 OpenAI API Key）
- **base_url**: 可选，留空使用默认
- **model**: 可选，留空使用默认

支持两种 API：
- DeepSeek: `sk-...`
- OpenAI: `sk-...`

## 📁 使用步骤

1. **选择文件夹**: 输入要整理的目标文件夹路径
2. **配置 prompts**: 选择或创建分类提示词
3. **预览模式**: 先不勾选 "执行移动"，点击"开始运行"查看分类结果
4. **确认无误**: 勾选"执行移动"和确认框，再次运行完成整理

## ⚠️ 安全提示

- **默认是预览模式**，不会真的移动文件
- 重要文件请先备份
- 不要操作系统目录（如 C:\Windows）

## 🛠️ 故障排除

**问题：提示 "未检测到 Python"**
- 解决方案：安装 Python 3.9+ https://www.python.org/downloads/

**问题：安装依赖很慢**
- 解决方案：换用清华镜像 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`

**问题：端口被占用**
- 解决方案：修改 `启动.bat` 中的端口号（默认 8501）

## 📦 文件说明

```
llm_folder_organizer-0.1.0/
├── 启动.bat          # 一键启动脚本
├── start.bat         # 原版启动脚本
├── build.bat         # 打包脚本
├── run_webui.py      # 打包入口
├── src/              # 源代码
│   └── llm_folder_organizer/
├── configs/          # 配置文件
├── prompts/          # 提示词模板
└── README.md         # 本文件
```

## 💡 提示

- 整理前建议先用小文件夹测试
- 可以在 prompts 目录自定义分类规则
- 支持中文文件名和内容识别
