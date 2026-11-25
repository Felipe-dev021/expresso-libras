"""Gerador procedural de sprites 2.5D em alta qualidade, Libras 128px e WAV.

Produz personagens 2.5D expressivos, estacoes com profundidade e volume
(tampo iluminado, face frontal e sombra projetada), ilustracoes didaticas
de Libras em 128x128 com busto e maos proporcionais, e audios WAV suaves.
"""

import math
import os
import struct
import wave

import pygame

from config import PASTA_DATA


def _garantir_pasta() -> None:
    """Garante que a pasta data/ exista antes de salvar os assets."""
    os.makedirs(PASTA_DATA, exist_ok=True)


def _salvar_png(superficie: pygame.Surface, nome: str) -> None:
    """Salva uma Surface com transparencia em data/<nome>."""
    pygame.image.save(superficie, os.path.join(PASTA_DATA, nome))


def _criar_surface(largura: int, altura: int) -> pygame.Surface:
    """Cria uma Surface transparente com suporte a canal alfa."""
    return pygame.Surface((largura, altura), pygame.SRCALPHA)


def _sombra_chao(surf: pygame.Surface, cx: int, cy: int, rx: int, ry: int) -> None:
    """Desenha uma sombra 2.5D em duas camadas suaves no piso."""
    pygame.draw.ellipse(surf, (22, 15, 11, 55), (cx - rx - 3, cy - ry - 1, (rx + 3) * 2, (ry + 1) * 2))
    pygame.draw.ellipse(surf, (22, 15, 11, 95), (cx - rx, cy - ry, rx * 2, ry * 2))


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
    """Desenha um movel/balcao 2.5D com tampo iluminado e frente sombreada."""
    # Frente (profundidade vertical)
    frente = pygame.Rect(x, y + h_topo - 2, w, h_frente)
    pygame.draw.rect(surf, cor_frente, frente)
    # Faixa de sombra logo abaixo do tampo
    sombra_tampo = tuple(max(0, c - 26) for c in cor_frente)
    pygame.draw.rect(surf, sombra_tampo, (x, y + h_topo - 2, w, 5))
    pygame.draw.rect(surf, cor_borda, frente, 2)

    # Tampo superior iluminado
    tampo = pygame.Rect(x - 2, y, w + 4, h_topo)
    pygame.draw.rect(surf, cor_topo, tampo)
    brilho = tuple(min(255, c + 16) for c in cor_topo)
    pygame.draw.line(surf, brilho, (tampo.left + 2, tampo.top + 2), (tampo.right - 3, tampo.top + 2), 2)
    pygame.draw.rect(surf, cor_borda, tampo, 2)


