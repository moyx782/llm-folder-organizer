from __future__ import annotations

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .config import AppConfig
from .llm import DeepSeekLLM
from .organize import organize

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LLM Folder Organizer")
        self.geometry("820x520")

        self.folder_var = tk.StringVar(value=str(Path.home()))
        self.config_var = tk.StringVar(value="configs/default.json")
        self.system_prompt_var = tk.StringVar(value="prompts/classify_file.system.txt")
        self.user_prompt_var = tk.StringVar(value="prompts/classify_file.user.txt")
        self.apply_var = tk.BooleanVar(value=False)
        self.model_var = tk.StringVar(value="")
        self.base_url_var = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self) -> None:
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Row: folder
        row0 = ttk.Frame(frm)
        row0.pack(fill="x", pady=(0, 8))
        ttk.Label(row0, text="目标文件夹：").pack(side="left")
        ttk.Entry(row0, textvariable=self.folder_var).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(row0, text="选择...", command=self._pick_folder).pack(side="left")

        # Row: config & prompts
        row1 = ttk.Frame(frm)
        row1.pack(fill="x", pady=(0, 8))
        ttk.Label(row1, text="配置：").pack(side="left")
        ttk.Entry(row1, textvariable=self.config_var, width=26).pack(side="left", padx=6)
        ttk.Label(row1, text="System Prompt：").pack(side="left", padx=(14, 0))
        ttk.Entry(row1, textvariable=self.system_prompt_var, width=28).pack(side="left", padx=6)
        ttk.Label(row1, text="User Prompt：").pack(side="left", padx=(14, 0))
        ttk.Entry(row1, textvariable=self.user_prompt_var, width=28).pack(side="left", padx=6)

        # Row: overrides
        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=(0, 8))
        ttk.Label(row2, text="base_url 覆盖：").pack(side="left")
        ttk.Entry(row2, textvariable=self.base_url_var, width=40).pack(side="left", padx=6)
        ttk.Label(row2, text="model 覆盖：").pack(side="left", padx=(14, 0))
        ttk.Entry(row2, textvariable=self.model_var, width=24).pack(side="left", padx=6)
        ttk.Checkbutton(row2, text="移动文件（Apply）", variable=self.apply_var).pack(side="left", padx=(18, 0))

        # Row: buttons
        row3 = ttk.Frame(frm)
        row3.pack(fill="x", pady=(0, 8))
        ttk.Button(row3, text="开始扫描 / 预览", command=self._run_dry).pack(side="left")
        ttk.Button(row3, text="执行移动", command=self._run_apply).pack(side="left", padx=8)
        ttk.Label(row3, text="提示：建议先预览，再执行移动。").pack(side="left", padx=18)

        # Output
        self.out = tk.Text(frm, height=20, wrap="none")
        self.out.pack(fill="both", expand=True)
        self._log("准备就绪。请先点击“开始扫描 / 预览”。\n")

    def _pick_folder(self) -> None:
        path = filedialog.askdirectory(initialdir=self.folder_var.get())
        if path:
            self.folder_var.set(path)

    def _log(self, msg: str) -> None:
        self.out.insert("end", msg)
        self.out.see("end")

    def _run_dry(self) -> None:
        self._start_worker(apply=False)

    def _run_apply(self) -> None:
        if not self.apply_var.get():
            if not messagebox.askyesno("确认", "你没有勾选 Apply，但点击了执行移动。仍要继续吗？"):
                return
        if not messagebox.askyesno("确认", "⚠️ 这将移动文件。确定继续吗？"):
            return
        self._start_worker(apply=True)

    def _start_worker(self, apply: bool) -> None:
        self.out.delete("1.0", "end")
        self._log("正在处理...\n")

        t = threading.Thread(target=self._worker, args=(apply,), daemon=True)
        t.start()

    def _worker(self, apply: bool) -> None:
        try:
            if load_dotenv is not None:
                load_dotenv()
            root = Path(self.folder_var.get()).expanduser().resolve()
            if not root.exists() or not root.is_dir():
                raise RuntimeError(f"不是有效目录：{root}")

            cfg = AppConfig.load(self.config_var.get())

            base_url = (self.base_url_var.get().strip()
                        or os.getenv("DEEPSEEK_BASE_URL")
                        or cfg.base_url)
            model = (self.model_var.get().strip()
                     or os.getenv("DEEPSEEK_MODEL")
                     or cfg.model)

            api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("缺少环境变量 DEEPSEEK_API_KEY（或 OPENAI_API_KEY）")

            system_prompt = Path(self.system_prompt_var.get()).read_text(encoding="utf-8")
            user_prompt = Path(self.user_prompt_var.get()).read_text(encoding="utf-8")

            llm = DeepSeekLLM(api_key=api_key, base_url=base_url, model=model)

            dry_run = not apply
            res = organize(
                root=root,
                llm=llm,
                system_prompt=system_prompt,
                user_prompt_tmpl=user_prompt,
                max_bytes=cfg.max_bytes,
                preview_chars=cfg.preview_chars,
                apply=apply,
                dry_run=dry_run,
            )

            def finish():
                self._log(f"完成：共处理 {len(res)} 个文件。\n\n")
                for src, dst, r in res:
                    action = "MOVE" if apply else "PLAN"
                    self._log(f"{action}\t{src.name} -> {dst.parent.name}/\t(conf={r.confidence:.2f})\t{r.reason}\n")

            self.after(0, finish)
        except Exception as e:
            err = str(e)
            self.after(0, lambda err=err: messagebox.showerror("错误", err))


def run_gui() -> None:
    app = App()
    app.mainloop()
