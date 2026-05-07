import subprocess
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import signal


class RunnerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Pump Predictor")
        self.geometry("900x550")

        self.proc: subprocess.Popen | None = None
        self.q: queue.Queue[str] = queue.Queue()

        # Top controls
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.run_btn = ttk.Button(top, text="Run", command=self.start_run)
        self.run_btn.pack(side="left")

        self.stop_btn = ttk.Button(top, text="Stop", command=self.stop_run, state="disabled")
        self.stop_btn.pack(side="left", padx=(10, 0))

        self.status_var = tk.StringVar(value="Idle")
        ttk.Label(top, textvariable=self.status_var).pack(side="left", padx=15)

        # Output area
        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Scrollbar
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=scroll.set)

        # Periodic UI update loop
        self.after(100, self.flush_queue)

        # Close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def append(self, s: str):
        self.text.insert("end", s)
        self.text.see("end")

    def start_run(self):
        if self.proc and self.proc.poll() is None:
            messagebox.showinfo("Already running", "Main.py is already running.")
            return

        self.text.delete("1.0", "end")
        self.append("Starting Main.py...\n\n")

        main_path = os.path.join(os.path.dirname(__file__), "Main.py")
        if not os.path.exists(main_path):
            messagebox.showerror("Not found", f"Cannot find Main.py at:\n{main_path}")
            return

        # Start subprocess with unbuffered output so logs stream live
        # Use the current Python interpreter to avoid PATH/venv confusion.
        creationflags = 0
        preexec_fn = None

        # On Windows, CREATE_NEW_PROCESS_GROUP helps terminate more reliably
        if os.name == "nt":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        self.proc = subprocess.Popen(
            [sys.executable, "-u", main_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(__file__),
            creationflags=creationflags,
            preexec_fn=preexec_fn,
        )

        self.run_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set("Running")

        # Start background thread to read output
        t = threading.Thread(target=self._reader_thread, daemon=True)
        t.start()

        # Watcher thread to re-enable buttons when done
        w = threading.Thread(target=self._watcher_thread, daemon=True)
        w.start()

    def _reader_thread(self):
        assert self.proc is not None
        try:
            for line in self.proc.stdout:
                self.q.put(line)
        except Exception as e:
            self.q.put(f"\n[UI] Output reader error: {e}\n")

    def _watcher_thread(self):
        assert self.proc is not None
        rc = self.proc.wait()
        self.q.put(f"\n\n[Process exited with code {rc}]\n")

        # Re-enable buttons in UI thread
        def done():
            self.run_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.status_var.set("Idle")
            self.proc = None
        self.after(0, done)

    def flush_queue(self):
        try:
            while True:
                self.append(self.q.get_nowait())
        except queue.Empty:
            pass
        self.after(100, self.flush_queue)

    def stop_run(self):
        if not self.proc or self.proc.poll() is not None:
            return

        self.append("\n[Stopping...]\n")

        try:
            if os.name == "nt":
                # CTRL_BREAK_EVENT is more graceful for process groups, but kill is most reliable.
                # Try terminate then kill.
                self.proc.terminate()
            else:
                self.proc.terminate()
        except Exception:
            pass

        # If it doesn't stop quickly, force kill
        self.after(800, self._force_kill_if_needed)

    def _force_kill_if_needed(self):
        if self.proc and self.proc.poll() is None:
            self.append("[Force killing process]\n")
            try:
                self.proc.kill()
            except Exception:
                pass

    def on_close(self):
        # Ensure subprocess is stopped when closing UI
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.kill()
            except Exception:
                pass
        self.destroy()


if __name__ == "__main__":
    # Optional: nicer ttk theme
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = RunnerUI()
    app.mainloop()