def gerar_atendente() -> None:
    """Gera os sprites 2.5D do atendente (68x84, 2 quadros de caminhada)."""
    contorno = (44, 30, 22)
    pele = (232, 184, 146)
    pele_sombra = (206, 154, 118)

    for passo in (0, 1):
        surf = _criar_surface(68, 84)
        _sombra_chao(surf, 34, 74, 21, 7)

        d_esq = -3 if passo == 0 else 3
        d_dir = 3 if passo == 0 else -3

        # Pernas e sapatos com volume
        pygame.draw.rect(surf, (52, 58, 76), (22, 56 + d_esq, 10, 16), border_radius=2)
        pygame.draw.rect(surf, (52, 58, 76), (36, 56 + d_dir, 10, 16), border_radius=2)
        pygame.draw.rect(surf, contorno, (22, 56 + d_esq, 10, 16), 2, border_radius=2)
        pygame.draw.rect(surf, contorno, (36, 56 + d_dir, 10, 16), 2, border_radius=2)
        pygame.draw.rect(surf, (40, 30, 24), (20, 68 + d_esq, 13, 6), border_radius=2)
        pygame.draw.rect(surf, (40, 30, 24), (35, 68 + d_dir, 13, 6), border_radius=2)

        # Tronco (camisa creme + avental verde barista com sombra lateral)
        pygame.draw.rect(surf, (248, 242, 232), (17, 32, 34, 27), border_radius=6)
        pygame.draw.rect(surf, contorno, (17, 32, 34, 27), 2, border_radius=6)

        pygame.draw.rect(surf, (44, 128, 84), (20, 35, 28, 27), border_radius=3)
        pygame.draw.rect(surf, (32, 98, 64), (40, 35, 8, 27), border_radius=2)
        pygame.draw.rect(surf, contorno, (20, 35, 28, 27), 2, border_radius=3)

        # Alcas e bolso do avental + broche dourado
        pygame.draw.line(surf, (32, 98, 64), (24, 32), (24, 37), 3)
        pygame.draw.line(surf, (32, 98, 64), (44, 32), (44, 37), 3)
        pygame.draw.rect(surf, (34, 102, 66), (26, 46, 16, 10), border_radius=2)
        pygame.draw.rect(surf, (244, 200, 74), (37, 39, 6, 6))
        pygame.draw.rect(surf, contorno, (37, 39, 6, 6), 1)

        # Bracos
        pygame.draw.rect(surf, (248, 242, 232), (10, 34, 8, 17), border_radius=3)
        pygame.draw.rect(surf, contorno, (10, 34, 8, 17), 2, border_radius=3)
        pygame.draw.rect(surf, (248, 242, 232), (50, 34, 8, 17), border_radius=3)
        pygame.draw.rect(surf, contorno, (50, 34, 8, 17), 2, border_radius=3)
        pygame.draw.circle(surf, pele, (14, 52), 5)
        pygame.draw.circle(surf, contorno, (14, 52), 5, 2)
        pygame.draw.circle(surf, pele, (54, 52), 5)
        pygame.draw.circle(surf, contorno, (54, 52), 5, 2)

        # Cabeca com sombreamento 2.5D
        pygame.draw.circle(surf, pele, (34, 20), 15)
        pygame.draw.arc(surf, pele_sombra, (19, 5, 30, 30), -0.9, 0.7, 4)
        pygame.draw.circle(surf, contorno, (34, 20), 15, 2)

        # Cabelo com volume e brilho
        pygame.draw.ellipse(surf, (76, 48, 32), (18, 4, 32, 14))
        pygame.draw.ellipse(surf, (104, 68, 46), (23, 6, 14, 5))
        pygame.draw.ellipse(surf, contorno, (18, 4, 32, 14), 2)

        # Olhos com brilho + sorriso acolhedor
        for ex in (28, 40):
            pygame.draw.circle(surf, (32, 24, 20), (ex, 20), 3)
            pygame.draw.circle(surf, (255, 255, 255), (ex - 1, 19), 1)
        pygame.draw.arc(surf, (156, 74, 60), (28, 21, 12, 8), math.pi + 0.25, 2 * math.pi - 0.25, 2)

        _salvar_png(surf, f"atendente_{passo}.png")


