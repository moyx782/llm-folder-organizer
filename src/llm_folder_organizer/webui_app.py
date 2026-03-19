from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

try:
    from .config import AppConfig
    from .llm import DeepSeekLLM
    from .organize import organize
except ImportError:  # Allow running via `streamlit run` on the file path.
    src_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(src_root))
    from llm_folder_organizer.config import AppConfig
    from llm_folder_organizer.llm import DeepSeekLLM
    from llm_folder_organizer.organize import organize

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def _load_text(p: str) -> str:
    return Path(p).read_text(encoding="utf-8")


def main() -> None:
    if load_dotenv is not None:
        load_dotenv()
    st.set_page_config(page_title="LLM Folder Organizer", layout="wide")
    st.title("LLM Folder Organizer (WebUI)")

    with st.sidebar:
        st.header("配置")
        folder = st.text_input("目标文件夹路径", value=str(Path.home()))
        config_path = st.text_input("config 路径", value="configs/default.json")
        system_prompt_path = st.text_input("system prompt 路径", value="prompts/classify_file.system.txt")
        user_prompt_path = st.text_input("user prompt 路径", value="prompts/classify_file.user.txt")

        st.divider()
        st.subheader("API 配置")
        api_key_input = st.text_input(
            "API Key（留空使用环境变量）",
            value="",
            type="password",
            help="支持 DeepSeek 或 OpenAI 的 API Key"
        )
        
        st.divider()
        st.subheader("可选覆盖")
        base_url = st.text_input("base_url（留空用配置/环境变量）", value="")
        model = st.text_input("model（留空用配置/环境变量）", value="")

        st.divider()
        apply = st.checkbox("执行移动（Apply）", value=False)
        confirm = st.checkbox("我已理解：Apply 会移动文件", value=False, disabled=not apply)

        run_btn = st.button("开始运行", type="primary")

    st.caption("建议先不勾选 Apply 进行预览；确认分类无误后再执行移动。")

    if not run_btn:
        st.stop()

    # Validate
    root = Path(folder).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        st.error(f"不是有效目录：{root}")
        st.stop()

    if apply and not confirm:
        st.warning("请先勾选“我已理解：Apply 会移动文件”再执行。")
        st.stop()

    try:
        cfg = AppConfig.load(config_path)
    except Exception as e:
        st.error(f"读取配置失败：{e}")
        st.stop()

    final_base_url = (base_url.strip() or os.getenv("DEEPSEEK_BASE_URL") or cfg.base_url)
    final_model = (model.strip() or os.getenv("DEEPSEEK_MODEL") or cfg.model)

    api_key = api_key_input.strip() or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("缺少 API Key：请在上方输入框填写，或设置环境变量 DEEPSEEK_API_KEY / OPENAI_API_KEY")
        st.stop()

    try:
        system_prompt = _load_text(system_prompt_path)
        user_prompt = _load_text(user_prompt_path)
    except Exception as e:
        st.error(f"读取 prompt 失败：{e}")
        st.stop()

    llm = DeepSeekLLM(api_key=api_key, base_url=final_base_url, model=final_model)

    with st.spinner("处理中..."):
        res = organize(
            root=root,
            llm=llm,
            system_prompt=system_prompt,
            user_prompt_tmpl=user_prompt,
            max_bytes=cfg.max_bytes,
            preview_chars=cfg.preview_chars,
            apply=apply,
            dry_run=not apply,
        )

    st.success(f"完成：共处理 {len(res)} 个文件。")

    # Render table
    rows = []
    for src, dst, r in res:
        rows.append(
            {
                "action": "MOVE" if apply else "PLAN",
                "file": src.name,
                "category": dst.parent.name,
                "confidence": float(r.confidence),
                "reason": r.reason,
            }
        )

    st.dataframe(rows, use_container_width=True)

    if apply:
        st.info("已执行移动。若需撤销建议：在正式使用前加入“操作日志/撤销”功能（后续可加）。")


if __name__ == "__main__":
    main()
