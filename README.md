# Expresso Libras — Atendimento Inclusivo em Libras

Jogo 2D educacional (*serious game*) desenvolvido em **Python + Pygame** para a disciplina de **Desenvolvimento de Jogos Digitais** (Engenharia de Software — 7º período, Univassouras Campus Maricá).

## Tema e Problema Real

- **Tema do Guarda-Chuva:** 07 — Acessibilidade e Inclusão.
- **Problema:** Atendentes de comércios e serviços presenciais raramente reconhecem sinais básicos de Libras (cumprimentos, pedidos cotidianos e solicitações de informação), gerando barreiras de comunicação, constrangimento e exclusão de pessoas surdas.
- **Como a mecânica resolve o problema:** O jogador assume o papel de um atendente em uma cafeteria 2.5D que acolhe clientes surdos cumprimentando em Libras, interpreta gestos animados (128x128) no balão visual e prepara/entrega o item ou serviço correto nas estações físicas do salão. Antes de cada fase, o **Briefing Educativo** ensina os sinais novos com animações e dicas; durante o jogo, o apoio de legendas desaparece progressivamente (com pista educativa automática em baixa paciência e feedback imediato em caso de erro), medindo o aprendizado pela taxa de **autonomia sem consulta ao Mural de Libras** e pelo **tempo médio de reconhecimento**.

## Requisitos e Instalação

- **Python 3.10+** (testado em Python 3.14)
- **pygame-ce** (`>= 2.5.0`)

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / Mac
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. (Opcional) Gerar os sprites e audios em data/ manualmente
python gerar_assets.py

# 4. Executar o jogo
python main.py
```

> **Observação:** Caso a pasta `data/` ainda não exista, `main.py` gera automaticamente todos os sprites PNG e efeitos sonoros WAV na primeira execução.

## Controles e Acessibilidade

| Tecla | Ação |
| --- | --- |
| `W, A, S, D` ou `Setas` | Movimentar o atendente pelo salão |
| `SHIFT` | Correr para atender mais rápido |
| `E` ou `ESPAÇO` | Cumprimentar cliente em Libras / Pegar item na estação / Entregar pedido |
| `TAB` | Abrir ou fechar o Mural de Referência em Libras |
| `F11` ou `ALT + ENTER` | Alternar **Tela Cheia / Modo Janela** |
| `C` | Alternar **Modo Alto Contraste** |
| `F` | Alternar **Fonte Grande** |
| `M` | Ligar / silenciar áudio (jogo 100% jogável sem som) |
| `P` ou `ESC` | Pausar / voltar ao menu |

## Sinais em Libras Trabalhados

1. **OI / OLÁ** — Cumprimento inicial acolhedor no balcão.
2. **CAFÉ** — Mão em "C" levando à boca (estação Máquina de Café).
3. **ÁGUA** — Mão em "L" com polegar tocando o queixo (estação Água).
4. **BOLO** — Formato cilíndrico + gesto de fatiar (estação Vitrine de Bolos).
5. **SUCO** — Gesto de espremer fruta sobre a palma (estação Suco).
6. **CONTA / PAGAR** — Deslizar a mão sobre a palma (estação Caixa).
7. **BANHEIRO** — Mão fechada balançando no pulso (estação Placa Banheiro).
8. **OBRIGADO(A)** — Mão na testa saindo para frente (feedback de gratidão do cliente).

## Arquitetura do Projeto

```text
trabalho-jogos-alternativo/
├── main.py            # Loop principal 60 FPS, maquina de estados e interacoes
├── config.py          # Constantes, paletas, catalogo de sinais e regras das 4 fases
├── save_manager.py    # Persistencia JSON de recordes, estatisticas e acessibilidade
├── gerar_assets.py    # Gerador procedural de sprites PNG e audios WAV em data/
├── libras.py          # Carregamento e animacao dos quadros de sinais em Libras
├── player.py          # Classe Atendente com movimentacao normalizada e item na mao
├── particulas.py      # Sistema de particulas, vapor e textos flutuantes
├── estacao.py         # Estacoes interativas da cafeteria e destaque de proximidade
├── cliente.py         # Clientes surdos com balao animado de Libras e paciencia
├── fase.py            # Progressao das 4 fases, spawn por dt e metricas pedagogicas
├── hud.py             # Cenario em cache, HUD, Mural de Libras e telas de estado
├── requirements.txt   # Dependencias do projeto
└── data/              # Sprites PNG e arquivos de audio WAV gerados
```

## Equipe e Créditos de Assets

- **Felipe-dev021** (`config.py`, `main.py`, `save_manager.py`) — Arquitetura core, game loop e persistência
- **anacgsx** (`gerar_assets.py`, `libras.py`, `data/`) — Arte 2.5D, áudio WAV e curadoria das ilustrações de Libras
- **lucas-marins-dev** (`player.py`, `particulas.py`) — Movimentação do atendente, feedback visual e acessibilidade
- **GuiMell0** (`estacao.py`, `cliente.py`, `fase.py`) — Estações, comportamento de clientes e progressão das 4 fases
- **Gabriel-dev10** (`hud.py`, `README.md`) — Cenário 2.5D, HUD, Mural de Libras, telas editoriais e documentação

### Origem dos Assets e Uso de IA (Transparência P2)

| Asset | Origem | Observação |
| --- | --- | --- |
| Sprites 2.5D (atendente, clientes, estações, itens) | Gerados proceduralmente em Python (`gerar_assets.py`) | Autoral do grupo |
| Trilha sonora e efeitos sonoros (`.wav`) | Síntese procedural em Python (`gerar_assets.py`) | Autoral do grupo |
| Ilustrações dos sinais em Libras (`data/sinal_*.png`) | IA generativa (geração de imagens 2D) + composição editorial em Python | Declarado conforme diretrizes da P2 |
