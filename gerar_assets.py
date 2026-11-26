"""Gerador procedural de sprites 2.5D com supersampling 2x e audios WAV.

Renderiza personagens expressivos estilo cafeteria moderna (paleta verde
floresta, creme e nogueira), estacoes 2.5D com profundidade e efeitos
sonoros WAV dentro da pasta data/, preservando as ilustracoes de Libras.
"""

import math
import os
import struct
import wave

import pygame

from config import PASTA_DATA, SINAIS_LIBRAS


def _garantir_pasta() -> None:
    """Garante que a pasta data/ exista antes de salvar os assets."""
    os.makedirs(PASTA_DATA, exist_ok=True)


def _salvar_supersampled(
    superficie: pygame.Surface, nome: str, tamanho_final: tuple[int, int]
) -> None:
    """Reduz a surface de alta resolucao (2x) com anti-aliasing suave e salva."""
    final = pygame.transform.smoothscale(superficie, tamanho_final)
    pygame.image.save(final, os.path.join(PASTA_DATA, nome))


def _criar_surface(largura: int, altura: int) -> pygame.Surface:
    """Cria uma Surface transparente com suporte a canal alfa."""
    return pygame.Surface((largura, altura), pygame.SRCALPHA)


def _sombra_chao(surf: pygame.Surface, cx: int, cy: int, rx: int, ry: int) -> None:
    """Desenha sombra oval suave em duas camadas no piso."""
    pygame.draw.ellipse(
        surf, (16, 28, 24, 48), (cx - rx - 8, cy - ry - 3, (rx + 8) * 2, (ry + 3) * 2)
    )
    pygame.draw.ellipse(
        surf, (16, 28, 24, 88), (cx - rx, cy - ry, rx * 2, ry * 2)
    )


def _desenhar_rosto_charmoso(
    surf: pygame.Surface,
    cx: int,
    cy: int,
    pele: tuple,
    cabelo: tuple,
    estilo: str,
    oculos: bool = False,
    bone_verde: bool = False,
) -> None:
    """Desenha cabeca estilizada 2x supersampled com olhos brilhantes e expressao."""
    traco = (36, 26, 22)
    pele_sombra = tuple(max(0, c - 24) for c in pele)
    bochecha = (min(255, pele[0] + 18), max(0, pele[1] - 28), max(0, pele[2] - 22))
    cabelo_luz = tuple(min(255, c + 30) for c in cabelo)

    if estilo == "longo":
        pygame.draw.ellipse(surf, cabelo, (cx - 56, cy - 46, 112, 118))
        pygame.draw.ellipse(surf, traco, (cx - 56, cy - 46, 112, 118), 5)
    elif estilo == "coque":
        pygame.draw.circle(surf, cabelo, (cx, cy - 58), 22)
        pygame.draw.circle(surf, cabelo_luz, (cx - 6, cy - 64), 7)
        pygame.draw.circle(surf, traco, (cx, cy - 58), 22, 5)
    elif estilo == "cacheado":
        for ox, oy, r in (
            (-44, -22, 24),
            (44, -22, 24),
            (-48, 8, 22),
            (48, 8, 22),
            (-26, -44, 24),
            (26, -44, 24),
            (0, -48, 26),
        ):
            pygame.draw.circle(surf, cabelo, (cx + ox, cy + oy), r)
            pygame.draw.circle(surf, traco, (cx + ox, cy + oy), r, 5)

    # Orelhas
    for dx in (-46, 46):
        pygame.draw.circle(surf, pele, (cx + dx, cy + 4), 11)
        pygame.draw.circle(surf, traco, (cx + dx, cy + 4), 11, 4)

    # Cabeca com leve sombra inferior
    pygame.draw.circle(surf, pele, (cx, cy), 46)
    pygame.draw.arc(surf, pele_sombra, (cx - 44, cy - 44, 88, 88), math.pi + 0.35, 2 * math.pi - 0.35, 7)
    pygame.draw.circle(surf, traco, (cx, cy), 46, 5)

    # Bochechas rosadas suaves
    pygame.draw.ellipse(surf, bochecha, (cx - 34, cy + 8, 18, 10))
    pygame.draw.ellipse(surf, bochecha, (cx + 16, cy + 8, 18, 10))

    # Olhos expressivos com brilho duplo e sobrancelhas
    for ex in (cx - 17, cx + 17):
        pygame.draw.ellipse(surf, (255, 255, 255), (ex - 9, cy - 8, 18, 16))
        pygame.draw.circle(surf, (32, 24, 20), (ex, cy), 6)
        pygame.draw.circle(surf, (255, 255, 255), (ex - 2, cy - 2), 2)
        pygame.draw.circle(surf, (255, 255, 255), (ex + 2, cy + 2), 1)
        pygame.draw.arc(surf, traco, (ex - 11, cy - 20, 22, 12), 0.2, math.pi - 0.2, 4)

    if oculos:
        pygame.draw.rect(surf, (46, 42, 40), (cx - 31, cy - 12, 26, 22), width=4, border_radius=6)
        pygame.draw.rect(surf, (46, 42, 40), (cx + 5, cy - 12, 26, 22), width=4, border_radius=6)
        pygame.draw.line(surf, (46, 42, 40), (cx - 5, cy - 2), (cx + 5, cy - 2), 4)

    # Sorriso acolhedor
    pygame.draw.arc(surf, (132, 58, 52), (cx - 14, cy + 12, 28, 16), math.pi + 0.25, 2 * math.pi - 0.25, 4)

    # Cabelo frontal
    if estilo != "cacheado":
        pygame.draw.ellipse(surf, cabelo, (cx - 48, cy - 52, 96, 38))
        pygame.draw.ellipse(surf, cabelo_luz, (cx - 24, cy - 46, 34, 12))
        pygame.draw.ellipse(surf, traco, (cx - 48, cy - 52, 96, 38), 5)

    # Bone verde Starbucks do atendente
    if bone_verde:
        pygame.draw.arc(surf, (0, 112, 74), (cx - 48, cy - 56, 96, 56), 0.0, math.pi, 26)
        pygame.draw.ellipse(surf, (0, 112, 74), (cx - 46, cy - 56, 92, 34))
        pygame.draw.ellipse(surf, traco, (cx - 46, cy - 56, 92, 34), 5)
        pygame.draw.rect(surf, (22, 68, 52), (cx - 48, cy - 30, 96, 12), border_radius=5)
        pygame.draw.rect(surf, traco, (cx - 48, cy - 30, 96, 12), 4, border_radius=5)
        pygame.draw.circle(surf, (248, 246, 240), (cx, cy - 40), 9)
        pygame.draw.circle(surf, (0, 112, 74), (cx, cy - 40), 5)


