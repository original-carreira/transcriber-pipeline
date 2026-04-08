# 📌 TranscriberPipeline

Sistema em Python para **transcrição e organização de conteúdo a partir de áudio e vídeo**, com interface gráfica e distribuição via executável.

---

## 🚀 Status Atual — v1.3.0

✔ Pipeline completo funcional (produção inicial)
✔ Interface gráfica (CustomTkinter)
✔ Transcrição com faster-whisper
✔ Extração de áudio com ffmpeg
✔ Exportação: TXT / DOCX / SRT
✔ Build com PyInstaller funcional
✔ Instalador profissional (Inno Setup)
✔ Arquitetura modular validada
✔ Pronto para distribuição

---

## 🧠 Visão Geral

Fluxo do sistema:

```
Entrada (vídeo/áudio)
→ Extração de áudio (ffmpeg)
→ Transcrição (faster-whisper)
→ Organização de texto
→ Exportação (TXT / DOCX / SRT)
→ Interface gráfica (CustomTkinter)
```

---

## 🧱 Arquitetura

```
UI → Pipeline → Services → Models → Export
```

### Princípios:

* Pipeline apenas orquestra (sem lógica de negócio)
* Services executam lógica
* Models representam dados
* UI desacoplada
* Baixo acoplamento e alta coesão

---

## 📂 Estrutura do Projeto

```
app/
  core/
    pipeline.py
    container.py

  services/
    audio_service.py
    transcription_service.py
    formatting_service.py
    export_service.py

  models/
    transcript.py
    segment.py
    document.py

  ui/
    main_window.py

  utils/
    path_utils.py
    app_paths.py

assets/
  icon.ico

ffmpeg/
  ffmpeg.exe

installer/
  setup.iss

main_ui.py
```

---

## ⚙️ Funcionalidades

### 🎤 Transcrição

* faster-whisper (modo fast / balanced)
* suporte a progresso em tempo real
* otimizado para CPU

---

### 🎧 Extração de áudio

* ffmpeg integrado
* compatível com executável (.exe)
* uso de diretório temporário controlado (AppData)

---

### 🧾 Organização de texto

* segmentação por frases
* agrupamento em parágrafos
* heurísticas de legibilidade

---

### 📤 Exportação

| Formato | Descrição              |
| ------- | ---------------------- |
| TXT     | Texto simples          |
| DOCX    | Documento formatado    |
| SRT     | Legendas com timestamp |

---

### 🖥️ Interface (CustomTkinter)

* seleção de arquivo
* escolha de formato (txt/docx/srt)
* seleção de modo (fast/balanced)
* barra de progresso
* logs em tempo real

---

## 📦 Distribuição

### ✔ Executável (.exe)

Gerado com PyInstaller:

```
pyinstaller --onefile --windowed ...
```

---

### ✔ Instalador (Windows)

Gerado com Inno Setup:

* instala em `Program Files`
* cria atalhos
* inclui ffmpeg
* pronto para usuário final

---

## 📁 Armazenamento de Arquivos

Arquivos gerados são salvos em:

```
C:\Users\<user>\AppData\Local\TranscriberPipeline\
```

* `output/` → arquivos exportados
* `temp/` → arquivos temporários

✔ evita poluir diretório do executável
✔ padrão profissional Windows

---

## 🧪 Execução em Desenvolvimento

```bash
python main_ui.py
```

---

## 🏗️ Build do Executável

```bash
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--name TranscriberPipeline ^
--icon assets/icon.ico ^
--paths . ^
--add-data "ffmpeg/ffmpeg.exe;ffmpeg" ^
--collect-data faster_whisper ^
--hidden-import=faster_whisper ^
--hidden-import=ctranslate2 ^
main_ui.py
```

---

## 📌 Versão

```
v1.3.0
```

---

## 🧭 Roadmap

### 🔹 Curto prazo

* melhoria de pontuação automática
* exportação JSON estruturado

### 🔹 Médio prazo

* pós-processamento com LLM
* segmentação semântica

### 🔹 Avançado

* pipeline assíncrono
* sistema de eventos
* testes automatizados (pytest)
* auto-update

---

## 👤 Autor

Victor Carreira

---

## 📄 Licença

Definir (MIT recomendado)

---