def gerar_clientes() -> None:
    """Gera 4 perfis diversos de clientes 2.5D expressivos (68x84)."""
    contorno = (40, 28, 22)
    perfis = [
        (0, (238, 194, 158), (64, 42, 30), (196, 86, 68), "curto"),
        (1, (162, 106, 72), (30, 22, 20), (54, 126, 186), "black"),
        (2, (218, 168, 130), (154, 76, 40), (124, 90, 174), "longo"),
        (3, (124, 76, 50), (26, 20, 22), (214, 154, 46), "coque"),
    ]

    for idx, pele, cabelo, camisa, estilo in perfis:
        surf = _criar_surface(68, 84)
        _sombra_chao(surf, 34, 74, 21, 7)

        camisa_sombra = tuple(max(0, c - 32) for c in camisa)

        # Pernas
        pygame.draw.rect(surf, (52, 58, 72), (22, 58, 9, 14), border_radius=2)
        pygame.draw.rect(surf, (52, 58, 72), (37, 58, 9, 14), border_radius=2)
        pygame.draw.rect(surf, contorno, (22, 58, 9, 14), 2, border_radius=2)
        pygame.draw.rect(surf, contorno, (37, 58, 9, 14), 2, border_radius=2)

        # Corpo / blusa com volume 2.5D
        pygame.draw.rect(surf, camisa, (16, 34, 36, 28), border_radius=6)
        pygame.draw.rect(surf, camisa_sombra, (42, 34, 10, 28), border_radius=4)
        pygame.draw.rect(surf, contorno, (16, 34, 36, 28), 2, border_radius=6)
        pygame.draw.arc(surf, (246, 240, 232), (26, 30, 16, 10), math.pi, 2 * math.pi, 3)

        # Bracos erguidos prontos para sinalizar em Libras
        pygame.draw.rect(surf, camisa, (9, 36, 8, 15), border_radius=3)
        pygame.draw.rect(surf, contorno, (9, 36, 8, 15), 2, border_radius=3)
        pygame.draw.rect(surf, camisa, (51, 36, 8, 15), border_radius=3)
        pygame.draw.rect(surf, contorno, (51, 36, 8, 15), 2, border_radius=3)
        pygame.draw.circle(surf, pele, (13, 52), 5)
        pygame.draw.circle(surf, contorno, (13, 52), 5, 2)
        pygame.draw.circle(surf, pele, (55, 52), 5)
        pygame.draw.circle(surf, contorno, (55, 52), 5, 2)

        # Cabelo traseiro
        if estilo == "longo":
            pygame.draw.rect(surf, cabelo, (16, 14, 36, 24), border_radius=8)
            pygame.draw.rect(surf, contorno, (16, 14, 36, 24), 2, border_radius=8)
        elif estilo == "coque":
            pygame.draw.circle(surf, cabelo, (34, 6), 8)
            pygame.draw.circle(surf, contorno, (34, 6), 8, 2)

        # Cabeca
        pygame.draw.circle(surf, pele, (34, 21), 15)
        pygame.draw.circle(surf, contorno, (34, 21), 15, 2)

        # Cabelo frontal
        if estilo == "black":
            pygame.draw.circle(surf, cabelo, (34, 14), 16)
            pygame.draw.circle(surf, contorno, (34, 14), 16, 2)
            pygame.draw.circle(surf, pele, (34, 22), 13)
            pygame.draw.arc(surf, contorno, (21, 9, 26, 26), math.pi + 0.1, 2 * math.pi - 0.1, 2)
        else:
            pygame.draw.ellipse(surf, cabelo, (18, 5, 32, 13))
            pygame.draw.ellipse(surf, contorno, (18, 5, 32, 13), 2)

        # Olhos com brilho e sorriso
        for ex in (28, 40):
            pygame.draw.circle(surf, (28, 22, 18), (ex, 21), 3)
            pygame.draw.circle(surf, (255, 255, 255), (ex - 1, 20), 1)
        pygame.draw.arc(surf, (136, 62, 52), (28, 23, 12, 7), math.pi + 0.25, 2 * math.pi - 0.25, 2)

        _salvar_png(surf, f"cliente_{idx}.png")