def gerar_atendente() -> None:
    """Gera os sprites 2.5D do atendente barista estilo Starbucks (112x136)."""
    traco = (36, 26, 22)
    pele = (236, 188, 152)
    verde_sb = (0, 112, 74)
    verde_esc = (22, 76, 56)

    for passo in (0, 1):
        surf = _criar_surface(224, 272)
        _sombra_chao(surf, 112, 242, 62, 18)

        d_esq = -7 if passo == 0 else 7
        d_dir = 7 if passo == 0 else -7

        # Pernas e tenis modernos
        for px, dy in ((76, d_esq), (118, d_dir)):
            pygame.draw.rect(surf, (38, 44, 52), (px, 186 + dy, 30, 44), border_radius=8)
            pygame.draw.rect(surf, traco, (px, 186 + dy, 30, 44), 5, border_radius=8)
            pygame.draw.rect(surf, (245, 242, 235), (px - 4, 222 + dy, 38, 18), border_radius=7)
            pygame.draw.rect(surf, (30, 57, 50), (px - 4, 232 + dy, 38, 8), border_radius=4)
            pygame.draw.rect(surf, traco, (px - 4, 222 + dy, 38, 18), 4, border_radius=7)

        # Camisa polo preta/grafite moderna + avental verde Starbucks icone
        pygame.draw.rect(surf, (44, 52, 50), (58, 116, 108, 78), border_radius=22)
        pygame.draw.rect(surf, traco, (58, 116, 108, 78), 5, border_radius=22)

        # Bracos e maos
        for bx in (38, 160):
            pygame.draw.rect(surf, (44, 52, 50), (bx, 122, 26, 44), border_radius=12)
            pygame.draw.rect(surf, traco, (bx, 122, 26, 44), 5, border_radius=12)
            pygame.draw.circle(surf, pele, (bx + 13, 174), 14)
            pygame.draw.circle(surf, traco, (bx + 13, 174), 14, 5)

        # Avental verde Starbucks com alcas, bolso e emblema circular branco
        pygame.draw.rect(surf, verde_sb, (68, 124, 88, 78), border_radius=10)
        pygame.draw.rect(surf, verde_esc, (132, 124, 24, 78), border_radius=8)
        pygame.draw.rect(surf, traco, (68, 124, 88, 78), 5, border_radius=10)
        pygame.draw.line(surf, verde_sb, (82, 112), (82, 128), 9)
        pygame.draw.line(surf, verde_sb, (142, 112), (142, 128), 9)
        pygame.draw.rect(surf, verde_esc, (86, 162, 52, 26), border_radius=6)
        pygame.draw.rect(surf, traco, (86, 162, 52, 26), 4, border_radius=6)
        # Medalhao circular branco/verde no centro do peito
        pygame.draw.circle(surf, (248, 246, 240), (112, 144), 14)
        pygame.draw.circle(surf, verde_sb, (112, 144), 8)
        pygame.draw.circle(surf, (203, 162, 88), (112, 144), 14, 3)

        # Pesoco e cabeca
        pygame.draw.rect(surf, pele, (98, 96, 28, 24), border_radius=6)
        _desenhar_rosto_charmoso(
            surf, 112, 68, pele, (74, 48, 32), "curto", bone_verde=True
        )
        _salvar_supersampled(surf, f"atendente_{passo}.png", (112, 136))


