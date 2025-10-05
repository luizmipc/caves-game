# Dreamrooms - Manual do Jogador

## Índice
1. [Primeiros Passos](#primeiros-passos)
2. [Controles](#controles)
3. [Objetivos do Jogo](#objetivos-do-jogo)
4. [Mecânicas de Gameplay](#mecânicas-de-gameplay)
5. [Dicas e Estratégias](#dicas-e-estratégias)
6. [Configuração](#configuração)

---

## Primeiros Passos

### Requisitos do Sistema
- Python 3.x
- PyOpenGL
- pygame
- numpy

### Instalação

1. **Criar um ambiente virtual:**
```bash
python -m venv venv
```

2. **Ativar o ambiente virtual:**
```bash
source venv/bin/activate
```

3. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

### Executando o Jogo
```bash
python main.py
```

**Nota**: Certifique-se de que o ambiente virtual está ativado (você deve ver `(venv)` no prompt do seu terminal) antes de executar o jogo.

### Menu Principal
Quando você inicia o jogo, verá o menu principal com três opções:
- **Jogar**: Iniciar um novo jogo
- **Config**: Ajustar configurações do jogo (volume da música, tamanho do labirinto)
- **Sair**: Sair do jogo

---

## Controles

### Movimento
- **W**: Mover para frente
- **S**: Mover para trás
- **A**: Mover para a esquerda
- **D**: Mover para a direita

### Câmera
- **Movimento do Mouse**: Olhar ao redor (visão 360 graus)
- A câmera segue os movimentos do mouse para controle total sobre a direção da visão

### Sistema
- **ESC**: Sair do jogo (funciona a qualquer momento)

---

## Objetivos do Jogo

### Objetivo Principal
Navegue pelo labirinto escuro para encontrar a **SAÍDA** antes que o inimigo te capture.

### Condição de Vitória
Alcance o ponto de saída (localização marcada no labirinto). Quando você escapar:
- O labirinto inteiro é revelado com luz plena
- Música de vitória toca
- Créditos são exibidos
- Você escapou com sucesso do pesadelo

### Condição de Derrota
Se o inimigo te capturar (chegar a 1 unidade da sua posição):
- Música de morte toca
- "GAME OVER" aparece na tela em vermelho
- Você não pode se mover - apenas pressione ESC para sair
- Você deve reiniciar para tentar novamente

---

## Mecânicas de Gameplay

### A Fonte de Luz
- Você carrega uma fonte de luz semelhante a tocha que ilumina um cone à sua frente
- **Ângulo do cone**: 35 graus
- **Alcance**: 15 unidades
- **Posição**: A fonte de luz é posicionada atrás e abaixo do nível dos olhos para imersão (você não a verá)
- A luz tem queda quente e realista com neblina atmosférica

### O Labirinto
- **Gerado proceduralmente**: Cada partida cria um novo layout de labirinto
- **Tamanho**: Configurável nas configurações (1-10, onde maior = labirinto maior)
- **Layout**: Garantido ter um caminho do início à saída
- O labirinto inclui becos sem saída onde o inimigo pode surgir

### O Inimigo
- **Alcance de Detecção**: 15 unidades - se você chegar a esta distância, o inimigo te avistará
- **Velocidade de Perseguição**: 3.5 unidades/segundo (mais rápido que sua velocidade de caminhada)
- **Comportamento da IA**:
  - Patrulha até avistar você
  - Uma vez que te vê, persegue implacavelmente
  - Pode navegar ao redor de paredes
  - Te capturará se chegar a 1 unidade
- **Localização de Spawn**: Colocado aleatoriamente em um beco sem saída, longe dos pontos de início e saída

### Visibilidade
- **Escuridão**: O labirinto está em escuridão completa exceto pela sua luz
- **Neblina**: Neblina de distância cria profundidade atmosférica (começa em 4 unidades, completa em 14 unidades)
- **Iluminação de Superfície**: Paredes, chão e teto reagem realisticamente à sua fonte de luz

---

## Dicas e Estratégias

### Navegação
1. **Marque Seu Caminho**: Tente lembrar curvas e pontos de referência
2. **Ouça Atentamente**: Pistas de áudio podem ajudar você a se orientar
3. **Verifique Esquinas**: O inimigo pode estar em qualquer esquina
4. **Becos Sem Saída**: Se você encontrar um beco sem saída, volte rapidamente

### Lidando com o Inimigo
1. **Fique Alerta**: Uma vez que você estiver a 15 unidades, a perseguição começa
2. **Continue Se Movendo**: O inimigo é mais rápido que você - não pare
3. **Use Esquinas**: Curvas fechadas podem ajudar você a quebrar a linha de visão
4. **Conheça Seus Limites**: Você pode chegar muito perto de paredes sem que a luz falhe

### Gerenciamento de Luz
1. **Aponte Para Onde Está Indo**: A luz segue a direção da sua visão
2. **Visibilidade de Curto Alcance**: Você pode chegar bem próximo de paredes e ainda vê-las
3. **Cone Amplo**: O cone de 35 graus oferece boa visão periférica
4. **Consciência da Neblina**: Objetos distantes desaparecerão na escuridão

### Estratégia Geral
- **Explore Sistematicamente**: Tente seguir um padrão (ex: sempre vire à direita)
- **Não Entre em Pânico**: Quando perseguido, pense sobre sua rota de fuga
- **Aprenda os Sons**: A trilha sonora ambiente e pistas de áudio fazem parte da experiência
- **Abrace a Atmosfera**: Este é um jogo sobre tensão e pavor - deixe-se imergir

---

## Configuração

### Menu de Configurações
Acesse o menu de configuração no menu principal para ajustar:

#### Configurações de Música
- **Música Ativada/Desativada**: Ativar/desativar música de fundo
- **Volume**: Ajustar volume da música (0.0 a 1.0)

#### Configurações do Labirinto
- **Tamanho do Labirinto**: Definir o tamanho do labirinto gerado (1-10)
  - Tamanho 1-3: Jogos pequenos e rápidos
  - Tamanho 4-6: Dificuldade média e balanceada
  - Tamanho 7-10: Exploração grande e estendida

### Arquivos de Áudio
O jogo usa três arquivos de áudio (colocar em `assets/audio/`):
- **soundtrack.mp3**: Música principal do jogo (toca em loop durante o gameplay)
- **autro.mp3**: Música de vitória (toca quando você alcança a saída)
- **death.mp3**: Música de game over (toca quando capturado pelo inimigo)

Se esses arquivos estiverem faltando, o jogo ainda executará mas sem música.

### Texturas
O jogo pode usar texturas personalizadas (colocar em `assets/textures/`):
- **floor.png**: Textura do chão
- **wall.png**: Textura da parede
- **enemy.png**: Textura do sprite do inimigo

Se as texturas estiverem faltando, o jogo usará cores padrão.

---

## Compreendendo a Experiência

**Dreamrooms** foi projetado para evocar sentimentos específicos:

- **Pavor Liminal**: A sensação de estar em um espaço de transição que não deveria existir
- **Isolamento**: Você está sozinho com apenas sua luz para conforto
- **Perseguição**: Algo está caçando você na escuridão
- **Desorientação**: O labirinto é feito para confundir e perturbar

Este não é um jogo sobre vencer rapidamente. É sobre a jornada pelo labirinto, a tensão da exploração e a fuga desesperada quando descoberto. Tome seu tempo, mergulhe na atmosfera e lembre-se: você não deve se sentir seguro.

---

## Solução de Problemas

### O Jogo Não Inicia
- Garanta que todas as dependências estejam instaladas: `pip install PyOpenGL PyOpenGL_accelerate pygame numpy`
- Verifique a versão do Python (3.x necessário)

### Problemas de Performance
- Reduza o tamanho do labirinto na configuração
- Feche outros aplicativos
- Atualize drivers gráficos

### Sem Som
- Verifique se os arquivos de áudio existem em `assets/audio/`
- Verifique se o mixer do pygame está instalado corretamente
- Verifique configurações de volume do sistema

### Tela Preta
- O jogo é intencionalmente escuro! Mova-se e procure pela luz
- Se realmente estiver quebrado, verifique compatibilidade com OpenGL

---

## Créditos

**Desenvolvedores do Jogo:**
- Leonardo Zordan Lima
- Luiz Marcelo Itapicuru Pereira Costa
- Matheus Soares Martins
- Thiago Crivaro Nunes

**Inspirado Por:**
- Estética Backrooms/Espaços Liminais
- Cultura visual Dreamcore
- David Lynch (Twin Peaks, Lost Highway)
- Arte experimental de David Bowie

---

*Boa sorte. Você vai precisar.*
