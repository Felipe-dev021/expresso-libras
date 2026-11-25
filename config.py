"""Configuracoes centralizadas do jogo Sinal Aberto.

Reune dimensoes de tela, constantes de jogabilidade, paleta autoral
(padrao artesanal e alto contraste), catalogo educativo de sinais em
Libras e parametros das quatro fases progressivas.
"""

import os

# --- Janela e desempenho (Full HD 16:9 nativo) ---
TITULO_JOGO = "Expresso Libras — Cafe Inclusivo"
LARGURA = 1920
ALTURA = 1080
JANELA_LARGURA = 1280
JANELA_ALTURA = 720
FPS = 60

# --- Caminhos de arquivos (compativel com PyInstaller) ---
PASTA_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
ARQUIVO_SAVE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "progresso_expresso_libras.json")
)


def caminho_arquivo(nome_arquivo: str) -> str:
    """Retorna o caminho absoluto de um asset dentro da pasta data/."""
    return os.path.join(PASTA_DATA, nome_arquivo)


# --- Layout 2.5D do cenario (Cafeteria Expresso Libras - 1920x1080) ---
HUD_ALTURA = 86
AREA_ATENDENTE = (116, 420, 1688, 594)  # (x, y, largura, altura)
BALCAO_Y = 382
BALCAO_ALTURA = 82

# Posicoes das 4 cadeiras/pontos de atendimento no balcao (x, y)
PONTOS_BALCAO = [
    (430, 328),
    (790, 328),
    (1150, 328),
    (1510, 328),
]

# --- Fisica e movimentacao do jogador ---
VELOCIDADE_JOGADOR = 530.0
VELOCIDADE_CORRIDA = 740.0
RAIO_INTERACAO = 165.0

# --- Regras de pontuacao, vidas e acessibilidade educativa ---
VIDAS_INICIAIS = 4
PONTOS_ACERTO_BASE = 100
BONUS_SEM_MURAL = 50
BONUS_RAPIDEZ_MAX = 40
BONUS_COMBO = 25
PENALIDADE_ERRO_PACIENCIA = 0.12  # erro suave para incentivar aprendizado
LIMIAR_DICA_AUTOMATICA = 0.35     # mostra legenda educativa se paciencia < 35%

# --- Paleta autoral (Cafeteria artesanal brasileira / editorial) ---
PALETA_PADRAO = {
    "fundo": (32, 24, 20),
    "parede": (244, 235, 220),
    "parede_azulejo": (232, 221, 202),
    "parede_sombra": (214, 198, 174),
    "rodape": (92, 62, 44),
    "piso_claro": (208, 170, 130),
    "piso_escuro": (192, 152, 112),
    "piso_linha": (164, 126, 88),
    "balcao_topo": (248, 243, 235),
    "balcao_frente": (118, 76, 48),
    "balcao_detalhe": (86, 52, 32),
    "hud_bg": (34, 25, 21),
    "hud_borda": (214, 146, 72),
    "texto_claro": (250, 244, 234),
    "texto_escuro": (36, 26, 20),
    "destaque": (214, 124, 48),
    "verde": (46, 142, 92),
    "verde_claro": (152, 222, 176),
    "amarelo": (232, 180, 48),
    "vermelho": (196, 68, 58),
    "azul": (48, 122, 184),
    "card_bg": (250, 245, 235),
    "card_borda": (74, 52, 38),
    "sombra": (20, 14, 11),
}

# --- Paleta Alto Contraste (Acessibilidade visual AAA) ---
PALETA_ALTO_CONTRASTE = {
    "fundo": (0, 0, 0),
    "parede": (18, 18, 24),
    "parede_azulejo": (28, 28, 36),
    "parede_sombra": (10, 10, 14),
    "rodape": (14, 14, 18),
    "piso_claro": (30, 30, 38),
    "piso_escuro": (22, 22, 30),
    "piso_linha": (68, 68, 84),
    "balcao_topo": (245, 245, 245),
    "balcao_frente": (42, 42, 54),
    "balcao_detalhe": (255, 220, 0),
    "hud_bg": (0, 0, 0),
    "hud_borda": (255, 220, 0),
    "texto_claro": (255, 255, 255),
    "texto_escuro": (0, 0, 0),
    "destaque": (255, 210, 0),
    "verde": (0, 220, 110),
    "verde_claro": (160, 255, 200),
    "amarelo": (255, 225, 0),
    "vermelho": (255, 70, 70),
    "azul": (80, 190, 255),
    "card_bg": (16, 16, 22),
    "card_borda": (255, 220, 0),
    "sombra": (0, 0, 0),
}

