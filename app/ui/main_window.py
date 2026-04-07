import customtkinter as ctk
from tkinter import filedialog
import threading
import os

# IMPORTANTE:
# Ajuste este import conforme seu projeto real
from app.core.pipeline import Pipeline
from app.core.container import ServiceContainer


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("Pipeline de Transcrição")
        self.geometry("700x400")

        # Pipeline (não alteramos nada nele)
        self.services = ServiceContainer()
        self.pipeline = Pipeline(self.services)

        # Variáveis de estado
        self.file_path = ctk.StringVar()
        self.output_format = ctk.StringVar(value="txt")
        self.status_text = ctk.StringVar(value="Aguardando...")

        self._build_ui()

    # ========================
    # UI
    # ========================
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # -------- Seleção de arquivo --------
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path
        )
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

        txt_radio = ctk.CTkRadioButton(
            format_frame,
            text="TXT",
            variable=self.output_format,
            value="txt"
        )
        txt_radio.pack(side="left", padx=10)

        docx_radio = ctk.CTkRadioButton(
            format_frame,
            text="DOCX",
            variable=self.output_format,
            value="docx"
        )
        docx_radio.pack(side="left", padx=10)

        # -------- Botão iniciar --------
        start_button = ctk.CTkButton(
            self,
            text="Iniciar Processamento",
            command=self.start_processing
        )
        start_button.grid(row=2, column=0, padx=20, pady=20)

        # -------- Status --------
        status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_text
        )
        status_label.grid(row=3, column=0, padx=20, pady=10)

    # ========================
    # Ações
    # ========================
    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Mídia", "*.mp4 *.mp3 *.wav"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if path:
            self.file_path.set(path)

    def start_processing(self):
        file_path = self.file_path.get()

        if not file_path or not os.path.exists(file_path):
            self.status_text.set("Selecione um arquivo válido.")
            return

        self.status_text.set("Processando...")

        thread = threading.Thread(
            target=self._run_pipeline,
            args=(file_path,),
            daemon=True
        )
        thread.start()

    # ========================
    # Execução do pipeline
    # ========================
    def _run_pipeline(self, file_path: str):
        try:
            output_format = self.output_format.get()

            # IMPORTANTE:
            # Aqui você adapta conforme a assinatura real do seu pipeline
            result = self.pipeline.run(
                input_path=file_path,
                output_format=output_format
            )

            # Atualizar UI na thread principal
            self.after(0, lambda: self.status_text.set("Concluído com sucesso."))

        except Exception as e:
            self.after(0, lambda: self.status_text.set(f"Erro: {str(e)}"))


# ========================
# ENTRY POINT
# ========================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()