def gerar_clientes() -> None:
    """Gera 4 clientes 2.5D expressivos com roupas modernas (112x136)."""
    traco = (36, 26, 22)
    perfis = [
        (0, (240, 198, 164), (72, 46, 32), (206, 148, 62), "cacheado", True),
        (1, (164, 108, 74), (30, 22, 20), (54, 118, 146), "curto", False),
        (2, (222, 174, 136), (138, 64, 38), (176, 82, 74), "longo", False),
        (3, (128, 78, 52), (26, 20, 22), (108, 84, 134), "coque", True),
    ]

    for idx, pele, cabelo, roupa, estilo, oculos in perfis:
        surf = _criar_surface(224, 272)
        _sombra_chao(surf, 112, 242, 62, 18)
        roupa_esc = tuple(max(0, c - 28) for c in roupa)

        # Calca e calcados
        for px in (78, 118):
            pygame.draw.rect(surf, (52, 60, 74), (px, 190, 28, 42), border_radius=8)
            pygame.draw.rect(surf, traco, (px, 190, 28, 42), 5, border_radius=8)
            pygame.draw.rect(surf, (62, 44, 34), (px - 3, 224, 34, 16), border_radius=6)
            pygame.draw.rect(surf, traco, (px - 3, 224, 34, 16), 4, border_radius=6)

        # Sueter / blusa casual com gola creme
        pygame.draw.rect(surf, roupa, (56, 118, 112, 80), border_radius=24)
        pygame.draw.rect(surf, roupa_esc, (140, 118, 28, 80), border_radius=14)
        pygame.draw.rect(surf, traco, (56, 118, 112, 80), 5, border_radius=24)
        pygame.draw.arc(surf, (245, 240, 232), (88, 106, 48, 28), math.pi, 2 * math.pi, 7)

        # Bracos e maos
        for bx in (36, 162):
            pygame.draw.rect(surf, roupa, (bx, 124, 26, 46), border_radius=12)
            pygame.draw.rect(surf, traco, (bx, 124, 26, 46), 5, border_radius=12)
            pygame.draw.circle(surf, pele, (bx + 13, 176), 14)
            pygame.draw.circle(surf, traco, (bx + 13, 176), 14, 5)

        pygame.draw.rect(surf, pele, (98, 98, 28, 24), border_radius=6)
        _desenhar_rosto_charmoso(surf, 112, 70, pele, cabelo, estilo, oculos=oculos)
        _salvar_supersampled(surf, f"cliente_{idx}.png", (112, 136))


