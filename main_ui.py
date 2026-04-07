import customtkinter as ctk
from app.ui.main_window import MainWindow


def main():
    # Aparência
    ctk.set_appearance_mode("dark")  # "light" ou "system"
    ctk.set_default_color_theme("blue")

    # Iniciar app
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()