def gerar_estacoes() -> None:
    """Gera sprites 2.5D detalhados (84x92) para todas as estacoes da cafeteria."""
    borda = (54, 36, 24)
    madeira = (128, 84, 54)
    tampo = (244, 236, 224)

    # 1. Maquina de Cafe Espresso 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 36, 7)
    _bloco_25d(s, 10, 44, 64, 14, 26, tampo, madeira, borda)
    # Corpo da maquina vermelha + inox
    pygame.draw.rect(s, (184, 52, 44), (18, 12, 48, 34))
    pygame.draw.rect(s, (214, 78, 66), (18, 12, 48, 8))
    pygame.draw.rect(s, borda, (18, 12, 48, 34), 2)
    pygame.draw.rect(s, (66, 68, 76), (25, 24, 34, 18))
    pygame.draw.rect(s, (248, 244, 236), (36, 30, 12, 11))
    pygame.draw.rect(s, borda, (36, 30, 12, 11), 1)
    pygame.draw.circle(s, (242, 202, 68), (26, 17), 3)
    pygame.draw.circle(s, (82, 208, 124), (35, 17), 3)
    _salvar_png(s, "estacao_cafe.png")

    # 2. Estacao de Agua Gelada 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 32, 7)
    _bloco_25d(s, 16, 38, 52, 12, 34, (236, 242, 248), (196, 210, 224), borda)
    # Galao translucido com brilho
    pygame.draw.rect(s, (74, 176, 232), (24, 8, 36, 32), border_radius=8)
    pygame.draw.rect(s, (164, 226, 255), (29, 12, 10, 22), border_radius=4)
    pygame.draw.rect(s, borda, (24, 8, 36, 32), 2, border_radius=8)
    pygame.draw.rect(s, (150, 168, 188), (24, 54, 36, 14))
    pygame.draw.circle(s, (36, 112, 198), (34, 60), 4)
    pygame.draw.circle(s, (214, 68, 62), (50, 60), 4)
    _salvar_png(s, "estacao_agua.png")

    # 3. Vitrine de Bolos 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 36, 7)
    _bloco_25d(s, 10, 48, 64, 12, 24, tampo, madeira, borda)
    # Cupula de vidro 2.5D
    pygame.draw.rect(s, (196, 232, 244, 185), (14, 14, 56, 36))
    pygame.draw.line(s, (255, 255, 255, 210), (20, 18), (28, 44), 3)
    # Bolo dentro da vitrine
    pygame.draw.rect(s, (238, 194, 130), (24, 28, 36, 18))
    pygame.draw.rect(s, (224, 104, 130), (22, 24, 40, 8))
    pygame.draw.circle(s, (206, 40, 58), (42, 21), 4)
    pygame.draw.rect(s, borda, (14, 14, 56, 36), 2)
    _salvar_png(s, "estacao_bolo.png")

    # 4. Estacao de Suco Natural 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 36, 7)
    _bloco_25d(s, 10, 46, 64, 14, 24, tampo, madeira, borda)
    # Suqueira de vidro com suco de laranja
    pygame.draw.rect(s, (242, 152, 34), (28, 12, 30, 34))
    pygame.draw.rect(s, (255, 214, 108), (32, 16, 8, 26))
    pygame.draw.rect(s, (108, 72, 46), (26, 8, 34, 6))
    pygame.draw.rect(s, borda, (28, 12, 30, 34), 2)
    # Laranjas no balcao
    pygame.draw.circle(s, (238, 126, 24), (20, 42), 7)
    pygame.draw.circle(s, borda, (20, 42), 7, 2)
    _salvar_png(s, "estacao_suco.png")

    # 5. Caixa / Conta 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 36, 7)
    _bloco_25d(s, 10, 48, 64, 12, 24, tampo, madeira, borda)
    # Terminal de caixa com visor verde
    pygame.draw.rect(s, (68, 76, 88), (20, 18, 44, 32))
    pygame.draw.rect(s, (92, 102, 116), (20, 18, 44, 8))
    pygame.draw.rect(s, (104, 218, 134), (26, 28, 32, 12))
    pygame.draw.rect(s, borda, (20, 18, 44, 32), 2)
    pygame.draw.rect(s, (218, 174, 58), (30, 62, 24, 7))
    _salvar_png(s, "estacao_caixa.png")

    # 6. Totem / Placa de Banheiro 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 28, 6)
    pygame.draw.rect(s, (92, 66, 48), (37, 46, 10, 34))
    pygame.draw.rect(s, borda, (37, 46, 10, 34), 2)
    # Placa com profundidade
    pygame.draw.rect(s, (82, 58, 146), (16, 16, 56, 36))
    pygame.draw.rect(s, (118, 86, 184), (12, 12, 56, 36))
    pygame.draw.rect(s, (246, 242, 254), (12, 12, 56, 36), 2)
    # Pictograma WC
    pygame.draw.circle(s, (255, 255, 255), (29, 23), 4)
    pygame.draw.rect(s, (255, 255, 255), (25, 28, 8, 13))
    pygame.draw.circle(s, (255, 255, 255), (50, 23), 4)
    pygame.draw.polygon(s, (255, 255, 255), [(50, 28), (44, 41), (56, 41)])
    _salvar_png(s, "estacao_banheiro.png")

    # 7. Mural de Libras 2.5D (Cavalete / Quadro de Madeira)
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 34, 7)
    pygame.draw.rect(s, (98, 64, 40), (14, 14, 60, 56))
    pygame.draw.rect(s, (132, 86, 52), (10, 10, 60, 56))
    pygame.draw.rect(s, borda, (10, 10, 60, 56), 2)
    pygame.draw.rect(s, (248, 242, 228), (16, 16, 48, 44))
    # Cartoes coloridos de Libras no mural
    pygame.draw.rect(s, (48, 122, 184), (20, 20, 18, 16))
    pygame.draw.rect(s, (214, 124, 48), (42, 20, 18, 16))
    pygame.draw.rect(s, (46, 142, 92), (20, 40, 18, 16))
    pygame.draw.rect(s, (118, 86, 176), (42, 40, 18, 16))
    pygame.draw.rect(s, (98, 64, 40), (20, 66, 8, 14))
    pygame.draw.rect(s, (98, 64, 40), (52, 66, 8, 14))
    _salvar_png(s, "estacao_mural.png")

    # 8. Lixeira 2.5D
    s = _criar_surface(84, 92)
    _sombra_chao(s, 42, 82, 24, 6)
    _bloco_25d(s, 22, 28, 40, 10, 42, (148, 156, 166), (104, 112, 124), borda)
    for lx in (32, 42, 52):
        pygame.draw.line(s, (166, 174, 184), (lx, 44), (lx, 74), 2)
    _salvar_png(s, "estacao_lixeira.png")