def _bloco_25d(
    surf: pygame.Surface,
    x: int,
    y: int,
    w: int,
    h_topo: int,
    h_frente: int,
    cor_topo: tuple,
    cor_frente: tuple,
    cor_borda: tuple,
) -> None:
    """Desenha movel 2.5D em 2x supersampling com tampo iluminado e profundidade."""
    frente = pygame.Rect(x, y + h_topo - 4, w, h_frente)
    pygame.draw.rect(surf, cor_frente, frente)
    sombra_tampo = tuple(max(0, c - 22) for c in cor_frente)
    pygame.draw.rect(surf, sombra_tampo, (x, y + h_topo - 4, w, 12))
    pygame.draw.rect(surf, cor_borda, frente, 5)

    tampo = pygame.Rect(x - 6, y, w + 12, h_topo)
    pygame.draw.rect(surf, cor_topo, tampo)
    brilho = tuple(min(255, c + 12) for c in cor_topo)
    pygame.draw.line(
        surf, brilho, (tampo.left + 6, tampo.top + 5), (tampo.right - 7, tampo.top + 5), 4
    )
    pygame.draw.rect(surf, cor_borda, tampo, 5)


def gerar_estacoes() -> None:
    """Gera estacoes 2.5D em alta definicao (138x150) na paleta Starbucks."""
    borda = (24, 42, 36)
    nogueira = (102, 68, 44)
    verde_sb = (0, 112, 74)
    verde_esc = (30, 57, 50)
    quartzo = (246, 244, 238)

    # 1. Maquina de Cafe Espresso (inox + verde Starbucks)
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 114, 22)
    _bloco_25d(s, 30, 144, 216, 42, 86, quartzo, verde_esc, borda)
    pygame.draw.rect(s, (194, 202, 204), (54, 34, 168, 114))
    pygame.draw.rect(s, verde_sb, (54, 34, 168, 30))
    pygame.draw.rect(s, borda, (54, 34, 168, 114), 5)
    pygame.draw.rect(s, (54, 60, 64), (78, 78, 120, 58))
    pygame.draw.rect(s, (248, 246, 240), (118, 96, 40, 36))
    pygame.draw.circle(s, verde_sb, (138, 114), 9)
    pygame.draw.rect(s, borda, (118, 96, 40, 36), 4)
    pygame.draw.circle(s, (203, 162, 88), (82, 49), 8)
    pygame.draw.circle(s, (132, 212, 174), (108, 49), 8)
    _salvar_supersampled(s, "estacao_cafe.png", (138, 150))

    # 2. Estacao de Agua Filtrada
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 102, 22)
    _bloco_25d(s, 52, 124, 172, 36, 112, (238, 244, 246), (192, 206, 212), borda)
    pygame.draw.rect(s, (62, 168, 212), (76, 24, 124, 104), border_radius=24)
    pygame.draw.rect(s, (164, 226, 248), (94, 38, 30, 72), border_radius=12)
    pygame.draw.rect(s, borda, (76, 24, 124, 104), 5, border_radius=24)
    pygame.draw.rect(s, (144, 164, 174), (78, 176, 120, 44))
    pygame.draw.circle(s, (34, 118, 186), (112, 198), 11)
    pygame.draw.circle(s, (204, 72, 66), (164, 198), 11)
    _salvar_supersampled(s, "estacao_agua.png", (138, 150))

    # 3. Vitrine de Bolos e Doces
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 114, 22)
    _bloco_25d(s, 30, 154, 216, 38, 78, quartzo, nogueira, borda)
    pygame.draw.rect(s, (200, 232, 236, 180), (44, 42, 188, 118))
    pygame.draw.line(s, (255, 255, 255, 210), (66, 54), (92, 144), 9)
    pygame.draw.rect(s, (238, 198, 138), (82, 92, 112, 56))
    pygame.draw.rect(s, (214, 106, 128), (76, 78, 124, 22))
    pygame.draw.circle(s, (194, 42, 58), (138, 68), 12)
    pygame.draw.rect(s, borda, (44, 42, 188, 118), 5)
    _salvar_supersampled(s, "estacao_bolo.png", (138, 150))

    # 4. Estacao de Suco Natural
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 114, 22)
    _bloco_25d(s, 30, 150, 216, 42, 78, quartzo, nogueira, borda)
    pygame.draw.rect(s, (238, 150, 34), (94, 40, 96, 110))
    pygame.draw.rect(s, (255, 216, 118), (108, 52, 24, 84))
    pygame.draw.rect(s, verde_esc, (86, 24, 112, 20))
    pygame.draw.rect(s, borda, (94, 40, 96, 110), 5)
    pygame.draw.circle(s, (232, 126, 26), (62, 136), 22)
    pygame.draw.circle(s, borda, (62, 136), 22, 5)
    _salvar_supersampled(s, "estacao_suco.png", (138, 150))

    # 5. Caixa / Pagamento
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 114, 22)
    _bloco_25d(s, 30, 154, 216, 38, 78, quartzo, verde_esc, borda)
    pygame.draw.rect(s, (52, 62, 68), (64, 56, 148, 104))
    pygame.draw.rect(s, (78, 92, 98), (64, 56, 148, 24))
    pygame.draw.rect(s, (118, 218, 154), (84, 90, 108, 40))
    pygame.draw.rect(s, borda, (64, 56, 148, 104), 5)
    pygame.draw.rect(s, (203, 162, 88), (98, 204, 80, 20))
    _salvar_supersampled(s, "estacao_caixa.png", (138, 150))

    # 6. Porta-chaves do Banheiro 2.5D (suporte verde floresta + chave dourada)
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 98, 20)
    _bloco_25d(s, 44, 152, 188, 36, 80, quartzo, nogueira, borda)
    # Painel porta-chaves no balcao
    pygame.draw.rect(s, verde_esc, (64, 34, 148, 122))
    pygame.draw.rect(s, (203, 162, 88), (64, 34, 148, 122), 6)
    # Gancho + chave dourada pendurada + tag WC verde
    pygame.draw.circle(s, (203, 162, 88), (138, 56), 8)
    pygame.draw.circle(s, (238, 198, 86), (114, 92), 20, 7)
    pygame.draw.rect(s, (238, 198, 86), (130, 87, 46, 10))
    pygame.draw.rect(s, (238, 198, 86), (156, 97, 8, 12))
    pygame.draw.rect(s, (238, 198, 86), (168, 97, 8, 16))
    pygame.draw.rect(s, verde_sb, (88, 118, 100, 26))
    pygame.draw.rect(s, (203, 162, 88), (88, 118, 100, 26), 3)
    _salvar_supersampled(s, "estacao_banheiro.png", (138, 150))

    # 7. Mural de Libras em cavalete nogueira + moldura verde
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 110, 22)
    pygame.draw.rect(s, nogueira, (64, 214, 26, 48))
    pygame.draw.rect(s, nogueira, (186, 214, 26, 48))
    pygame.draw.rect(s, (18, 38, 32), (44, 44, 198, 182))
    pygame.draw.rect(s, verde_esc, (32, 32, 198, 182))
    pygame.draw.rect(s, (203, 162, 88), (32, 32, 198, 182), 6)
    pygame.draw.rect(s, (248, 246, 240), (50, 50, 162, 146))
    pygame.draw.rect(s, verde_sb, (62, 64, 62, 54))
    pygame.draw.rect(s, (203, 162, 88), (138, 64, 62, 54))
    pygame.draw.rect(s, (32, 134, 174), (62, 130, 62, 54))
    pygame.draw.rect(s, (182, 86, 108), (138, 130, 62, 54))
    _salvar_supersampled(s, "estacao_mural.png", (138, 150))

    # 8. Lixeira Inox / Verde Escuro
    s = _criar_surface(276, 300)
    _sombra_chao(s, 138, 266, 78, 18)
    _bloco_25d(s, 72, 92, 132, 32, 138, (164, 174, 176), (78, 92, 90), borda)
    for lx in (104, 138, 172):
        pygame.draw.line(s, (148, 162, 160), (lx, 142), (lx, 242), 6)
    _salvar_supersampled(s, "estacao_lixeira.png", (138, 150))


