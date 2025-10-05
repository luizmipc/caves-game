# Construindo o Executável do Dreamrooms

Este documento explica como construir executáveis autônomos para o Dreamrooms.

## Pré-requisitos

1. **Instalar o cx_Freeze:**
```bash
pip install cx_Freeze
```

2. **Garantir que todas as dependências estejam instaladas:**
```bash
pip install -r requirements.txt
```

## Construindo o Executável

### Para Windows

1. Abra um terminal/prompt de comando em uma **máquina Windows**
2. Navegue até o diretório do projeto
3. Execute o comando de construção:
```bash
python setup.py build
```

O executável será criado em `build/exe.win-amd64-3.x/` (onde 3.x é sua versão do Python)

### Para Linux

1. Abra um terminal em uma **máquina Linux**
2. Navegue até o diretório do projeto
3. Execute o comando de construção:
```bash
python setup.py build
```

O executável será criado em `build/exe.linux-x86_64-3.x/` (onde 3.x é sua versão do Python)

## Notas Importantes

### Construções Específicas por Plataforma
- **Você DEVE construir na plataforma de destino**
- Executáveis Windows só podem ser construídos no Windows
- Executáveis Linux só podem ser construídos no Linux
- Não há suporte para compilação cruzada

### O Que É Incluído
O processo de construção inclui automaticamente:
- Interpretador Python
- Todas as bibliotecas necessárias (PyOpenGL, pygame, numpy)
- A pasta `assets/` (texturas, áudio)
- Todos os módulos do jogo (player, place, maze, light, etc.)

### Tamanho do Arquivo
O executável terá aproximadamente 50-150MB porque inclui:
- Runtime do Python
- Bibliotecas OpenGL
- Bibliotecas Pygame
- Bibliotecas NumPy
- Todos os recursos do jogo

## Distribuição

### Distribuição Windows
1. Navegue até `build/exe.win-amd64-3.x/`
2. A pasta inteira é necessária (não apenas o .exe)
3. Compacte a pasta inteira para distribuição
4. Os usuários extraem e executam `Dreamrooms.exe`

### Distribuição Linux
1. Navegue até `build/exe.linux-x86_64-3.x/`
2. A pasta inteira é necessária (não apenas o executável)
3. Crie um tarball: `tar -czf Dreamrooms-Linux.tar.gz build/exe.linux-x86_64-3.x/`
4. Os usuários extraem e executam `./Dreamrooms`

## Solução de Problemas

### Assets Ausentes
Se o jogo executar mas não tiver texturas ou som:
- Verifique se a pasta `assets/` está no mesmo diretório do executável
- Verifique se `setup.py` tem `"include_files": ["assets/"]`

### Erros de Importação
Se você receber erros de módulo não encontrado:
- Adicione o módulo ausente à lista `packages` em `setup.py`
- Reconstrua com `python setup.py build`

### Erros OpenGL
Se você receber erros relacionados ao OpenGL:
- Garanta que os drivers gráficos estejam atualizados
- Alguns sistemas podem precisar instalar OpenGL separadamente

### "Cannot execute binary file"
No Linux, garanta que o executável tenha permissões de execução:
```bash
chmod +x Dreamrooms
```

## Criando um Pacote Distribuível

### Windows
```bash
cd build/exe.win-amd64-3.x/
# Compacte o diretório inteiro
```

### Linux
```bash
cd build
tar -czf Dreamrooms-Linux.tar.gz exe.linux-x86_64-3.x/
```

## Alternativa: Distribuição Python

Se a construção de executáveis for problemática, você pode distribuir o código-fonte:

1. Incluir `requirements.txt`
2. Fornecer instruções de instalação (veja MANUAL.md)
3. Os usuários executam `python main.py` após instalar as dependências

Isso é menor e mais confiável em diferentes sistemas.

## Adicionando um Ícone (Opcional)

### Windows
1. Crie ou obtenha um arquivo `.ico`
2. Coloque-o na raiz do projeto como `icon.ico`
3. Atualize `setup.py`:
   ```python
   icon="icon.ico"
   ```
4. Reconstrua

### Linux
Ícones são tratados de forma diferente - normalmente através de arquivos desktop entry.

---

Para dúvidas ou problemas, consulte:
- [Documentação do cx_Freeze](https://cx-freeze.readthedocs.io/)
- MANUAL.md para instruções do jogo
- CODE_DOCUMENTATION.md para detalhes técnicos
