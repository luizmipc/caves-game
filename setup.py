"""
Script de configuração cx_Freeze para Dreamrooms.

Este script constrói executáveis standalone para o jogo.

Uso:
    python setup.py build

O executável será criado no diretório build/.
"""

from cx_Freeze import setup, Executable
import sys

# Dependências a incluir
build_exe_options = {
    # Pacotes a incluir explicitamente
    "packages": [
        "pygame",
        "OpenGL",
        "OpenGL.GL",
        "OpenGL.GLU",
        "numpy",
        "os",
        "random"
    ],

    # Arquivos e pastas a incluir com o executável
    "include_files": [
        "assets/",  # Inclui todos os recursos do jogo (áudio, texturas)
    ],

    # Módulos a excluir (reduz tamanho do arquivo)
    "excludes": [
        "tkinter",  # Não usado no jogo
        "unittest",
        "email",
        "http",
        "xml",
        "pydoc",
    ],

    # Otimização adicional
    "optimize": 2,
}

# Determina base para Windows (usa "Win32GUI" para esconder janela do console)
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Esconde janela do console no Windows

# Configuração do executável
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="Dreamrooms",  # Nome do executável
        icon=None,  # Adicione "icon.ico" aqui se você criar um
    )
]

# Configuração do setup
setup(
    name="Dreamrooms",
    version="1.0",
    description="Um jogo de labirinto de horror liminal inspirado por backrooms, dreamcore e David Lynch",
    author="Leonardo Zordan Lima, Luiz Marcelo Itapicuru Pereira Costa, Matheus Soares Martins, Thiago Crivaro Nunes",
    options={"build_exe": build_exe_options},
    executables=executables,
)
