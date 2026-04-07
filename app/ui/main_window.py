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
        self.geometry("800x500")

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

        self._build_ui()

    # ========================================
    # UI
    # ========================================
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # -------- Seleção de arquivo --------
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        self.file_entry = ctk.CTkEntry(file_frame, textvariable=self.file_path)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        select_button = ctk.CTkButton(
            file_frame,
            text="Selecionar",
            command=self.select_file
        )
        select_button.pack(side="left", padx=10)

        # -------- Formato de saída --------
        format_frame = ctk.CTkFrame(self)
        format_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(format_frame, text="Formato de saída:").pack(side="left", padx=10)

        ctk.CTkRadioButton(
            format_frame,
            text="TXT",
            variable=self.output_format,
            value="txt"
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            format_frame,
            text="DOCX",
            variable=self.output_format,
            value="docx"
        ).pack(side="left", padx=10)

        # -------- Botão iniciar --------
        self.start_button = ctk.CTkButton(
            self,
            text="Iniciar Processamento",
            command=self.start_processing
        )
        self.start_button.grid(row=2, column=0, padx=20, pady=15)

        # -------- Status --------
        self.status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_text,
            font=("Arial", 14)
        )
        self.status_label.grid(row=3, column=0, padx=20, pady=5)

        # -------- Log --------
        self.log_box = ctk.CTkTextbox(self)
        self.log_box.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.log_box.configure(state="disabled")

    # ========================================
    # AÇÕES
    # ========================================
    def select_file(self):
        """
        Abre seletor de arquivos e atualiza UI
        """
        path = filedialog.askopenfilename(
            filetypes=[
                ("Mídia", "*.mp4 *.mp3 *.wav"),
                ("Todos", "*.*")
            ]
        )

        if path:
            self.file_path.set(path)

            # UX: mostra nome do arquivo
            self.status_text.set(
                f"Arquivo selecionado: {os.path.basename(path)}"
            )

    def start_processing(self):
        """
        Valida entrada e inicia execução em thread separada
        """
        file_path = self.file_path.get()

        if not file_path or not os.path.exists(file_path):
            self.status_text.set("Selecione um arquivo válido.")
            return

        # ----------------------------------------
        # FEEDBACK VISUAL INICIAL
        # ----------------------------------------
        self.start_button.configure(state="disabled")
        self.file_entry.configure(state="disabled")

        self.status_text.set("Preparando processamento...")
        self.clear_log()

        thread = threading.Thread(
            target=self._run_pipeline,
            args=(file_path,),
            daemon=True
        )
        thread.start()

    # ========================================
    # EXECUÇÃO DO PIPELINE
    # ========================================
    def _run_pipeline(self, file_path: str):
        """
        Executa pipeline em background
        """
        try:
            output_format = self.output_format.get()

            # UX: informa formato selecionado
            self._log_callback(
                f"Formato selecionado: {output_format.upper()}"
            )

            self.pipeline.run(
                input_file=file_path,
                output_dir="data/output",
                format=output_format,
                callback=self._log_callback
            )

            self.after(0, self.finish_success)

        except Exception as e:
            self.after(0, self.finish_error, str(e))

    # ========================================
    # CALLBACK DE LOG
    # ========================================
    def _log_callback(self, message: str):
        """
        Recebe logs do pipeline e envia para UI thread-safe
        """
        self.after(0, self._update_log_ui, message)

    def _update_log_ui(self, message: str):
        """
        Atualiza status + log visual
        """
        self.add_log(message)
        
        if "Concluído" in message or "Erro" in message:
            self.status_text.set(message)

    # ========================================
    # FINALIZAÇÃO
    # ========================================
    def finish_success(self):
        """
        Executado quando pipeline finaliza com sucesso
        """
        self.status_text.set("Processo concluído com sucesso.")
        self.start_button.configure(state="normal")
        self.file_entry.configure(state="normal")

    def finish_error(self, error):
        """
        Executado em caso de erro
        """
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