def gerar_itens() -> None:
    """Gera icones nitidos (52x52) dos itens carregados na bandeja."""
    borda = (28, 42, 36)
    verde_sb = (0, 112, 74)

    # Copo Starbucks de Cafe
    s = _criar_surface(104, 104)
    pygame.draw.polygon(s, (248, 246, 240), [(24, 24), (80, 24), (72, 90), (32, 90)])
    pygame.draw.rect(s, (168, 128, 86), (26, 46, 52, 24))
    pygame.draw.circle(s, verde_sb, (52, 58), 11)
    pygame.draw.rect(s, (242, 240, 234), (18, 16, 68, 12))
    pygame.draw.polygon(s, borda, [(24, 24), (80, 24), (72, 90), (32, 90)], 5)
    pygame.draw.rect(s, borda, (18, 16, 68, 12), 4)
    _salvar_supersampled(s, "item_cafe.png", (52, 52))

    # Agua
    s = _criar_surface(104, 104)
    pygame.draw.rect(s, (108, 202, 238), (28, 20, 48, 66))
    pygame.draw.rect(s, (224, 248, 255), (38, 30, 14, 42))
    pygame.draw.rect(s, borda, (28, 20, 48, 66), 5)
    _salvar_supersampled(s, "item_agua.png", (52, 52))

    # Bolo
    s = _criar_surface(104, 104)
    pygame.draw.polygon(s, (238, 194, 130), [(16, 78), (88, 78), (74, 38), (30, 38)])
    pygame.draw.rect(s, (214, 104, 128), (26, 32, 52, 16))
    pygame.draw.circle(s, (194, 40, 58), (52, 24), 10)
    pygame.draw.polygon(s, borda, [(16, 78), (88, 78), (74, 38), (30, 38)], 5)
    _salvar_supersampled(s, "item_bolo.png", (52, 52))

    # Suco
    s = _criar_surface(104, 104)
    pygame.draw.rect(s, (238, 150, 32), (28, 28, 48, 58))
    pygame.draw.rect(s, borda, (28, 28, 48, 58), 5)
    pygame.draw.line(s, verde_sb, (58, 28), (76, 10), 8)
    _salvar_supersampled(s, "item_suco.png", (52, 52))

    # Conta / Maquininha
    s = _criar_surface(104, 104)
    pygame.draw.rect(s, (56, 68, 74), (24, 16, 56, 74))
    pygame.draw.rect(s, (118, 218, 154), (34, 26, 36, 24))
    pygame.draw.rect(s, borda, (24, 16, 56, 74), 5)
    _salvar_supersampled(s, "item_pagar.png", (52, 52))

    # Chave do Banheiro (chave dourada com chaveiro verde)
    s = _criar_surface(104, 104)
    # Chaveiro verde Starbucks
    pygame.draw.rect(s, verde_sb, (10, 40, 26, 24), border_radius=5)
    pygame.draw.rect(s, borda, (10, 40, 26, 24), 4, border_radius=5)
    # Argola e cabeca da chave dourada
    pygame.draw.circle(s, (238, 196, 78), (46, 52), 16)
    pygame.draw.circle(s, borda, (46, 52), 16, 4)
    pygame.draw.circle(s, (248, 246, 240), (46, 52), 6)
    pygame.draw.circle(s, borda, (46, 52), 6, 3)
    # Haste e dentes da chave
    pygame.draw.rect(s, (238, 196, 78), (58, 46, 36, 12))
    pygame.draw.rect(s, borda, (58, 46, 36, 12), 4)
    pygame.draw.rect(s, (238, 196, 78), (72, 56, 8, 14))
    pygame.draw.rect(s, borda, (72, 56, 8, 14), 3)
    pygame.draw.rect(s, (238, 196, 78), (84, 56, 8, 18))
    pygame.draw.rect(s, borda, (84, 56, 8, 18), 3)
    _salvar_supersampled(s, "item_banheiro.png", (52, 52))