def gerar_itens() -> None:
    """Gera os mini icones nitidos (32x32) dos itens carregados na bandeja."""
    borda = (48, 34, 24)

    # Cafe
    s = _criar_surface(32, 32)
    pygame.draw.rect(s, (250, 246, 238), (6, 10, 16, 15))
    pygame.draw.rect(s, (112, 62, 32), (8, 11, 12, 4))
    pygame.draw.rect(s, borda, (6, 10, 16, 15), 2)
    pygame.draw.rect(s, borda, (22, 13, 5, 9), 2)
    _salvar_png(s, "item_cafe.png")

    # Agua
    s = _criar_surface(32, 32)
    pygame.draw.rect(s, (112, 204, 248), (9, 7, 14, 19))
    pygame.draw.rect(s, (226, 248, 255), (12, 10, 4, 12))
    pygame.draw.rect(s, borda, (9, 7, 14, 19), 2)
    _salvar_png(s, "item_agua.png")

    # Bolo
    s = _criar_surface(32, 32)
    pygame.draw.polygon(s, (238, 192, 128), [(5, 24), (27, 24), (23, 12), (9, 12)])
    pygame.draw.rect(s, (224, 102, 130), (8, 10, 16, 5))
    pygame.draw.circle(s, (206, 40, 58), (16, 8), 3)
    pygame.draw.polygon(s, borda, [(5, 24), (27, 24), (23, 12), (9, 12)], 2)
    _salvar_png(s, "item_bolo.png")

    # Suco
    s = _criar_surface(32, 32)
    pygame.draw.rect(s, (244, 152, 32), (9, 9, 14, 17))
    pygame.draw.rect(s, borda, (9, 9, 14, 17), 2)
    pygame.draw.line(s, (56, 162, 86), (18, 9), (23, 3), 3)
    _salvar_png(s, "item_suco.png")

    # Conta / Maquininha
    s = _criar_surface(32, 32)
    pygame.draw.rect(s, (74, 84, 98), (8, 5, 16, 22))
    pygame.draw.rect(s, (108, 224, 140), (11, 8, 10, 7))
    pygame.draw.rect(s, borda, (8, 5, 16, 22), 2)
    _salvar_png(s, "item_pagar.png")

    # Banheiro / Placa
    s = _criar_surface(32, 32)
    pygame.draw.rect(s, (118, 86, 184), (5, 7, 22, 18))
    pygame.draw.rect(s, borda, (5, 7, 22, 18), 2)
    pygame.draw.polygon(s, (255, 255, 255), [(11, 16), (20, 11), (20, 21)])
    _salvar_png(s, "item_banheiro.png")