# --- Catalogo educativo de sinais em Libras ---
SINAIS_LIBRAS = {
    "oi": {
        "nome": "OI / OLA",
        "categoria": "Cumprimento",
        "estacao": "cumprimento",
        "descricao": "Mao aberta acenando de um lado para o outro na altura do rosto.",
        "dica_curta": "Aceno aberto ao lado do rosto",
        "cor": (48, 122, 184),
    },
    "cafe": {
        "nome": "CAFE",
        "categoria": "Bebida",
        "estacao": "cafe",
        "descricao": "Mao em formato de 'C' levando uma xicara imaginaria ate a boca.",
        "dica_curta": "Mao em 'C' indo ate a boca",
        "cor": (142, 78, 42),
    },
    "agua": {
        "nome": "AGUA",
        "categoria": "Bebida",
        "estacao": "agua",
        "descricao": "Mao em 'L' (polegar e indicador) tocando o queixo duas vezes.",
        "dica_curta": "Mao em 'L' tocando o queixo",
        "cor": (36, 146, 198),
    },
    "bolo": {
        "nome": "BOLO",
        "categoria": "Comida",
        "estacao": "bolo",
        "descricao": "Mao aberta de lado fazendo movimento de cortar uma fatia.",
        "dica_curta": "Mao cortando fatia na palma",
        "cor": (196, 94, 118),
    },
    "suco": {
        "nome": "SUCO",
        "categoria": "Bebida",
        "estacao": "suco",
        "descricao": "Mao fechando e abrindo como quem espreme uma laranja no copo.",
        "dica_curta": "Mao espremendo fruta p/ baixo",
        "cor": (222, 138, 28),
    },
    "obrigado": {
        "nome": "OBRIGADO(A)",
        "categoria": "Cortesia",
        "estacao": "cortesia",
        "descricao": "Dedos unidos tocam a testa e descem para frente em agradecimento.",
        "dica_curta": "Mao na testa saindo p/ frente",
        "cor": (46, 142, 92),
    },
    "pagar": {
        "nome": "CONTA / PAGAR",
        "categoria": "Servico",
        "estacao": "caixa",
        "descricao": "Uma mao desliza para frente sobre a palma aberta da outra mao.",
        "dica_curta": "Deslizar mao sobre a palma",
        "cor": (108, 142, 54),
    },
    "banheiro": {
        "nome": "BANHEIRO",
        "categoria": "Informacao",
        "estacao": "banheiro",
        "descricao": "Mao fechada com o polegar entre os dedos (letra T) balancando.",
        "dica_curta": "Mao em 'T' balancando o pulso",
        "cor": (118, 86, 176),
    },
}

# Sinais que representam pedidos/acoes fisicas em estacoes
SINAIS_ESTACAO = ["cafe", "agua", "bolo", "suco", "pagar", "banheiro"]

# --- Definicao das 4 fases progressivas (Mais acessivel e educativo) ---
FASES_CONFIG = [
    {
        "numero": 1,
        "titulo": "Manha Tranquila",
        "subtitulo": "Aprendendo os primeiros sinais no balcao",
        "meta_clientes": 5,
        "sinais_permitidos": ["cafe", "agua"],
        "sinais_novos": ["oi", "cafe", "agua", "obrigado"],
        "legendas_iniciais": 3,
        "paciencia_base": 38.0,
        "intervalo_spawn": 6.8,
        "max_simultaneos": 2,
        "chance_pedido_duplo": 0.0,
        "exige_cumprimento": True,
        "dica_briefing": (
            "Fase introdutoria! Os 3 primeiros clientes exibem legenda para voce "
            "associar o gesto ao pedido. Depois, teste sua memoria!"
        ),
    },
    {
        "numero": 2,
        "titulo": "Hora do Lanche",
        "subtitulo": "Ampliando o vocabulario do cardapio",
        "meta_clientes": 6,
        "sinais_permitidos": ["cafe", "agua", "bolo", "suco"],
        "sinais_novos": ["bolo", "suco"],
        "legendas_iniciais": 2,
        "paciencia_base": 34.0,
        "intervalo_spawn": 5.8,
        "max_simultaneos": 3,
        "chance_pedido_duplo": 0.10,
        "exige_cumprimento": True,
        "dica_briefing": (
            "Novos sinais no cardapio: BOLO e SUCO! Os 2 primeiros clientes "
            "mostram legenda. Aperte [TAB] sempre que quiser revisar o Mural."
        ),
    },
    {
        "numero": 3,
        "titulo": "Horario de Pico",
        "subtitulo": "Servicos, informacoes e pedidos combinados",
        "meta_clientes": 7,
        "sinais_permitidos": ["cafe", "agua", "bolo", "suco", "pagar", "banheiro"],
        "sinais_novos": ["pagar", "banheiro"],
        "legendas_iniciais": 1,
        "paciencia_base": 30.0,
        "intervalo_spawn": 5.0,
        "max_simultaneos": 3,
        "chance_pedido_duplo": 0.25,
        "exige_cumprimento": True,
        "dica_briefing": (
            "Agora clientes tambem pedem CONTA/PAGAR e BANHEIRO, e alguns "
            "fazem 2 pedidos seguidos. A pista visual aparece se demorar muito."
        ),
    },
    {
        "numero": 4,
        "titulo": "Casa Cheia Inclusiva",
        "subtitulo": "Desafio final de fluencia e acolhimento",
        "meta_clientes": 8,
        "sinais_permitidos": ["cafe", "agua", "bolo", "suco", "pagar", "banheiro"],
        "sinais_novos": [],
        "legendas_iniciais": 0,
        "paciencia_base": 27.0,
        "intervalo_spawn": 4.3,
        "max_simultaneos": 4,
        "chance_pedido_duplo": 0.40,
        "exige_cumprimento": True,
        "dica_briefing": (
            "Todos os sinais combinados em ritmo animado! Atenda sem consultar "
            "o Mural para alcancar nota maxima em autonomia inclusiva."
        ),
    },
]
