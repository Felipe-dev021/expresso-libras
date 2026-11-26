# Expresso Libras — Café Inclusivo

![Python](https://img.shields.io/static/v1?label=Python&message=3.10%2B&color=3776AB&style=flat-square&logo=python&logoColor=white)
![Pygame-CE](https://img.shields.io/static/v1?label=Pygame-CE&message=2.5%2B&color=00704A&style=flat-square)
![Resolucao](https://img.shields.io/static/v1?label=Full%20HD&message=1920x1080&color=1E3932&style=flat-square)
![Tema P2](https://img.shields.io/static/v1?label=Tema%2007&message=Acessibilidade%20e%20Inclusao&color=CBA258&style=flat-square)

**Expresso Libras** é um *serious game* 2.5D desenvolvido em **Python + Pygame** para a avaliação **P2** da disciplina de **Desenvolvimento de Jogos Digitais** (Bacharelado em Engenharia de Software — 7º período, Univassouras Campus Maricá).

---

## 1. Problema Real e Objetivo de Impacto

- **Tema do Guarda-Chuva:** 07 — Acessibilidade e Inclusão (*"Barreiras que só enxerga quem as vive"*).
- **Problema:** Atendentes ouvintes de cafeterias, comércios e serviços presenciais raramente reconhecem sinais básicos de **Libras** (Língua Brasileira de Sinais), gerando filas paradas, constrangimento e exclusão de clientes surdos no cotidiano.
- **Solução pela Mecânica (não é quiz):** O jogador controla fisicamente um barista em uma cafeteria 2.5D, acolhendo clientes surdos com o cumprimento em Libras, interpretando gestos ilustrados sob pressão de tempo, preparando itens nas estações certas (inclusive a **Chave WC** para o banheiro e a **Conta** sempre após um pedido de consumo) e entregando antes que a paciência acabe.
- **Como medimos que ajudou:** Ao fim de cada fase e na tela de finalização da campanha, o jogo apresenta métricas reais de aprendizado:
  - **Autonomia plena (%):** clientes atendidos sem consultar o Mural de Libras, sem legenda inicial e sem precisar da dica automática de baixa paciência.
  - **Tempo médio de reconhecimento:** em segundos por sinal.
  - **Sinais para revisar:** ranking dos sinais com mais erros na fase.
  - **Classificação final:** *Barista Fluente em Libras* ($\ge 75\%$), *Atendente Inclusivo* ($\ge 45\%$) ou *Aprendiz Dedicado* ($< 45\%$).

---

## 2. Principais Recursos

- **Visual 2.5D em Full HD (`1920x1080`, 16:9):** cenário pré-renderizado em cache com estética de cafeteria contemporânea (verde floresta, creme, madeira nogueira e latão), feixes de luz solar, balcão ripado e ordenação de profundidade (Y-Sort).
- **Tela Cheia Real + Modo Janela:** inicia em Tela Cheia mantendo nitidez 1080p e oferece botão clicável + atalho `[F11]` / `[ALT + ENTER]` para alternar com janela redimensionável (`1280x720`).
- **Acessibilidade Nativa:** Modo **Alto Contraste** (`[C]`), **Fonte Grande** (`[F]`) com ajuste automático de texto nos botões, **Mudo** (`[M]`) e jogo 100% jogável sem depender de áudio (feedback visual completo).
- **Aprendizado Progressivo (Scaffolding):** Briefing educativo antes de cada fase exibindo os sinais novos, Mural de Referência (`[TAB]`) consultável a qualquer momento, pista educativa automática abaixo de 35% de paciência e dica imediata ao errar.
- **Persistência Segura:** recordes, estatísticas de sinais e preferências de acessibilidade salvos em JSON (`progresso_expresso_libras.json`) com gravação atômica e fallback seguro.

---

## 3. Progressão das 4 Fases (Canal de Fluxo)

| Fase | Título | Meta | Sinais de Pedido | Legendas Iniciais | Paciência | Pedidos Duplos |
| :---: | --- | :---: | --- | :---: | :---: | :---: |
| **1** | Manhã Tranquila | 5 clientes | Café, Água | 3 clientes | 38s | 0% |
| **2** | Hora do Lanche | 6 clientes | Café, Água, Bolo, Suco | 2 clientes | 34s | 10% |
| **3** | Horário de Pico | 7 clientes | Todos os 6 sinais | 1 cliente | 30s | 25% |
| **4** | Casa Cheia Inclusiva | 8 clientes | Todos os 6 sinais | 0 (memória pura) | 27s | 40% |

> **Regra realista de atendimento:** clientes que solicitam **Conta / Pagar** sempre fazem primeiro um pedido de consumo (Café, Água, Bolo ou Suco) antes de pedir a conta. Ao concluir a Fase 4, o jogador acessa a **Tela de Finalização** com o resumo completo da campanha.

---

## 4. Vocabulário em Libras Trabalhado

| Sinal | Categoria | Estação / Ação no Jogo | Dica de Execução |
| --- | --- | --- | --- |
| **OI / OLÁ** | Cumprimento | Acolher no balcão (`[E]`) | Aceno aberto ao lado do rosto |
| **CAFÉ** | Bebida | Máquina de Café | Mão em "C" indo até a boca |
| **ÁGUA** | Bebida | Estação de Água | Mão em "L" tocando o queixo |
| **BOLO** | Comida | Vitrine de Bolos | Mão cortando fatia na palma |
| **SUCO** | Bebida | Estação de Suco | Mão espremendo fruta para baixo |
| **CONTA / PAGAR** | Serviço | Caixa (`CONTA`) | Deslizar mão sobre a palma |
| **BANHEIRO** | Informação | Porta-chaves (`CHAVE WC`) | Mão em "T" balançando o pulso |
| **OBRIGADO(A)** | Cortesia | Retorno de gratidão do cliente | Mão na testa saindo para frente |

---

## 5. Controles e Atalhos

| Tecla / Controle | Ação |
| --- | --- |
| `W, A, S, D` ou `Setas` | Movimentar o atendente em 8 direções |
| `SHIFT` | Correr para atender mais rápido |
| `E` ou `ESPAÇO` | Cumprimentar cliente / Pegar item / Entregar pedido / Abrir Mural |
| `TAB` ou botão `MURAL` | Abrir ou fechar o Mural de Referência em Libras |
| `F11`, `ALT + ENTER` ou botão | Alternar **Tela Cheia / Modo Janela** |
| `C` | Alternar **Modo Alto Contraste** |
| `F` | Alternar **Fonte Grande** |
| `M` ou botão `SOM` | Ligar / silenciar música e efeitos sonoros |
| `P` ou `ESC` | Pausar / voltar ao menu |

---

## 6. Instalação e Execução

### Pré-requisitos
- **Python 3.10+**
- **pygame-ce** (`>= 2.5.0`)

### Passo a passo

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/expresso-libras.git
cd expresso-libras

# 2. Criar e ativar o ambiente virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash)
source .venv/Scripts/activate

# Linux / macOS
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar o jogo
python main.py
```

> **Geração automática de assets:** se algum sprite, áudio WAV ou ilustração de fallback estiver ausente em `data/`, `main.py` regenera automaticamente na inicialização via `gerar_assets.py`.

### Empacotamento opcional (PyInstaller — Windows)

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name ExpressoLibras --add-data "data;data" main.py
```

---

## 7. Arquitetura do Projeto

```text
expresso-libras/
├── main.py            # Loop principal 60 FPS, tela cheia Full HD, máquina de estados e interações
├── config.py          # Constantes, paletas (padrão e alto contraste), catálogo de Libras e 4 fases
├── save_manager.py    # Persistência JSON atômica de recordes, estatísticas e acessibilidade
├── gerar_assets.py    # Gerador procedural 2x supersampled de sprites 2.5D, áudios WAV e fallback
├── libras.py          # Carregamento, cache suave e animação sutil das ilustrações de Libras
├── player.py          # Classe Atendente com movimento normalizado por dt, hitbox 2.5D e bandeja
├── particulas.py      # Partículas de feedback, vapor da máquina de café e textos flutuantes
├── estacao.py         # Estações interativas da cafeteria e destaque visual de proximidade
├── cliente.py         # Clientes surdos com balão de Libras, pista automática e barra de paciência
├── fase.py            # Gerenciador das 4 fases, regras de pedido e métricas de autonomia
├── hud.py             # Cenário 2.5D em cache, HUD, Briefing, Mural, Pausa e Tela de Finalização
├── requirements.txt   # Dependências do projeto
└── data/              # Sprites PNG 2.5D, 8 ilustrações de Libras (256x256) e 6 áudios WAV
```

---

## 8. Equipe e Origem dos Assets (Transparência P2)

### Integrantes e Responsabilidades

| Integrante | Módulos Principais | Responsabilidade |
| --- | --- | --- |
| **Felipe-dev021** | `main.py`, `save_manager.py` | Arquitetura core, game loop 60 FPS, tela cheia Full HD e persistência JSON |
| **anacgsx** | `gerar_assets.py`, `libras.py`, `data/` | Sprites 2.5D supersampled, síntese de áudio WAV e curadoria de Libras |
| **lucas-marins-dev** | `player.py`, `particulas.py` | Movimentação 2.5D do atendente, bandeja e feedback visual inclusivo |
| **GuiMell0** | `config.py`, `estacao.py`, `cliente.py`, `fase.py` | Estações, lógica de clientes/pedidos e progressão das 4 fases |
| **Gabriel-dev10** | `hud.py`, `README.md` | Cenário 2.5D, HUD, Mural, acessibilidade visual, Tela de Finalização e documentação |

### Origem dos Assets e Uso de IA

| Recurso | Origem | Observação |
| --- | --- | --- |
| Sprites 2.5D (atendente, clientes, estações, itens) | Gerados proceduralmente via Python (`gerar_assets.py`) | Autoral do grupo, sem assets de terceiros |
| Trilha sonora e efeitos sonoros (`.wav`) | Síntese procedural via Python (`gerar_assets.py`) | Autoral do grupo |
| Ilustrações dos 8 sinais de Libras (`data/sinal_*.png`) | IA generativa de imagens 2D (estilo editorial uniforme) | Revisadas e integradas pelo grupo; declarado conforme diretrizes da P2 |
| Apoio ao desenvolvimento e refatoração | Assistente de código com IA | Todo o código foi revisado, testado e compreendido pela equipe |