def _desenhar_seta_grande(
    surf: pygame.Surface,
    inicio: tuple[int, int],
    fim: tuple[int, int],
    cor: tuple[int, int, int],
    espessura: int = 5,
) -> None:
    """Desenha uma seta didatica nitida indicando direcao do gesto em Libras."""
    pygame.draw.line(surf, cor, inicio, fim, espessura)
    ang = math.atan2(fim[1] - inicio[1], fim[0] - inicio[0])
    ponta = [
        fim,
        (
            fim[0] + int(13 * math.cos(ang + 2.55)),
            fim[1] + int(13 * math.sin(ang + 2.55)),
        ),
        (
            fim[0] + int(13 * math.cos(ang - 2.55)),
            fim[1] + int(13 * math.sin(ang - 2.55)),
        ),
    ]
    pygame.draw.polygon(surf, cor, ponta)


def _desenhar_rosto_ref(surf: pygame.Surface, cx: int, cy: int) -> None:
    """Desenha um rosto estilizado claro como ponto de articulacao do sinal."""
    pele_ref = (242, 222, 204)
    traco = (138, 108, 88)
    # Ombros suaves
    pygame.draw.ellipse(surf, (218, 206, 192), (cx - 34, cy + 28, 68, 36))
    pygame.draw.ellipse(surf, traco, (cx - 34, cy + 28, 68, 36), 2)
    # Cabeca
    pygame.draw.circle(surf, pele_ref, (cx, cy), 26)
    pygame.draw.circle(surf, traco, (cx, cy), 26, 2)
    # Olhos e sorriso sereno
    pygame.draw.circle(surf, traco, (cx - 9, cy - 3), 3)
    pygame.draw.circle(surf, traco, (cx + 9, cy - 3), 3)
    pygame.draw.arc(surf, traco, (cx - 9, cy + 4, 18, 10), math.pi + 0.25, 2 * math.pi - 0.25, 2)


def _mao_aberta(surf: pygame.Surface, cx: int, cy: int, pele: tuple, traco: tuple) -> None:
    """Desenha uma mao aberta legivel (palma + 4 dedos + polegar)."""
    # 4 dedos
    for dx, alt in [(-12, -26), (-4, -30), (4, -29), (12, -23)]:
        pygame.draw.rect(surf, pele, (cx + dx - 3, cy + alt, 7, 26), border_radius=3)
        pygame.draw.rect(surf, traco, (cx + dx - 3, cy + alt, 7, 26), 2, border_radius=3)
    # Polegar lateral
    pygame.draw.rect(surf, pele, (cx - 22, cy - 6, 12, 8), border_radius=4)
    pygame.draw.rect(surf, traco, (cx - 22, cy - 6, 12, 8), 2, border_radius=4)
    # Palma
    pygame.draw.rect(surf, pele, (cx - 15, cy - 8, 31, 26), border_radius=8)
    pygame.draw.rect(surf, traco, (cx - 15, cy - 8, 31, 26), 2, border_radius=8)


