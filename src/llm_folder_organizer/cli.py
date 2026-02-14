from __future__ import annotations

import argparse
import os
from pathlib import Path

from .config import AppConfig
from .llm import DeepSeekLLM
from .organize import organize

# Optional GUIs:
try:
    from .gui import run_gui  # type: ignore
except Exception:
    run_gui = None  # type: ignore

from .webui import run_webui

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(prog="lfo", description="LLM Folder Organizer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="scan and (optionally) organize a folder")
    p_scan.add_argument("folder", type=str, help="target folder path")
    p_scan.add_argument("--config", type=str, default="configs/default.json", help="config json path")
    p_scan.add_argument("--system-prompt", type=str, default="prompts/classify_file.system.txt")
    p_scan.add_argument("--user-prompt", type=str, default="prompts/classify_file.user.txt")
    p_scan.add_argument("--apply", action="store_true", help="actually move files")
    p_scan.add_argument("--yes", action="store_true", help="skip confirmation (use with --apply)")
    p_scan.add_argument("--model", type=str, default=None, help="override model (e.g., deepseek-chat)")
    p_scan.add_argument("--base-url", type=str, default=None, help="override base_url (e.g., https://api.deepseek.com)")

    p_web = sub.add_parser("web", help="launch WebUI (Streamlit)")
    p_web.add_argument("--host", type=str, default="127.0.0.1")
    p_web.add_argument("--port", type=int, default=8501)

    p_gui = sub.add_parser("gui", help="launch GUI (Tkinter, optional)")

    args = parser.parse_args()

    if load_dotenv is not None:
        load_dotenv()

    if args.cmd == "web":
        raise SystemExit(run_webui(host=args.host, port=args.port))

    if args.cmd == "gui":
        if run_gui is None:
            raise SystemExit("Tkinter GUI unavailable in this environment. Use `lfo web` instead.")
        run_gui()
        return

    if args.cmd == "scan":
        root = Path(args.folder).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            raise SystemExit(f"Not a directory: {root}")

        cfg = AppConfig.load(args.config)
        base_url = args.base_url or os.getenv("DEEPSEEK_BASE_URL") or cfg.base_url
        model = args.model or os.getenv("DEEPSEEK_MODEL") or cfg.model
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("Missing DEEPSEEK_API_KEY (or OPENAI_API_KEY) env var")

        system_prompt = load_text(Path(args.system_prompt))
        user_prompt = load_text(Path(args.user_prompt))

        llm = DeepSeekLLM(api_key=api_key, base_url=base_url, model=model)

        if args.apply and not args.yes:
            print("⚠️  --apply 会移动文件。若确定继续，请加上 --yes。\n例如：lfo scan <folder> --apply --yes")
            return

        dry_run = not args.apply
        res = organize(
            root=root,
            llm=llm,
            system_prompt=system_prompt,
            user_prompt_tmpl=user_prompt,
            max_bytes=cfg.max_bytes,
            preview_chars=cfg.preview_chars,
            apply=args.apply,
            dry_run=dry_run,
        )

        for src, dst, r in res:
            action = "MOVE" if args.apply else "PLAN"
            print(f"{action}\t{src.name} -> {dst.parent.name}/\t(conf={r.confidence:.2f})\t{r.reason}")