def _escrever_wav(nome: str, amostras: list[float], taxa: int = 22050) -> None:
    """Salva uma lista de amostras [-1.0, 1.0] como arquivo WAV 16-bit mono."""
    caminho = os.path.join(PASTA_DATA, nome)
    with wave.open(caminho, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(taxa)
        dados = bytearray()
        for v in amostras:
            clamped = max(-1.0, min(1.0, v))
            dados.extend(struct.pack("<h", int(clamped * 32767)))
        wav.writeframes(bytes(dados))


def _nota(freq: float, duracao: float, vol: float = 0.25, taxa: int = 22050) -> list[float]:
    """Sintetiza uma nota suave com ataque e decaimento exponencial."""
    total = int(duracao * taxa)
    saida = []
    for i in range(total):
        t = i / taxa
        env = min(1.0, t / 0.015) * math.exp(-3.5 * t / max(0.05, duracao))
        val = (
            0.75 * math.sin(2 * math.pi * freq * t)
            + 0.25 * math.sin(2 * math.pi * freq * 2 * t)
        )
        saida.append(val * env * vol)
    return saida


def gerar_audios() -> None:
    """Gera trilha sonora calma de cafeteria e efeitos sonoros em WAV."""
    acerto = _nota(523.25, 0.11, 0.28) + _nota(659.25, 0.11, 0.28) + _nota(783.99, 0.20, 0.30)
    _escrever_wav("acerto.wav", acerto)

    erro = _nota(220.0, 0.14, 0.26) + _nota(185.0, 0.22, 0.26)
    _escrever_wav("erro.wav", erro)

    pegar = _nota(440.0, 0.06, 0.24) + _nota(587.33, 0.09, 0.24)
    _escrever_wav("pegar.wav", pegar)

    campainha = _nota(1046.5, 0.16, 0.22) + _nota(1318.5, 0.24, 0.18)
    _escrever_wav("campainha.wav", campainha)

    vitoria = (
        _nota(523.25, 0.12, 0.28)
        + _nota(659.25, 0.12, 0.28)
        + _nota(783.99, 0.12, 0.28)
        + _nota(1046.5, 0.36, 0.32)
    )
    _escrever_wav("vitoria.wav", vitoria)

    acordes = [
        (261.63, 329.63, 392.00),
        (220.00, 261.63, 329.63),
        (174.61, 220.00, 261.63),
        (196.00, 246.94, 293.66),
    ]
    taxa = 22050
    musica: list[float] = []
    for f1, f2, f3 in acordes:
        dur = 2.0
        n = int(dur * taxa)
        for i in range(n):
            t = i / taxa
            env = min(1.0, t / 0.08) * (1.0 - 0.35 * (t / dur))
            onda = (
                math.sin(2 * math.pi * f1 * t)
                + 0.7 * math.sin(2 * math.pi * f2 * t)
                + 0.5 * math.sin(2 * math.pi * f3 * t)
            ) / 2.2
            musica.append(onda * env * 0.12)
    _escrever_wav("musica.wav", musica, taxa)


def gerar_fallback_sinais_libras() -> None:
    """Garante que todos os arquivos sinal_<id>.png existam em data/.

    Preserva ilustracoes ja existentes e gera cartoes de fallback nitidos
    (256x256) apenas para eventuais arquivos ausentes.
    """
    fonte_tit = pygame.font.SysFont("segoeui", 28, bold=True)
    fonte_dica = pygame.font.SysFont("segoeui", 16, bold=True)
    for sid, info in SINAIS_LIBRAS.items():
        destino = os.path.join(PASTA_DATA, f"sinal_{sid}.png")
        if os.path.exists(destino):
            continue
        surf = pygame.Surface((256, 256), pygame.SRCALPHA)
        surf.fill((244, 235, 220))
        pygame.draw.rect(surf, info["cor"], (8, 8, 240, 240), width=6)
        pygame.draw.circle(surf, info["cor"], (128, 108), 54)
        inicial = fonte_tit.render(info["nome"].split("/")[0].strip(), True, (255, 255, 255))
        if inicial.get_width() > 96:
            esc = 96 / inicial.get_width()
            inicial = pygame.transform.smoothscale(
                inicial, (96, max(1, int(inicial.get_height() * esc)))
            )
        surf.blit(inicial, inicial.get_rect(center=(128, 108)))
        dica = fonte_dica.render(info["dica_curta"], True, (36, 26, 22))
        if dica.get_width() > 224:
            esc = 224 / dica.get_width()
            dica = pygame.transform.smoothscale(
                dica, (224, max(1, int(dica.get_height() * esc)))
            )
        surf.blit(dica, dica.get_rect(center=(128, 204)))
        pygame.image.save(surf, destino)


def gerar_todos_assets() -> None:
    """Executa a geracao completa de sprites 2.5D, fallback de Libras e audios WAV."""
    pygame.init()
    _garantir_pasta()
    gerar_atendente()
    gerar_clientes()
    gerar_estacoes()
    gerar_itens()
    gerar_fallback_sinais_libras()
    gerar_audios()


if __name__ == "__main__":
    gerar_todos_assets()
    print(f"Assets 2.5D Starbucks gerados em: {PASTA_DATA}")
