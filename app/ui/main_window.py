import customtkinter as ctk
from tkinter import filedialog
import threading
import os

# Imports corretos conforme arquitetura
from app.core.pipeline import Pipeline
from app.core.container import ServiceContainer


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ----------------------------------------
        # CONFIGURAÇÃO DA JANELA
        # ----------------------------------------
        self.title("Pipeline de Transcrição")
        self.geometry("800x550")

        # ----------------------------------------
        # INICIALIZAÇÃO DO CORE (SEM QUEBRAR ARQUITETURA)
        # ----------------------------------------
        self.services = ServiceContainer()
        self.pipeline = Pipeline(self.services)

        # ----------------------------------------
        # ESTADO DA UI
        # ----------------------------------------
        self.file_path = ctk.StringVar()
        self.output_format = ctk.StringVar(value="txt")
        self.status_text = ctk.StringVar(value="Aguardando...")

        # Mapeamento de modo (UI → core)
        self.mode_map = {
            "Rápido": "fast",
            "Equilibrado": "balanced"
        }

        self._build_ui()

    # ========================================
    # UI
    # ========================================
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # -------- Seleção de arquivo --------
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.file_entry = ctk.CTkEntry(file_frame, textvariable=self.file_path)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        select_button = ctk.CTkButton(
            file_frame,
            text="Selecionar",
            command=self.select_file
        )
        select_button.pack(side="left", padx=10)

        # -------- Formato --------
        format_frame = ctk.CTkFrame(self)
        format_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(format_frame, text="Formato:").pack(side="left", padx=10)

        ctk.CTkRadioButton(
            format_frame, text="TXT",
            variable=self.output_format, value="txt"
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            format_frame, text="DOCX",
            variable=self.output_format, value="docx"
        ).pack(side="left", padx=10)

        # -------- Modo --------
        mode_frame = ctk.CTkFrame(self)
        mode_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(mode_frame, text="Modo:").pack(side="left", padx=10)

        self.mode_menu = ctk.CTkOptionMenu(
            mode_frame,
            values=["Rápido", "Equilibrado"]
        )
        self.mode_menu.set("Equilibrado")
        self.mode_menu.pack(side="left", padx=10)

        # -------- Botão --------
        self.start_button = ctk.CTkButton(
            self,
            text="Iniciar Processamento",
            command=self.start_processing
        )
        self.start_button.grid(row=3, column=0, padx=20, pady=10)

        # -------- Barra de progresso --------
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.progress.set(0)

        # -------- Status --------
        self.status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_text
        )
        self.status_label.grid(row=5, column=0, padx=20, pady=5)

        # -------- Log --------
        self.log_box = ctk.CTkTextbox(self)
        self.log_box.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        self.log_box.configure(state="disabled")

    # ========================================
    # AÇÕES
    # ========================================
    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Mídia", "*.mp4 *.mp3 *.wav"),
                ("Todos", "*.*")
            ]
        )

        if path:
            self.file_path.set(path)
            self.status_text.set(f"Arquivo: {os.path.basename(path)}")

    def start_processing(self):
        file_path = self.file_path.get()

        if not file_path or not os.path.exists(file_path):
            self.status_text.set("Selecione um arquivo válido.")
            return

        # Feedback visual
        self.start_button.configure(state="disabled")
        self.file_entry.configure(state="disabled")

        self.progress.set(0)
        self.status_text.set("Iniciando processamento...")
        self.clear_log()

        threading.Thread(
            target=self._run_pipeline,
            args=(file_path,),
            daemon=True
        ).start()

    # ========================================
    # EXECUÇÃO PIPELINE
    # ========================================
    def _run_pipeline(self, file_path: str):
        try:
            output_format = self.output_format.get()

            # Seleção de modo
            selected_mode = self.mode_map[self.mode_menu.get()]

            # Log inicial
            self._log_callback({
                "type": "log",
                "message": f"Modo: {selected_mode.upper()}"
            })

            # Simulação de progresso por etapas (sem alterar pipeline)
            self._log_callback({"type": "progress", "value": 0.1})

            self.pipeline.run(
                input_file=file_path,
                output_dir="data/output",
                format=output_format,
                callback=self._log_callback,
                mode=selected_mode  # se suportado pelo pipeline
            )

            self._log_callback({"type": "progress", "value": 1.0})

            self.after(0, self.finish_success)

        except Exception as e:
            self.after(0, self.finish_error, str(e))

    # ========================================
    # CALLBACK
    # ========================================
    def _log_callback(self, data):
        """
        Callback estruturado (thread-safe)
        """
        self.after(0, self._handle_callback, data)

    def _handle_callback(self, data):
        if isinstance(data, dict):
            if data.get("type") == "progress":
                self.progress.set(data.get("value", 0))

            elif data.get("type") == "log":
                self.add_log(data.get("message", ""))

        else:
            # compatibilidade com logs antigos
            self.add_log(str(data))

    # ========================================
    # FINALIZAÇÃO
    # ========================================
    def finish_success(self):
        self.status_text.set("Processo concluído.")
        self.start_button.configure(state="normal")
        self.file_entry.configure(state="normal")

    def finish_error(self, error):
        self.status_text.set(f"Erro: {error}")
        self.add_log(f"ERRO: {error}")
        self.start_button.configure(state="normal")
        self.file_entry.configure(state="normal")

    # ========================================
    # LOG
    # ========================================
    def add_log(self, message: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")


# ========================================
# ENTRY POINT
# ========================================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()