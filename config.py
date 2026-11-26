"""Configuracoes centralizadas do jogo Expresso Libras.

Reune resolucao Full HD, parametros de jogabilidade, paleta inspirada em
cafeterias modernas (verde floresta, creme e madeira nogueira), catalogo
educativo de Libras e configuracao das quatro fases progressivas.
"""

import os

TITULO_JOGO = "Expresso Libras — Cafe Inclusivo"
LARGURA = 1920
ALTURA = 1080
JANELA_LARGURA = 1280
JANELA_ALTURA = 720
FPS = 60

PASTA_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
ARQUIVO_SAVE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "progresso_expresso_libras.json")
)


def caminho_arquivo(nome_arquivo: str) -> str:
    """Retorna o caminho absoluto de um asset dentro da pasta data/."""
    return os.path.join(PASTA_DATA, nome_arquivo)


HUD_ALTURA = 86
AREA_ATENDENTE = (116, 420, 1688, 594)
BALCAO_Y = 382
BALCAO_ALTURA = 82

PONTOS_BALCAO = [
    (380, 328),
    (730, 328),
    (1190, 328),
    (1540, 328),
]

VELOCIDADE_JOGADOR = 530.0
VELOCIDADE_CORRIDA = 740.0
RAIO_INTERACAO = 165.0

VIDAS_INICIAIS = 4
PONTOS_ACERTO_BASE = 100
BONUS_SEM_MURAL = 50
BONUS_RAPIDEZ_MAX = 40
BONUS_COMBO = 25
PENALIDADE_ERRO_PACIENCIA = 0.12
LIMIAR_DICA_AUTOMATICA = 0.35

PALETA_PADRAO = {
    "fundo": (22, 42, 36),
    "parede": (245, 242, 235),
    "parede_azulejo": (228, 224, 214),
    "parede_sombra": (206, 202, 192),
    "rodape": (30, 57, 50),
    "piso_claro": (204, 172, 134),
    "piso_escuro": (188, 154, 116),
    "piso_linha": (156, 124, 88),
    "balcao_topo": (248, 247, 243),
    "balcao_frente": (30, 57, 50),
    "balcao_detalhe": (18, 38, 32),
    "hud_bg": (22, 44, 38),
    "hud_borda": (203, 162, 88),
    "texto_claro": (248, 246, 240),
    "texto_escuro": (26, 42, 36),
    "destaque": (0, 112, 74),
    "dourado": (203, 162, 88),
    "verde": (0, 112, 74),
    "verde_claro": (132, 212, 174),
    "amarelo": (228, 184, 72),
    "vermelho": (194, 66, 62),
    "azul": (38, 114, 152),
    "card_bg": (249, 247, 242),
    "card_borda": (30, 57, 50),
    "sombra": (14, 26, 22),
}

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
    "balcao_frente": (32, 38, 44),
    "balcao_detalhe": (255, 220, 0),
    "hud_bg": (0, 0, 0),
    "hud_borda": (255, 220, 0),
    "texto_claro": (255, 255, 255),
    "texto_escuro": (0, 0, 0),
    "destaque": (255, 210, 0),
    "dourado": (255, 220, 0),
    "verde": (0, 220, 110),
    "verde_claro": (160, 255, 200),
    "amarelo": (255, 225, 0),
    "vermelho": (255, 70, 70),
    "azul": (80, 190, 255),
    "card_bg": (16, 16, 22),
    "card_borda": (255, 220, 0),
    "sombra": (0, 0, 0),
}

SINAIS_LIBRAS = {
    "oi": {
        "nome": "OI / OLA",
        "categoria": "Cumprimento",
        "estacao": "cumprimento",
        "dica_curta": "Aceno aberto ao lado do rosto",
        "cor": (0, 112, 74),
    },
    "cafe": {
        "nome": "CAFE",
        "categoria": "Bebida",
        "estacao": "cafe",
        "dica_curta": "Mao em 'C' indo ate a boca",
        "cor": (108, 68, 42),
    },
    "agua": {
        "nome": "AGUA",
        "categoria": "Bebida",
        "estacao": "agua",
        "dica_curta": "Mao em 'L' tocando o queixo",
        "cor": (32, 134, 174),
    },
    "bolo": {
        "nome": "BOLO",
        "categoria": "Comida",
        "estacao": "bolo",
        "dica_curta": "Mao cortando fatia na palma",
        "cor": (182, 86, 108),
    },
    "suco": {
        "nome": "SUCO",
        "categoria": "Bebida",
        "estacao": "suco",
        "dica_curta": "Mao espremendo fruta p/ baixo",
        "cor": (208, 134, 34),
    },
    "obrigado": {
        "nome": "OBRIGADO(A)",
        "categoria": "Cortesia",
        "estacao": "cortesia",
        "dica_curta": "Mao na testa saindo p/ frente",
        "cor": (0, 112, 74),
    },
    "pagar": {
        "nome": "CONTA / PAGAR",
        "categoria": "Servico",
        "estacao": "caixa",
        "dica_curta": "Deslizar mao sobre a palma",
        "cor": (30, 57, 50),
    },
    "banheiro": {
        "nome": "BANHEIRO",
        "categoria": "Informacao",
        "estacao": "banheiro",
        "dica_curta": "Mao em 'T' balancando o pulso",
        "cor": (96, 82, 148),
    },
}

SINAIS_ESTACAO = ["cafe", "agua", "bolo", "suco", "pagar", "banheiro"]

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
