"""Interface grafica 2.5D, menus quadrados autorais, HUD e Mural de Libras.

Implementa identidade visual editorial de cafeteria artesanal brasileira:
paineis quadrados com sombra solida deslocada, moldura dupla, cenario 2.5D
com luz solar obliqua, azulejos, prateleiras e briefing educativo animado.
"""

from typing import Dict, List

import pygame

from config import (
    ALTURA,
    BALCAO_ALTURA,
    BALCAO_Y,
    HUD_ALTURA,
    LARGURA,
    PALETA_ALTO_CONTRASTE,
    PALETA_PADRAO,
    SINAIS_LIBRAS,
    VIDAS_INICIAIS,
)
from fase import GerenciadorFases
from libras import BibliotecaLibras


class InterfaceHUD:
    """Gerencia fontes adaptaveis, cache 2.5D do cenario e telas autorais."""

    def __init__(self) -> None:
        """Inicializa fontes e caches de fundo para as duas paletas."""
        self.alto_contraste = False
        self.fonte_grande = False
        self._cache_cenario: Dict[bool, pygame.Surface] = {}
        self.botoes_clicaveis: Dict[str, pygame.Rect] = {}
        self._carregar_fontes()

    @property
    def paleta(self) -> dict:
        """Retorna a paleta ativa (padrao artesanal ou alto contraste)."""
        return PALETA_ALTO_CONTRASTE if self.alto_contraste else PALETA_PADRAO

    def _carregar_fontes(self) -> None:
        """Carrega hierarquia tipografica ajustada ao modo de fonte grande."""
        delta = 4 if self.fonte_grande else 0
        self.f_titulo = pygame.font.SysFont("georgia", 38 + delta, bold=True)
        self.f_sub = pygame.font.SysFont("segoeui", 20 + delta, bold=True)
        self.f_corpo = pygame.font.SysFont("segoeui", 16 + delta)
        self.f_hud = pygame.font.SysFont("segoeui", 15 + delta, bold=True)
        self.f_peq = pygame.font.SysFont("segoeui", 12 + min(3, delta), bold=True)
        self.f_flutuante = pygame.font.SysFont("segoeui", 17 + delta, bold=True)

    def alternar_contraste(self) -> None:
        """Alterna entre paleta artesanal padrao e modo de alto contraste."""
        self.alto_contraste = not self.alto_contraste

    def alternar_fonte(self) -> None:
        """Alterna o tamanho das fontes para maior legibilidade."""
        self.fonte_grande = not self.fonte_grande
        self._carregar_fontes()

    def _desenhar_painel_editorial(
        self,
        tela: pygame.Surface,
        ret: pygame.Rect,
        cor_borda: tuple,
        cor_faixa: tuple | None = None,
        altura_faixa: int = 10,
    ) -> None:
        """Desenha um painel quadrado autoral com sombra solida e moldura dupla."""
        p = self.paleta
        # Sombra projetada solida deslocada (estetica poster/editorial)
        pygame.draw.rect(tela, p["sombra"], ret.move(8, 8))
        pygame.draw.rect(tela, p["card_bg"], ret)
        if cor_faixa is not None:
            pygame.draw.rect(tela, cor_faixa, (ret.x, ret.y, ret.width, altura_faixa))
        pygame.draw.rect(tela, cor_borda, ret, width=3)
        # Moldura interna fina
        interna = ret.inflate(-12, -12)
        pygame.draw.rect(tela, p["card_borda"], interna, width=1)

    def _desenhar_botao(
        self,
        tela: pygame.Surface,
        chave: str,
        texto: str,
        ret: pygame.Rect,
        cor_bg: tuple,
        cor_txt: tuple,
    ) -> None:
        """Desenha um botao quadrado clicavel com sombra solida e efeito hover."""
        mouse = pygame.mouse.get_pos()
        hover = ret.collidepoint(mouse)
        desloc = (2, 2) if hover else (4, 4)
        cor_final = tuple(min(255, c + 16) for c in cor_bg) if hover else cor_bg

        pygame.draw.rect(tela, self.paleta["sombra"], ret.move(*desloc))
        ret_draw = ret.move(1, 1) if hover else ret
        pygame.draw.rect(tela, cor_final, ret_draw)
        pygame.draw.rect(tela, self.paleta["card_borda"], ret_draw, width=2)
        # Detalhe luminoso no topo do botao
        brilho = tuple(min(255, c + 30) for c in cor_final)
        pygame.draw.line(
            tela,
            brilho,
            (ret_draw.left + 2, ret_draw.top + 2),
            (ret_draw.right - 3, ret_draw.top + 2),
            2,
        )
        lbl = self.f_sub.render(texto, True, cor_txt)
        tela.blit(lbl, lbl.get_rect(center=ret_draw.center))
        self.botoes_clicaveis[chave] = ret

    def _criar_cenario_cache(self, contraste: bool) -> pygame.Surface:
        """Pre-renderiza o cenario 2.5D da cafeteria com luz, azulejos e profundidade."""
        p = PALETA_ALTO_CONTRASTE if contraste else PALETA_PADRAO
        surf = pygame.Surface((LARGURA, ALTURA))
        surf.fill(p["fundo"])

        # 1. Parede superior com padrao de azulejos artesanais
        parede_ret = pygame.Rect(0, HUD_ALTURA, LARGURA, BALCAO_Y - HUD_ALTURA)
        pygame.draw.rect(surf, p["parede"], parede_ret)
        for ay in range(HUD_ALTURA + 24, BALCAO_Y, 24):
            pygame.draw.line(surf, p["parede_azulejo"], (0, ay), (LARGURA, ay), 1)
            desloc = 24 if ((ay // 24) % 2 == 0) else 0
            for ax in range(desloc, LARGURA, 48):
                pygame.draw.line(surf, p["parede_azulejo"], (ax, ay), (ax, ay + 24), 1)
        pygame.draw.rect(surf, p["parede_sombra"], (0, HUD_ALTURA, LARGURA, 14))

        # 2. Quadro-negro autoral "EXPRESSO LIBRAS" na parede central
        quadro = pygame.Rect(422, HUD_ALTURA + 18, 186, 72)
        pygame.draw.rect(surf, p["sombra"], quadro.move(4, 4))
        pygame.draw.rect(surf, (32, 42, 38) if not contraste else (0, 0, 0), quadro)
        pygame.draw.rect(surf, p["rodape"] if not contraste else p["hud_borda"], quadro, 4)
        f_q1 = pygame.font.SysFont("georgia", 15, bold=True)
        f_q2 = pygame.font.SysFont("segoeui", 11, bold=True)
        t_q1 = f_q1.render("EXPRESSO LIBRAS", True, p["amarelo"])
        t_q2 = f_q2.render("CAFE INCLUSIVO", True, (240, 236, 226))
        surf.blit(t_q1, t_q1.get_rect(center=(quadro.centerx, quadro.top + 26)))
        surf.blit(t_q2, t_q2.get_rect(center=(quadro.centerx, quadro.top + 48)))

        # 3. Janelas amplas com moldura 2.5D e brilho celeste
        for jx in (254, 652):
            janela = pygame.Rect(jx, HUD_ALTURA + 18, 136, 68)
            pygame.draw.rect(surf, p["parede_sombra"], janela.move(3, 3))
            cor_vidro = (30, 44, 66) if contraste else (186, 224, 240)
            pygame.draw.rect(surf, cor_vidro, janela)
            if not contraste:
                # Reflexo diagonal no vidro
                pygame.draw.polygon(
                    surf,
                    (220, 244, 252),
                    [
                        (janela.left + 12, janela.top + 4),
                        (janela.left + 44, janela.top + 4),
                        (janela.left + 18, janela.bottom - 4),
                        (janela.left + 4, janela.bottom - 4),
                    ],
                )
            cor_mold = p["hud_borda"] if contraste else p["rodape"]
            pygame.draw.rect(surf, cor_mold, janela, 4)
            pygame.draw.line(
                surf, cor_mold, (janela.centerx, janela.top), (janela.centerx, janela.bottom), 3
            )
            pygame.draw.line(
                surf, cor_mold, (janela.left, janela.centery), (janela.right, janela.centery), 3
            )

        # 4. Prateleira 2.5D com potes de cafe a direita
        prat = pygame.Rect(838, HUD_ALTURA + 58, 134, 10)
        pygame.draw.rect(surf, p["sombra"], prat.move(3, 4))
        pygame.draw.rect(surf, p["rodape"] if not contraste else p["hud_borda"], prat)
        for px, cor_pote in ((852, (168, 86, 52)), (884, (58, 146, 98)), (916, (214, 152, 54)), (946, (240, 232, 220))):
            pygame.draw.rect(surf, cor_pote, (px, HUD_ALTURA + 34, 20, 24))
            pygame.draw.rect(surf, p["sombra"], (px, HUD_ALTURA + 34, 20, 24), 2)
            pygame.draw.rect(surf, p["rodape"], (px - 2, HUD_ALTURA + 30, 24, 5))

        # 5. Porta de entrada a esquerda com tapete 2.5D
        porta = pygame.Rect(52, HUD_ALTURA + 14, 88, 118)
        cor_porta = (36, 44, 58) if contraste else (136, 92, 60)
        cor_borda_p = p["hud_borda"] if contraste else p["rodape"]
        pygame.draw.rect(surf, cor_porta, porta)
        pygame.draw.rect(surf, cor_borda_p, porta, 4)
        pygame.draw.rect(
            surf,
            (108, 184, 214) if not contraste else (48, 66, 92),
            (64, HUD_ALTURA + 26, 64, 48),
        )
        placa = pygame.Rect(70, HUD_ALTURA + 42, 52, 18)
        pygame.draw.rect(surf, p["verde"], placa)
        pygame.draw.rect(surf, p["sombra"], placa, 1)
        f_mini = pygame.font.SysFont("segoeui", 10, bold=True)
        txt_ab = f_mini.render("ABERTO", True, (255, 255, 255))
        surf.blit(txt_ab, txt_ab.get_rect(center=placa.center))

        # Tapete de entrada
        pygame.draw.rect(surf, p["destaque"], (56, BALCAO_Y - 36, 80, 26))
        pygame.draw.rect(surf, cor_borda_p, (56, BALCAO_Y - 36, 80, 26), 2)

        # 6. Piso de madeira 2.5D com tabuas alternadas
        piso_y = BALCAO_Y + BALCAO_ALTURA - 6
        altura_tabua = 28
        for idx, y in enumerate(range(piso_y, ALTURA, altura_tabua)):
            cor = p["piso_claro"] if idx % 2 == 0 else p["piso_escuro"]
            pygame.draw.rect(surf, cor, (0, y, LARGURA, altura_tabua))
            pygame.draw.line(surf, p["piso_linha"], (0, y), (LARGURA, y), 1)
            desloc = (idx % 3) * 86
            for x in range(desloc, LARGURA, 196):
                pygame.draw.line(surf, p["piso_linha"], (x, y), (x, y + altura_tabua), 1)

        # Feixes de luz solar obliquos (apenas no modo padrao, para atmosfera acolhedora)
        if not contraste:
            luz = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            for jx in (254, 652):
                feixe = [
                    (jx, BALCAO_Y + BALCAO_ALTURA),
                    (jx + 136, BALCAO_Y + BALCAO_ALTURA),
                    (jx + 60, ALTURA - 38),
                    (jx - 76, ALTURA - 38),
                ]
                pygame.draw.polygon(luz, (255, 244, 204, 34), feixe)
            surf.blit(luz, (0, 0))

        # 7. Laterais arquitetonicas e barra de rodape
        cor_borda_salao = (12, 12, 16) if contraste else p["rodape"]
        pygame.draw.rect(surf, cor_borda_salao, (0, piso_y, 56, ALTURA - piso_y))
        pygame.draw.rect(surf, cor_borda_salao, (LARGURA - 56, piso_y, 56, ALTURA - piso_y))
        pygame.draw.rect(surf, cor_borda_salao, (0, ALTURA - 38, LARGURA, 38))
        pygame.draw.line(surf, p["hud_borda"], (0, ALTURA - 38), (LARGURA, ALTURA - 38), 2)

        # Plantas 2.5D nos cantos do salao
        for px, py in ((28, 304), (28, 560), (LARGURA - 28, 304)):
            pygame.draw.rect(surf, (152, 82, 50), (px - 12, py + 2, 24, 18))
            pygame.draw.rect(surf, (116, 60, 36), (px - 14, py, 28, 6))
            pygame.draw.circle(surf, (44, 124, 68), (px - 6, py - 5), 11)
            pygame.draw.circle(surf, (66, 164, 92), (px + 6, py - 7), 10)
            pygame.draw.circle(surf, (88, 186, 110), (px, py - 13), 9)

        # 8. Balcao 2.5D com sombra projetada no piso, frente ripada e tampo de marmore
        sombra_balcao = pygame.Surface((LARGURA - 112, 16), pygame.SRCALPHA)
        sombra_balcao.fill((18, 12, 8, 95))
        surf.blit(sombra_balcao, (56, BALCAO_Y + BALCAO_ALTURA + 6))

        pygame.draw.rect(
            surf, p["balcao_frente"], (56, BALCAO_Y + 14, LARGURA - 112, BALCAO_ALTURA - 4)
        )
        # Sombra logo abaixo do beiral do tampo
        pygame.draw.rect(
            surf, p["balcao_detalhe"], (56, BALCAO_Y + 14, LARGURA - 112, 7)
        )
        # Ripas verticais 2.5D na frente do balcao
        for rx in range(72, LARGURA - 68, 22):
            pygame.draw.line(
                surf,
                p["balcao_detalhe"],
                (rx, BALCAO_Y + 22),
                (rx, BALCAO_Y + BALCAO_ALTURA + 8),
                2,
            )
        pygame.draw.rect(
            surf, p["balcao_detalhe"], (56, BALCAO_Y + 14, LARGURA - 112, BALCAO_ALTURA - 4), 2
        )
        # Tampo de marmore claro
        pygame.draw.rect(surf, p["balcao_topo"], (50, BALCAO_Y, LARGURA - 100, 16))
        pygame.draw.rect(surf, p["balcao_detalhe"], (50, BALCAO_Y, LARGURA - 100, 16), 2)

        # Rodape de controles rapidos
        f_bar = pygame.font.SysFont("segoeui", 12, bold=True)
        dica = (
            "[WASD/Setas] Mover  [SHIFT] Correr  [E/ESPACO] Interagir  "
            "[TAB] Mural  [F11] Tela Cheia  [C] Contraste  [F] Fonte  [M] Som  [P] Pausa"
        )
        txt = f_bar.render(dica, True, p["texto_claro"])
        surf.blit(txt, txt.get_rect(center=(LARGURA // 2, ALTURA - 19)))

        return surf

    def desenhar_cenario(self, tela: pygame.Surface) -> None:
        """Desenha o fundo 2.5D pre-renderizado da cafeteria."""
        if self.alto_contraste not in self._cache_cenario:
            self._cache_cenario[self.alto_contraste] = self._criar_cenario_cache(
                self.alto_contraste
            )
        tela.blit(self._cache_cenario[self.alto_contraste], (0, 0))

    def desenhar_hud(
        self,
        tela: pygame.Surface,
        fase: GerenciadorFases,
        score: int,
        vidas: int,
        mudo: bool,
        mensagem_barra: str = "",
    ) -> None:
        """Renderiza a barra superior quadrada com fase, meta, pontos e 4 vidas."""
        p = self.paleta
        pygame.draw.rect(tela, p["hud_bg"], (0, 0, LARGURA, HUD_ALTURA))
        pygame.draw.line(
            tela, p["hud_borda"], (0, HUD_ALTURA - 2), (LARGURA, HUD_ALTURA - 2), 3
        )

        cfg = fase.config_atual
        txt_fase = self.f_hud.render(
            f"FASE {cfg['numero']}/{fase.total_fases}  |  {cfg['titulo'].upper()}",
            True,
            p["destaque"],
        )
        tela.blit(txt_fase, (16, 8))

        meta = cfg["meta_clientes"]
        txt_meta = self.f_peq.render(
            f"Clientes atendidos: {fase.clientes_atendidos}/{meta}", True, p["texto_claro"]
        )
        tela.blit(txt_meta, (16, 32))

        # Pontuacao e feedback educativo na barra
        txt_score = self.f_hud.render(f"PONTOS: {score}", True, p["texto_claro"])
        tela.blit(txt_score, (336, 8))
        if mensagem_barra:
            txt_msg = self.f_peq.render(mensagem_barra, True, p["amarelo"])
            tela.blit(txt_msg, (336, 32))
        elif fase.combo_atual >= 2:
            txt_combo = self.f_peq.render(
                f"Sequencia inclusiva x{fase.combo_atual}!", True, p["verde_claro"]
            )
            tela.blit(txt_combo, (336, 32))

        # Vidas (4 coracoes)
        lbl_vidas = self.f_hud.render("VIDAS:", True, p["texto_claro"])
        tela.blit(lbl_vidas, (656, 16))
        for i in range(VIDAS_INICIAIS):
            cor = p["vermelho"] if i < vidas else (82, 70, 64)
            cx = 724 + i * 24
            cy = 26
            pygame.draw.circle(tela, cor, (cx - 4, cy - 2), 5)
            pygame.draw.circle(tela, cor, (cx + 4, cy - 2), 5)
            pygame.draw.polygon(
                tela, cor, [(cx - 9, cy), (cx + 9, cy), (cx, cy + 9)]
            )

        # Botao indicador do Mural (quadrado)
        status_som = "SOM: OFF" if mudo else "SOM: ON"
        badge = pygame.Rect(LARGURA - 188, 11, 172, 32)
        pygame.draw.rect(tela, p["hud_borda"], badge, width=2)
        txt_st = self.f_peq.render(f"{status_som}  |  [TAB] MURAL", True, p["texto_claro"])
        tela.blit(txt_st, txt_st.get_rect(center=badge.center))

    def desenhar_menu(
        self, tela: pygame.Surface, melhor_score: int, libras: BibliotecaLibras
    ) -> None:
        """Desenha o menu inicial quadrado autoral com gestos animados de Libras."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((22, 16, 12, 200))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(112, 58, LARGURA - 224, 520)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 14)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tag = self.f_peq.render("CAFE INCLUSIVO  •  SERIOUS GAME EM LIBRAS", True, p["destaque"])
        titulo = self.f_titulo.render("EXPRESSO LIBRAS", True, cor_t)
        tela.blit(tag, tag.get_rect(center=(LARGURA // 2, 102)))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 144)))

        # Linha editorial divisoria
        pygame.draw.line(
            tela, p["destaque"], (card.left + 80, 178), (card.right - 80, 178), 2
        )

        # Mini vitrine animada de 3 sinais reais no proprio menu
        sinais_destaque = [("oi", "OI"), ("cafe", "CAFE"), ("obrigado", "OBRIGADO")]
        for idx, (sid, rot) in enumerate(sinais_destaque):
            bx = LARGURA // 2 - 190 + idx * 145
            box = pygame.Rect(bx, 194, 100, 104)
            pygame.draw.rect(tela, p["parede"], box)
            pygame.draw.rect(tela, SINAIS_LIBRAS[sid]["cor"], box, 2)
            frame = libras.obter_frame(sid, tamanho=72)
            tela.blit(frame, frame.get_rect(center=(box.centerx, box.top + 42)))
            lbl = self.f_peq.render(rot, True, cor_t)
            tela.blit(lbl, lbl.get_rect(center=(box.centerx, box.bottom - 13)))

        linhas = [
            "Acolha clientes surdos observando gestos reais de Libras no balcao.",
            "Comece com legendas de apoio e evolua ate atender com autonomia!",
        ]
        for idx, linha in enumerate(linhas):
            t = self.f_corpo.render(linha, True, cor_t)
            tela.blit(t, t.get_rect(center=(LARGURA // 2, 326 + idx * 24)))

        if melhor_score > 0:
            rec = self.f_hud.render(
                f"MELHOR PONTUACAO: {melhor_score} PTS", True, p["verde"]
            )
            tela.blit(rec, rec.get_rect(center=(LARGURA // 2, 384)))

        self._desenhar_botao(
            tela,
            "jogar",
            "JOGAR  [ENTER]",
            pygame.Rect(LARGURA // 2 - 165, 412, 330, 50),
            p["verde"],
            (255, 255, 255),
        )
        self._desenhar_botao(
            tela,
            "instrucoes",
            "COMO JOGAR  [I]",
            pygame.Rect(LARGURA // 2 - 165, 474, 330, 44),
            p["azul"],
            (255, 255, 255),
        )
        rodape = self.f_peq.render(
            "[F11] Tela Cheia   |   [C] Alto Contraste   |   [F] Fonte Grande   |   [M] Som   |   [ESC] Sair",
            True,
            cor_t,
        )
        tela.blit(rodape, rodape.get_rect(center=(LARGURA // 2, 548)))

    def desenhar_instrucoes(self, tela: pygame.Surface) -> None:
        """Exibe instrucoes quadradas passo a passo para jogar sem ajuda."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((20, 15, 12, 210))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(88, 48, LARGURA - 176, 540)
        self._desenhar_painel_editorial(tela, card, p["azul"], p["azul"], 12)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tit = self.f_titulo.render("COMO JOGAR", True, p["azul"])
        tela.blit(tit, tit.get_rect(center=(LARGURA // 2, 98)))

        passos = [
            "1. ACOLHA EM LIBRAS: Quando o cliente fizer OI, chegue perto do balcao",
            "   e aperte [E] ou [ESPACO] para responder o cumprimento.",
            "2. LEIA O GESTO: O cliente mostrara o sinal animado em Libras do pedido",
            "   (Cafe, Agua, Bolo, Suco, Conta/Pagar ou Banheiro).",
            "3. PREPARE NA ESTACAO: Mova-se com [WASD] ou [Setas] ([SHIFT] corre)",
            "   e aperte [E] na estacao correspondente ao sinal.",
            "4. ENTREGUE NO BALCAO: Volte ao cliente e aperte [E]. Pegou errado?",
            "   Descarte na Lixeira (DESCARTAR) sem perder pontos!",
            "5. APRENDA NO SEU RITMO: Aperte [TAB] para abrir o Mural de Libras.",
            "   Se a paciencia cair abaixo de 35%, uma pista educativa aparece!",
        ]
        for i, linha in enumerate(passos):
            t = self.f_corpo.render(linha, True, cor_t)
            tela.blit(t, (124, 144 + i * 33))

        self._desenhar_botao(
            tela,
            "voltar_menu",
            "VOLTAR AO MENU  [ENTER / ESC]",
            pygame.Rect(LARGURA // 2 - 195, 502, 390, 48),
            p["destaque"],
            (255, 255, 255),
        )

    def desenhar_briefing(
        self, tela: pygame.Surface, fase: GerenciadorFases, libras: BibliotecaLibras
    ) -> None:
        """Briefing educativo quadrado que ensina os sinais novos da fase antes de jogar."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        cfg = fase.config_atual
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((20, 15, 12, 200))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(88, 52, LARGURA - 176, 534)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 12)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        t1 = self.f_titulo.render(
            f"FASE {cfg['numero']} — {cfg['titulo'].upper()}", True, p["destaque"]
        )
        t2 = self.f_sub.render(
            f"{cfg['subtitulo']}  •  Meta: {cfg['meta_clientes']} clientes", True, cor_t
        )
        tela.blit(t1, t1.get_rect(center=(LARGURA // 2, 102)))
        tela.blit(t2, t2.get_rect(center=(LARGURA // 2, 144)))

        # Quebra limpa da dica educativa
        palavras = cfg["dica_briefing"].split()
        linhas: List[str] = []
        atual = ""
        for pal in palavras:
            teste = f"{atual} {pal}".strip()
            if len(teste) <= 74:
                atual = teste
            else:
                linhas.append(atual)
                atual = pal
        if atual:
            linhas.append(atual)

        for idx, linha in enumerate(linhas):
            t = self.f_corpo.render(linha, True, cor_t)
            tela.blit(t, t.get_rect(center=(LARGURA // 2, 184 + idx * 24)))

        # Vitrine educativa com os sinais novos animados para o jogador memorizar antes
        novos = cfg.get("sinais_novos") or cfg["sinais_permitidos"][:4]
        lbl_sec = (
            "APRENDA OS SINAIS DESTA FASE ANTES DE ABRIR O BALCAO:"
            if cfg.get("sinais_novos")
            else "REVISAO RAPIDA — TODOS OS SINAIS ATIVOS NESTA FASE:"
        )
        t_sec = self.f_hud.render(lbl_sec, True, p["verde"])
        tela.blit(t_sec, t_sec.get_rect(center=(LARGURA // 2, 256)))

        qtd = len(novos)
        larg_box = 186
        esp = 16
        larg_total = qtd * larg_box + (qtd - 1) * esp
        start_x = (LARGURA - larg_total) // 2

        for i, sid in enumerate(novos):
            info = SINAIS_LIBRAS[sid]
            bx = start_x + i * (larg_box + esp)
            box = pygame.Rect(bx, 280, larg_box, 184)
            pygame.draw.rect(tela, p["sombra"], box.move(3, 3))
            pygame.draw.rect(tela, p["parede"], box)
            pygame.draw.rect(tela, info["cor"], (bx, 280, larg_box, 28))
            pygame.draw.rect(tela, info["cor"], box, 2)

            lbl_n = self.f_peq.render(info["nome"], True, (255, 255, 255))
            tela.blit(lbl_n, lbl_n.get_rect(center=(box.centerx, 294)))

            frame = libras.obter_frame(sid, tamanho=96)
            tela.blit(frame, frame.get_rect(center=(box.centerx, 366)))

            dica = self.f_peq.render(info["dica_curta"], True, cor_t)
            tela.blit(dica, dica.get_rect(center=(box.centerx, 444)))

        self._desenhar_botao(
            tela,
            "iniciar_fase",
            "ABRIR O BALCAO  [ENTER / ESPACO]",
            pygame.Rect(LARGURA // 2 - 205, 496, 410, 50),
            p["verde"],
            (255, 255, 255),
        )

    def desenhar_mural(
        self, tela: pygame.Surface, libras: BibliotecaLibras
    ) -> None:
        """Renderiza o Mural quadrado de Libras com os 8 sinais animados em 128px."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((16, 12, 10, 215))
        tela.blit(overlay, (0, 0))

        painel = pygame.Rect(56, 36, LARGURA - 112, ALTURA - 72)
        self._desenhar_painel_editorial(tela, painel, p["destaque"], p["destaque"], 10)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tit = self.f_sub.render(
            "MURAL DE REFERENCIA EM LIBRAS   •   [TAB] ou [ESC] para voltar",
            True,
            p["destaque"],
        )
        tela.blit(tit, tit.get_rect(center=(LARGURA // 2, 72)))

        ordem = ["oi", "cafe", "agua", "bolo", "suco", "pagar", "banheiro", "obrigado"]
        colunas = 4
        larg_card = 208
        alt_card = 210
        inicio_x = 84
        inicio_y = 104
        esp_x = 16
        esp_y = 18

        for idx, sid in enumerate(ordem):
            col = idx % colunas
            lin = idx // colunas
            cx = inicio_x + col * (larg_card + esp_x)
            cy = inicio_y + lin * (alt_card + esp_y)
            box = pygame.Rect(cx, cy, larg_card, alt_card)
            info = SINAIS_LIBRAS[sid]

            pygame.draw.rect(tela, p["sombra"], box.move(3, 3))
            pygame.draw.rect(tela, p["parede"], box)
            topo = pygame.Rect(cx, cy, larg_card, 30)
            pygame.draw.rect(tela, info["cor"], topo)
            pygame.draw.rect(tela, info["cor"], box, width=2)

            lbl_nome = self.f_hud.render(info["nome"], True, (255, 255, 255))
            tela.blit(lbl_nome, lbl_nome.get_rect(center=topo.center))

            frame = libras.obter_frame(sid, tamanho=104)
            tela.blit(frame, frame.get_rect(center=(box.centerx, cy + 96)))

            dica = self.f_peq.render(info["dica_curta"], True, cor_t)
            tela.blit(dica, dica.get_rect(center=(box.centerx, cy + 170)))
            cat = self.f_peq.render(f"[{info['categoria'].upper()}]", True, info["cor"])
            tela.blit(cat, cat.get_rect(center=(box.centerx, cy + 192)))

    def desenhar_pausa(self, tela: pygame.Surface) -> None:
        """Renderiza painel quadrado de pausa com botoes claros."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((16, 12, 10, 190))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(262, 152, LARGURA - 524, 326)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 10)

        tit = self.f_titulo.render("PAUSADO", True, p["destaque"])
        tela.blit(tit, tit.get_rect(center=(LARGURA // 2, 206)))

        self._desenhar_botao(
            tela,
            "continuar",
            "CONTINUAR  [P / ESC]",
            pygame.Rect(LARGURA // 2 - 155, 256, 310, 48),
            p["verde"],
            (255, 255, 255),
        )
        self._desenhar_botao(
            tela,
            "reiniciar_fase",
            "REINICIAR FASE  [R]",
            pygame.Rect(LARGURA // 2 - 155, 318, 310, 48),
            p["azul"],
            (255, 255, 255),
        )
        self._desenhar_botao(
            tela,
            "voltar_menu",
            "MENU PRINCIPAL",
            pygame.Rect(LARGURA // 2 - 155, 380, 310, 48),
            p["vermelho"],
            (255, 255, 255),
        )

    def desenhar_resultado(
        self,
        tela: pygame.Surface,
        tipo: str,
        fase: GerenciadorFases,
        score: int,
    ) -> None:
        """Renderiza relatorio quadrado de aprendizado ao final da fase/jogo."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((18, 14, 10, 210))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(128, 66, LARGURA - 256, 504)
        cor_borda = p["vermelho"] if tipo == "derrota" else p["verde"]
        self._desenhar_painel_editorial(tela, card, cor_borda, cor_borda, 12)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        if tipo == "derrota":
            titulo_str = "TURNO ENCERRADO"
            sub_str = "Sem problemas! Revise o Mural de Libras e tente novamente."
        elif tipo == "vitoria_final":
            titulo_str = "ATENDIMENTO DOMINADO!"
            sub_str = "Voce concluiu todas as 4 fases do Expresso Libras!"
        else:
            titulo_str = f"FASE {fase.numero_fase} CONCLUIDA!"
            sub_str = f"Excelente acolhimento em '{fase.config_atual['titulo']}'!"

        t1 = self.f_titulo.render(titulo_str, True, cor_borda)
        t2 = self.f_corpo.render(sub_str, True, cor_t)
        tela.blit(t1, t1.get_rect(center=(LARGURA // 2, 122)))
        tela.blit(t2, t2.get_rect(center=(LARGURA // 2, 166)))

        autonomia = fase.taxa_autonomia()
        tempo_med = fase.tempo_medio_reacao()
        revisar = fase.sinais_para_revisar()
        revisar_str = ", ".join(revisar) if revisar else "Nenhum — memoria excelente!"

        # Quadro interno de metricas
        box_m = pygame.Rect(card.left + 44, 198, card.width - 88, 206)
        pygame.draw.rect(tela, p["parede"], box_m)
        pygame.draw.rect(tela, p["card_borda"], box_m, 2)

        metricas = [
            f"Pontuacao acumulada: {score} pts   |   Melhor sequencia: x{fase.melhor_combo}",
            f"Clientes atendidos: {fase.clientes_atendidos}/{fase.config_atual['meta_clientes']}",
            f"Autonomia (sem consultar o Mural): {autonomia:.0f}% ({fase.clientes_sem_mural} clientes)",
            f"Tempo medio de reconhecimento: {tempo_med:.1f}s por sinal",
            f"Sinais para revisar: {revisar_str}",
        ]
        for idx, linha in enumerate(metricas):
            txt = self.f_hud.render(linha, True, cor_t)
            tela.blit(txt, txt.get_rect(center=(LARGURA // 2, 226 + idx * 36)))

        if tipo == "vitoria_fase":
            self._desenhar_botao(
                tela,
                "proxima_fase",
                "PROXIMA FASE  [ENTER]",
                pygame.Rect(LARGURA // 2 - 175, 438, 350, 52),
                p["verde"],
                (255, 255, 255),
            )
        elif tipo == "derrota":
            self._desenhar_botao(
                tela,
                "reiniciar_fase",
                "TENTAR NOVAMENTE  [R / ENTER]",
                pygame.Rect(LARGURA // 2 - 185, 438, 370, 52),
                p["destaque"],
                (255, 255, 255),
            )
        else:
            self._desenhar_botao(
                tela,
                "jogar_novamente",
                "JOGAR NOVAMENTE  [ENTER]",
                pygame.Rect(LARGURA // 2 - 185, 438, 370, 52),
                p["verde"],
                (255, 255, 255),
            )

        rod = self.f_peq.render(
            "Pressione [ESC] para voltar ao menu principal", True, cor_t
        )
        tela.blit(rod, rod.get_rect(center=(LARGURA // 2, 522)))