def gerar_sinais_libras() -> None:
    """Gera 2 quadros animados em alta definicao (128x128) para cada sinal de Libras."""
    pele = (238, 186, 146)
    traco = (64, 40, 26)
    seta = (216, 86, 36)

    for quadro in (0, 1):
        # 1. OI / OLA — rosto + mao aberta acenando ao lado
        s = _criar_surface(128, 128)
        _desenhar_rosto_ref(s, 44, 62)
        hx = 90 + (-7 if quadro == 0 else 7)
        _mao_aberta(s, hx, 64, pele, traco)
        _desenhar_seta_grande(s, (68, 22), (86, 16), seta, 4)
        _desenhar_seta_grande(s, (114, 22), (96, 16), seta, 4)
        _salvar_png(s, f"sinal_oi_{quadro}.png")

        # 2. CAFE — rosto + mao em 'C' levando xicara a boca
        s = _criar_surface(128, 128)
        _desenhar_rosto_ref(s, 42, 60)
        mx = 84 + (6 if quadro == 0 else -12)
        my = 76 + (6 if quadro == 0 else -10)
        # Mao em C bem nitida
        pygame.draw.arc(s, traco, (mx - 22, my - 22, 44, 44), 0.75, 5.5, 13)
        pygame.draw.arc(s, pele, (mx - 19, my - 19, 38, 38), 0.75, 5.5, 9)
        _desenhar_seta_grande(s, (98, 102), (66, 74), seta, 5)
        _salvar_png(s, f"sinal_cafe_{quadro}.png")

        # 3. AGUA — rosto + mao em 'L' tocando o queixo
        s = _criar_surface(128, 128)
        _desenhar_rosto_ref(s, 46, 48)
        my = 80 + (6 if quadro == 0 else -6)
        # Punho + indicador reto p/ cima + polegar em L no queixo
        pygame.draw.rect(s, pele, (62, my, 28, 28), border_radius=7)
        pygame.draw.rect(s, traco, (62, my, 28, 28), 2, border_radius=7)
        # Indicador para cima
        pygame.draw.rect(s, pele, (78, my - 30, 11, 34), border_radius=5)
        pygame.draw.rect(s, traco, (78, my - 30, 11, 34), 2, border_radius=5)
        # Polegar horizontal tocando o queixo
        pygame.draw.rect(s, pele, (42, my + 2, 26, 11), border_radius=5)
        pygame.draw.rect(s, traco, (42, my + 2, 26, 11), 2, border_radius=5)
        _desenhar_seta_grande(s, (32, 108), (44, 84), seta, 5)
        _salvar_png(s, f"sinal_agua_{quadro}.png")

        # 4. BOLO — palma de base + mao cortando fatia de cima p/ baixo
        s = _criar_surface(128, 128)
        # Mao esquerda aberta de base
        pygame.draw.ellipse(s, pele, (20, 78, 86, 28))
        pygame.draw.ellipse(s, traco, (20, 78, 86, 28), 3)
        # Mao direita de lado (fatiando)
        fy = 24 + (0 if quadro == 0 else 22)
        pygame.draw.rect(s, pele, (54, fy, 18, 46), border_radius=7)
        pygame.draw.rect(s, traco, (54, fy, 18, 46), 3, border_radius=7)
        _desenhar_seta_grande(s, (92, 24), (92, 68), seta, 5)
        _salvar_png(s, f"sinal_bolo_{quadro}.png")

        # 5. SUCO — mao espremendo fruta sobre a outra mao em copo
        s = _criar_surface(128, 128)
        # Mao inferior em formato de copo/palma
        pygame.draw.ellipse(s, pele, (26, 86, 76, 24))
        pygame.draw.ellipse(s, traco, (26, 86, 76, 24), 3)
        # Mao superior abrindo/fechando (espremendo)
        raio = 23 if quadro == 0 else 16
        pygame.draw.circle(s, pele, (64, 46), raio)
        pygame.draw.circle(s, traco, (64, 46), raio, 3)
        # Dedos dobrados no punho
        pygame.draw.line(s, traco, (56, 36), (56, 54), 2)
        pygame.draw.line(s, traco, (64, 34), (64, 56), 2)
        pygame.draw.line(s, traco, (72, 36), (72, 54), 2)
        if quadro == 1:
            pygame.draw.circle(s, (238, 148, 28), (58, 72), 4)
            pygame.draw.circle(s, (238, 148, 28), (70, 76), 4)
        _desenhar_seta_grande(s, (16, 46), (36, 46), seta, 4)
        _desenhar_seta_grande(s, (112, 46), (92, 46), seta, 4)
        _salvar_png(s, f"sinal_suco_{quadro}.png")

        # 6. OBRIGADO(A) — rosto + mao saindo da testa para frente
        s = _criar_surface(128, 128)
        _desenhar_rosto_ref(s, 40, 62)
        mx = 58 + (0 if quadro == 0 else 28)
        my = 34 + (0 if quadro == 0 else 18)
        pygame.draw.rect(s, pele, (mx, my, 34, 18), border_radius=7)
        pygame.draw.rect(s, traco, (mx, my, 34, 18), 3, border_radius=7)
        _desenhar_seta_grande(s, (64, 62), (104, 86), seta, 5)
        _salvar_png(s, f"sinal_obrigado_{quadro}.png")

        # 7. CONTA / PAGAR — mao deslizando para frente sobre a palma aberta
        s = _criar_surface(128, 128)
        # Palma esquerda aberta
        pygame.draw.ellipse(s, pele, (16, 74, 84, 30))
        pygame.draw.ellipse(s, traco, (16, 74, 84, 30), 3)
        # Mao direita deslizando sobre a palma
        mx = 24 + (0 if quadro == 0 else 38)
        pygame.draw.rect(s, pele, (mx, 44, 38, 22), border_radius=8)
        pygame.draw.rect(s, traco, (mx, 44, 38, 22), 3, border_radius=8)
        _desenhar_seta_grande(s, (24, 26), (98, 26), seta, 5)
        _salvar_png(s, f"sinal_pagar_{quadro}.png")

        # 8. BANHEIRO — mao em 'T' (polegar entre dedos) balancando no pulso
        s = _criar_surface(128, 128)
        cx = 64 + (-10 if quadro == 0 else 10)
        # Antebraco/pulso
        pygame.draw.rect(s, pele, (cx - 12, 76, 24, 24), border_radius=5)
        pygame.draw.rect(s, traco, (cx - 12, 76, 24, 24), 3, border_radius=5)
        # Punho fechado em 'T'
        pygame.draw.rect(s, pele, (cx - 22, 32, 44, 48), border_radius=12)
        pygame.draw.rect(s, traco, (cx - 22, 32, 44, 48), 3, border_radius=12)
        pygame.draw.line(s, traco, (cx - 8, 34), (cx - 8, 60), 3)
        pygame.draw.line(s, traco, (cx + 8, 34), (cx + 8, 60), 3)
        # Polegar aparecendo entre indicador e medio
        pygame.draw.circle(s, (248, 206, 172), (cx - 1, 56), 9)
        pygame.draw.circle(s, traco, (cx - 1, 56), 9, 3)
        _desenhar_seta_grande(s, (16, 108), (44, 108), seta, 4)
        _desenhar_seta_grande(s, (112, 108), (84, 108), seta, 4)
        _salvar_png(s, f"sinal_banheiro_{quadro}.png")


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


def gerar_todos_assets() -> None:
    """Executa a geracao completa de sprites 2.5D e audios WAV em data/.

    Preserva ilustracoes desenhadas (sinal_<id>.png) ja existentes em data/.
    """
    pygame.init()
    _garantir_pasta()
    gerar_atendente()
    gerar_clientes()
    gerar_estacoes()
    gerar_itens()
    if not os.path.exists(os.path.join(PASTA_DATA, "sinal_oi.png")):
        gerar_sinais_libras()
    gerar_audios()


if __name__ == "__main__":
    gerar_todos_assets()
    print(f"Assets 2.5D gerados com sucesso em: {PASTA_DATA}")
