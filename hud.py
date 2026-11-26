"""Interface grafica 2.5D em Full HD (1920x1080), menus quadrados autorais e HUD.

Implementa identidade visual editorial de cafeteria artesanal brasileira em
alta definicao: paineis quadrados com sombra solida deslocada, moldura dupla,
cenario 2.5D com luz solar obliqua, azulejos, prateleiras, briefing educativo
animado e botao clicavel de alternancia entre Tela Cheia e Modo Janela.
"""

from typing import Dict, List, Tuple

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
    """Gerencia fontes Full HD adaptaveis, cache 2.5D e telas autorais."""

    def __init__(self) -> None:
        """Inicializa fontes Full HD e caches de fundo para as duas paletas."""
        self.alto_contraste = False
        self.fonte_grande = False
        self._cache_cenario: Dict[bool, pygame.Surface] = {}
        self.botoes_clicaveis: Dict[str, pygame.Rect] = {}
        self.mouse_canvas: Tuple[int, int] = (0, 0)
        self._carregar_fontes()

    @property
    def paleta(self) -> dict:
        """Retorna a paleta ativa (padrao artesanal ou alto contraste)."""
        return PALETA_ALTO_CONTRASTE if self.alto_contraste else PALETA_PADRAO

    def definir_mouse_canvas(self, pos: Tuple[int, int]) -> None:
        """Atualiza a posicao do mouse ja convertida para coordenadas 1920x1080."""
        self.mouse_canvas = pos

    def _carregar_fontes(self) -> None:
        """Carrega hierarquia tipografica Full HD ajustada ao modo fonte grande."""
        delta = 6 if self.fonte_grande else 0
        self.f_titulo = pygame.font.SysFont("georgia", 64 + delta, bold=True)
        self.f_sub = pygame.font.SysFont("segoeui", 32 + delta, bold=True)
        self.f_corpo = pygame.font.SysFont("segoeui", 26 + delta)
        self.f_hud = pygame.font.SysFont("segoeui", 24 + delta, bold=True)
        self.f_peq = pygame.font.SysFont("segoeui", 19 + min(4, delta), bold=True)
        self.f_flutuante = pygame.font.SysFont("segoeui", 28 + delta, bold=True)

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
        altura_faixa: int = 16,
    ) -> None:
        """Desenha um painel quadrado autoral com sombra solida e moldura dupla."""
        p = self.paleta
        pygame.draw.rect(tela, p["sombra"], ret.move(12, 12))
        pygame.draw.rect(tela, p["card_bg"], ret)
        if cor_faixa is not None:
            pygame.draw.rect(tela, cor_faixa, (ret.x, ret.y, ret.width, altura_faixa))
        pygame.draw.rect(tela, cor_borda, ret, width=5)
        interna = ret.inflate(-18, -18)
        pygame.draw.rect(tela, p["card_borda"], interna, width=2)

    def _desenhar_botao(
        self,
        tela: pygame.Surface,
        chave: str,
        texto: str,
        ret: pygame.Rect,
        cor_bg: tuple,
        cor_txt: tuple,
        fonte: pygame.font.Font | None = None,
    ) -> None:
        """Desenha um botao quadrado clicavel com sombra solida e efeito hover."""
        hover = ret.collidepoint(self.mouse_canvas)
        desloc = (3, 3) if hover else (6, 6)
        cor_final = tuple(min(255, c + 18) for c in cor_bg) if hover else cor_bg

        pygame.draw.rect(tela, self.paleta["sombra"], ret.move(*desloc))
        ret_draw = ret.move(2, 2) if hover else ret
        pygame.draw.rect(tela, cor_final, ret_draw)
        pygame.draw.rect(tela, self.paleta["card_borda"], ret_draw, width=3)
        brilho = tuple(min(255, c + 30) for c in cor_final)
        pygame.draw.line(
            tela,
            brilho,
            (ret_draw.left + 3, ret_draw.top + 3),
            (ret_draw.right - 4, ret_draw.top + 3),
            3,
        )
        f_usar = fonte or self.f_sub
        lbl = f_usar.render(texto, True, cor_txt)
        max_w = ret_draw.width - 20
        if lbl.get_width() > max_w and max_w > 10:
            escala = max_w / lbl.get_width()
            nova_h = max(1, int(round(lbl.get_height() * escala)))
            lbl = pygame.transform.smoothscale(lbl, (max_w, nova_h))
        tela.blit(lbl, lbl.get_rect(center=ret_draw.center))
        self.botoes_clicaveis[chave] = ret

    def _criar_cenario_cache(self, contraste: bool) -> pygame.Surface:
        """Pre-renderiza o cenario 2.5D da cafeteria em Full HD (1920x1080)."""
        p = PALETA_ALTO_CONTRASTE if contraste else PALETA_PADRAO
        surf = pygame.Surface((LARGURA, ALTURA))
        surf.fill(p["fundo"])

        # 1. Parede superior com padrao de azulejos artesanais
        parede_ret = pygame.Rect(0, HUD_ALTURA, LARGURA, BALCAO_Y - HUD_ALTURA)
        pygame.draw.rect(surf, p["parede"], parede_ret)
        for ay in range(HUD_ALTURA + 38, BALCAO_Y, 38):
            pygame.draw.line(surf, p["parede_azulejo"], (0, ay), (LARGURA, ay), 2)
            desloc = 38 if ((ay // 38) % 2 == 0) else 0
            for ax in range(desloc, LARGURA, 76):
                pygame.draw.line(surf, p["parede_azulejo"], (ax, ay), (ax, ay + 38), 2)
        pygame.draw.rect(surf, p["parede_sombra"], (0, HUD_ALTURA, LARGURA, 22))

        # Quadro-negro central estilo Starbucks (entre os slots 2 e 3, sem sobreposicao)
        quadro = pygame.Rect(810, HUD_ALTURA + 28, 300, 122)
        pygame.draw.rect(surf, p["sombra"], quadro.move(7, 7))
        pygame.draw.rect(surf, (20, 42, 36) if not contraste else (0, 0, 0), quadro)
        pygame.draw.rect(surf, p["dourado"] if not contraste else p["hud_borda"], quadro, 5)
        f_q1 = pygame.font.SysFont("georgia", 24, bold=True)
        f_q2 = pygame.font.SysFont("segoeui", 17, bold=True)
        t_q1 = f_q1.render("EXPRESSO LIBRAS", True, p["dourado"])
        t_q2 = f_q2.render("CAFE INCLUSIVO", True, (244, 242, 236))
        surf.blit(t_q1, t_q1.get_rect(center=(quadro.centerx, quadro.top + 44)))
        surf.blit(t_q2, t_q2.get_rect(center=(quadro.centerx, quadro.top + 84)))

        for jx in (465, 1210):
            janela = pygame.Rect(jx, HUD_ALTURA + 28, 255, 118)
            pygame.draw.rect(surf, p["parede_sombra"], janela.move(6, 6))
            cor_vidro = (30, 44, 66) if contraste else (204, 228, 232)
            pygame.draw.rect(surf, cor_vidro, janela)
            if not contraste:
                pygame.draw.polygon(
                    surf,
                    (234, 248, 248),
                    [
                        (janela.left + 22, janela.top + 6),
                        (janela.left + 84, janela.top + 6),
                        (janela.left + 34, janela.bottom - 6),
                        (janela.left + 8, janela.bottom - 6),
                    ],
                )
            cor_mold = p["hud_borda"] if contraste else p["rodape"]
            pygame.draw.rect(surf, cor_mold, janela, 6)
            pygame.draw.line(
                surf, cor_mold, (janela.centerx, janela.top), (janela.centerx, janela.bottom), 5
            )
            pygame.draw.line(
                surf, cor_mold, (janela.left, janela.centery), (janela.right, janela.centery), 5
            )

        prat = pygame.Rect(1560, HUD_ALTURA + 98, 260, 16)
        pygame.draw.rect(surf, p["sombra"], prat.move(5, 6))
        pygame.draw.rect(surf, p["rodape"] if not contraste else p["hud_borda"], prat)
        for px, cor_pote in (
            (1584, (0, 112, 74)),
            (1646, (30, 57, 50)),
            (1708, (203, 162, 88)),
            (1770, (242, 238, 228)),
        ):
            pygame.draw.rect(surf, cor_pote, (px, HUD_ALTURA + 54, 38, 44))
            pygame.draw.rect(surf, p["sombra"], (px, HUD_ALTURA + 54, 38, 44), 3)
            pygame.draw.rect(surf, (96, 64, 42), (px - 3, HUD_ALTURA + 46, 44, 9))

        porta = pygame.Rect(96, HUD_ALTURA + 22, 166, 200)
        cor_porta = (36, 44, 58) if contraste else (96, 64, 42)
        cor_borda_p = p["hud_borda"] if contraste else p["rodape"]
        pygame.draw.rect(surf, cor_porta, porta)
        pygame.draw.rect(surf, cor_borda_p, porta, 6)
        pygame.draw.rect(
            surf,
            (196, 224, 228) if not contraste else (48, 66, 92),
            (118, HUD_ALTURA + 42, 122, 82),
        )
        placa = pygame.Rect(130, HUD_ALTURA + 70, 98, 30)
        pygame.draw.rect(surf, p["verde"], placa)
        pygame.draw.rect(surf, p["dourado"], placa, 2)
        f_mini = pygame.font.SysFont("segoeui", 17, bold=True)
        txt_ab = f_mini.render("ABERTO", True, (255, 255, 255))
        surf.blit(txt_ab, txt_ab.get_rect(center=placa.center))

        pygame.draw.rect(surf, p["verde"], (104, BALCAO_Y - 58, 150, 42))
        pygame.draw.rect(surf, p["dourado"], (104, BALCAO_Y - 58, 150, 42), 3)

        # 6. Piso de madeira 2.5D com tabuas alternadas
        piso_y = BALCAO_Y + BALCAO_ALTURA - 8
        altura_tabua = 46
        for idx, y in enumerate(range(piso_y, ALTURA, altura_tabua)):
            cor = p["piso_claro"] if idx % 2 == 0 else p["piso_escuro"]
            pygame.draw.rect(surf, cor, (0, y, LARGURA, altura_tabua))
            pygame.draw.line(surf, p["piso_linha"], (0, y), (LARGURA, y), 2)
            desloc = (idx % 3) * 150
            for x in range(desloc, LARGURA, 340):
                pygame.draw.line(surf, p["piso_linha"], (x, y), (x, y + altura_tabua), 2)

        # Feixes de luz solar obliquos (modo padrao)
        if not contraste:
            luz = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            for jx in (465, 1210):
                feixe = [
                    (jx, BALCAO_Y + BALCAO_ALTURA),
                    (jx + 255, BALCAO_Y + BALCAO_ALTURA),
                    (jx + 110, ALTURA - 58),
                    (jx - 145, ALTURA - 58),
                ]
                pygame.draw.polygon(luz, (255, 244, 204, 34), feixe)
            surf.blit(luz, (0, 0))

        # 7. Laterais arquitetonicas e barra de rodape
        cor_borda_salao = (12, 12, 16) if contraste else p["rodape"]
        pygame.draw.rect(surf, cor_borda_salao, (0, piso_y, 96, ALTURA - piso_y))
        pygame.draw.rect(surf, cor_borda_salao, (LARGURA - 96, piso_y, 96, ALTURA - piso_y))
        pygame.draw.rect(surf, cor_borda_salao, (0, ALTURA - 58, LARGURA, 58))
        pygame.draw.line(surf, p["hud_borda"], (0, ALTURA - 58), (LARGURA, ALTURA - 58), 3)

        # Plantas 2.5D nos cantos do salao
        for px, py in ((48, 520), (48, 945), (LARGURA - 48, 520)):
            pygame.draw.rect(surf, (152, 82, 50), (px - 20, py + 4, 40, 30))
            pygame.draw.rect(surf, (116, 60, 36), (px - 24, py, 48, 10))
            pygame.draw.circle(surf, (44, 124, 68), (px - 10, py - 8), 18)
            pygame.draw.circle(surf, (66, 164, 92), (px + 10, py - 12), 17)
            pygame.draw.circle(surf, (88, 186, 110), (px, py - 22), 15)

        # 8. Balcao 2.5D com sombra projetada no piso, frente ripada e tampo de marmore
        sombra_balcao = pygame.Surface((LARGURA - 192, 26), pygame.SRCALPHA)
        sombra_balcao.fill((18, 12, 8, 95))
        surf.blit(sombra_balcao, (96, BALCAO_Y + BALCAO_ALTURA + 10))

        pygame.draw.rect(
            surf, p["balcao_frente"], (96, BALCAO_Y + 24, LARGURA - 192, BALCAO_ALTURA - 8)
        )
        pygame.draw.rect(
            surf, p["balcao_detalhe"], (96, BALCAO_Y + 24, LARGURA - 192, 12)
        )
        for rx in range(124, LARGURA - 116, 38):
            pygame.draw.line(
                surf,
                p["balcao_detalhe"],
                (rx, BALCAO_Y + 36),
                (rx, BALCAO_Y + BALCAO_ALTURA + 14),
                3,
            )
        pygame.draw.rect(
            surf, p["balcao_detalhe"], (96, BALCAO_Y + 24, LARGURA - 192, BALCAO_ALTURA - 8), 3
        )
        # Tampo de marmore claro
        pygame.draw.rect(surf, p["balcao_topo"], (86, BALCAO_Y, LARGURA - 172, 26))
        pygame.draw.rect(surf, p["balcao_detalhe"], (86, BALCAO_Y, LARGURA - 172, 26), 3)

        # Rodape de controles rapidos
        f_bar = pygame.font.SysFont("segoeui", 19, bold=True)
        dica = (
            "[WASD/Setas] Mover   [SHIFT] Correr   [E/ESPACO] Interagir   "
            "[TAB] Mural   [F11] Tela Cheia / Janela   [C] Contraste   [F] Fonte   [M] Som   [P] Pausa"
        )
        txt = f_bar.render(dica, True, p["texto_claro"])
        surf.blit(txt, txt.get_rect(center=(LARGURA // 2, ALTURA - 29)))

        return surf

    def desenhar_cenario(self, tela: pygame.Surface) -> None:
        """Desenha o fundo 2.5D pre-renderizado da cafeteria em Full HD."""
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
        tela_cheia: bool,
        mensagem_barra: str = "",
        limpar_botoes: bool = True,
    ) -> None:
        """Renderiza a barra superior com fase, pontos, 4 vidas e botoes clicaveis."""
        if limpar_botoes:
            self.botoes_clicaveis.clear()

        p = self.paleta
        pygame.draw.rect(tela, p["hud_bg"], (0, 0, LARGURA, HUD_ALTURA))
        pygame.draw.line(
            tela, p["hud_borda"], (0, HUD_ALTURA - 3), (LARGURA, HUD_ALTURA - 3), 4
        )

        cfg = fase.config_atual
        txt_fase = self.f_hud.render(
            f"FASE {cfg['numero']}/{fase.total_fases}  |  {cfg['titulo'].upper()}",
            True,
            p["destaque"],
        )
        tela.blit(txt_fase, (26, 12))

        meta = cfg["meta_clientes"]
        txt_meta = self.f_peq.render(
            f"Clientes atendidos: {fase.clientes_atendidos}/{meta}", True, p["texto_claro"]
        )
        tela.blit(txt_meta, (26, 48))

        # Pontuacao e feedback educativo na barra
        txt_score = self.f_hud.render(f"PONTOS: {score}", True, p["texto_claro"])
        tela.blit(txt_score, (540, 12))
        if mensagem_barra:
            txt_msg = self.f_peq.render(mensagem_barra, True, p["amarelo"])
            tela.blit(txt_msg, (540, 48))
        elif fase.combo_atual >= 2:
            txt_combo = self.f_peq.render(
                f"Sequencia inclusiva x{fase.combo_atual}!", True, p["verde_claro"]
            )
            tela.blit(txt_combo, (540, 48))

        # Vidas (4 coracoes)
        lbl_vidas = self.f_hud.render("VIDAS:", True, p["texto_claro"])
        tela.blit(lbl_vidas, (960, 26))
        for i in range(VIDAS_INICIAIS):
            cor = p["vermelho"] if i < vidas else (70, 86, 80)
            cx = 1072 + i * 36
            cy = 40
            pygame.draw.circle(tela, cor, (cx - 6, cy - 3), 8)
            pygame.draw.circle(tela, cor, (cx + 6, cy - 3), 8)
            pygame.draw.polygon(
                tela, cor, [(cx - 14, cy), (cx + 14, cy), (cx, cy + 14)]
            )

        if limpar_botoes:
            lbl_som = "SOM: OFF [M]" if mudo else "SOM: ON [M]"
            self._desenhar_botao(
                tela,
                "alternar_som",
                lbl_som,
                pygame.Rect(LARGURA - 684, 17, 184, 48),
                p["rodape"],
                p["texto_claro"],
                fonte=self.f_peq,
            )
            self._desenhar_botao(
                tela,
                "abrir_mural",
                "MURAL [TAB]",
                pygame.Rect(LARGURA - 486, 17, 200, 48),
                p["verde"],
                (255, 255, 255),
                fonte=self.f_peq,
            )
            lbl_tela = "JANELA [F11]" if tela_cheia else "TELA CHEIA [F11]"
            self._desenhar_botao(
                tela,
                "alternar_tela",
                lbl_tela,
                pygame.Rect(LARGURA - 272, 17, 248, 48),
                p["dourado"],
                p["texto_escuro"],
                fonte=self.f_peq,
            )

    def desenhar_menu(
        self,
        tela: pygame.Surface,
        melhor_score: int,
        libras: BibliotecaLibras,
        tela_cheia: bool,
    ) -> None:
        """Desenha o menu inicial quadrado autoral em Full HD com botao Tela Cheia."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((22, 16, 12, 200))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(240, 86, LARGURA - 480, 900)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 20)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tag = self.f_peq.render(
            "CAFE INCLUSIVO  •  SERIOUS GAME EM LIBRAS", True, p["destaque"]
        )
        titulo = self.f_titulo.render("EXPRESSO LIBRAS", True, cor_t)
        tela.blit(tag, tag.get_rect(center=(LARGURA // 2, 152)))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 218)))

        pygame.draw.line(
            tela, p["destaque"], (card.left + 120, 272), (card.right - 120, 272), 3
        )

        # Vitrine animada de 3 sinais reais em alta definicao
        sinais_destaque = [("oi", "OI / OLA"), ("cafe", "CAFE"), ("obrigado", "OBRIGADO")]
        for idx, (sid, rot) in enumerate(sinais_destaque):
            bx = LARGURA // 2 - 320 + idx * 230
            box = pygame.Rect(bx, 300, 180, 192)
            pygame.draw.rect(tela, p["sombra"], box.move(4, 4))
            pygame.draw.rect(tela, p["parede"], box)
            pygame.draw.rect(tela, SINAIS_LIBRAS[sid]["cor"], box, 3)
            frame = libras.obter_frame(sid, tamanho=136)
            tela.blit(frame, frame.get_rect(center=(box.centerx, box.top + 78)))
            lbl = self.f_peq.render(rot, True, cor_t)
            tela.blit(lbl, lbl.get_rect(center=(box.centerx, box.bottom - 20)))

        linhas = [
            "Acolha clientes surdos observando gestos reais de Libras no balcao.",
            "Comece com legendas de apoio e evolua ate atender com autonomia!",
        ]
        for idx, linha in enumerate(linhas):
            t = self.f_corpo.render(linha, True, cor_t)
            tela.blit(t, t.get_rect(center=(LARGURA // 2, 534 + idx * 38)))

        if melhor_score > 0:
            rec = self.f_hud.render(
                f"MELHOR PONTUACAO: {melhor_score} PTS", True, p["verde"]
            )
            tela.blit(rec, rec.get_rect(center=(LARGURA // 2, 622)))

        self._desenhar_botao(
            tela,
            "jogar",
            "JOGAR  [ENTER]",
            pygame.Rect(LARGURA // 2 - 310, 666, 620, 74),
            p["verde"],
            (255, 255, 255),
        )
        self._desenhar_botao(
            tela,
            "instrucoes",
            "COMO JOGAR  [I]",
            pygame.Rect(LARGURA // 2 - 310, 756, 300, 66),
            p["azul"],
            (255, 255, 255),
            fonte=self.f_hud,
        )
        lbl_tela = "MODO JANELA [F11]" if tela_cheia else "TELA CHEIA [F11]"
        self._desenhar_botao(
            tela,
            "alternar_tela",
            lbl_tela,
            pygame.Rect(LARGURA // 2 + 10, 756, 300, 66),
            p["dourado"],
            p["texto_escuro"],
            fonte=self.f_hud,
        )

        rodape = self.f_peq.render(
            "[F11] Tela Cheia / Janela   |   [C] Alto Contraste   |   [F] Fonte Grande   |   [M] Som   |   [ESC] Sair",
            True,
            cor_t,
        )
        tela.blit(rodape, rodape.get_rect(center=(LARGURA // 2, 916)))

    def desenhar_instrucoes(self, tela: pygame.Surface) -> None:
        """Exibe instrucoes quadradas passo a passo em Full HD."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((20, 15, 12, 210))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(180, 76, LARGURA - 360, 920)
        self._desenhar_painel_editorial(tela, card, p["azul"], p["azul"], 18)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tit = self.f_titulo.render("COMO JOGAR", True, p["azul"])
        tela.blit(tit, tit.get_rect(center=(LARGURA // 2, 158)))

        passos = [
            "1. ACOLHA EM LIBRAS: Quando o cliente fizer OI, chegue perto do balcao",
            "   e aperte [E] ou [ESPACO] para responder o cumprimento.",
            "2. LEIA O GESTO: O cliente mostrara o sinal ilustrado em Libras do pedido",
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
            tela.blit(t, (248, 240 + i * 56))

        self._desenhar_botao(
            tela,
            "voltar_menu",
            "VOLTAR AO MENU  [ENTER / ESC]",
            pygame.Rect(LARGURA // 2 - 300, 860, 600, 74),
            p["destaque"],
            (255, 255, 255),
        )

    def desenhar_briefing(
        self, tela: pygame.Surface, fase: GerenciadorFases, libras: BibliotecaLibras
    ) -> None:
        """Briefing educativo em Full HD mostrando os sinais novos em alta definicao."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        cfg = fase.config_atual
        self.desenhar_cenario(tela)

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((20, 15, 12, 200))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(150, 76, LARGURA - 300, 920)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 18)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        t1 = self.f_titulo.render(
            f"FASE {cfg['numero']} — {cfg['titulo'].upper()}", True, p["destaque"]
        )
        t2 = self.f_sub.render(
            f"{cfg['subtitulo']}  •  Meta: {cfg['meta_clientes']} clientes", True, cor_t
        )
        tela.blit(t1, t1.get_rect(center=(LARGURA // 2, 160)))
        tela.blit(t2, t2.get_rect(center=(LARGURA // 2, 224)))

        palavras = cfg["dica_briefing"].split()
        linhas: List[str] = []
        atual = ""
        for pal in palavras:
            teste = f"{atual} {pal}".strip()
            if len(teste) <= 80:
                atual = teste
            else:
                linhas.append(atual)
                atual = pal
        if atual:
            linhas.append(atual)

        for idx, linha in enumerate(linhas):
            t = self.f_corpo.render(linha, True, cor_t)
            tela.blit(t, t.get_rect(center=(LARGURA // 2, 286 + idx * 38)))

        novos = cfg.get("sinais_novos") or cfg["sinais_permitidos"][:4]
        lbl_sec = (
            "APRENDA OS SINAIS DESTA FASE ANTES DE ABRIR O BALCAO:"
            if cfg.get("sinais_novos")
            else "REVISAO RAPIDA — TODOS OS SINAIS ATIVOS NESTA FASE:"
        )
        t_sec = self.f_hud.render(lbl_sec, True, p["verde"])
        tela.blit(t_sec, t_sec.get_rect(center=(LARGURA // 2, 412)))

        qtd = len(novos)
        larg_box = 340
        esp = 28
        larg_total = qtd * larg_box + (qtd - 1) * esp
        start_x = (LARGURA - larg_total) // 2

        for i, sid in enumerate(novos):
            info = SINAIS_LIBRAS[sid]
            bx = start_x + i * (larg_box + esp)
            box = pygame.Rect(bx, 452, larg_box, 330)
            pygame.draw.rect(tela, p["sombra"], box.move(5, 5))
            pygame.draw.rect(tela, p["parede"], box)
            pygame.draw.rect(tela, info["cor"], (bx, 452, larg_box, 48))
            pygame.draw.rect(tela, info["cor"], box, 3)

            lbl_n = self.f_hud.render(info["nome"], True, (255, 255, 255))
            tela.blit(lbl_n, lbl_n.get_rect(center=(box.centerx, 476)))

            frame = libras.obter_frame(sid, tamanho=188)
            tela.blit(frame, frame.get_rect(center=(box.centerx, 608)))

            dica = self.f_peq.render(info["dica_curta"], True, cor_t)
            tela.blit(dica, dica.get_rect(center=(box.centerx, 748)))

        self._desenhar_botao(
            tela,
            "iniciar_fase",
            "ABRIR O BALCAO  [ENTER / ESPACO]",
            pygame.Rect(LARGURA // 2 - 330, 846, 660, 80),
            p["verde"],
            (255, 255, 255),
        )

    def desenhar_mural(
        self, tela: pygame.Surface, libras: BibliotecaLibras
    ) -> None:
        """Renderiza o Mural de Libras em Full HD com ilustracoes 256->196px."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((16, 12, 10, 215))
        tela.blit(overlay, (0, 0))

        painel = pygame.Rect(92, 54, LARGURA - 184, ALTURA - 108)
        self._desenhar_painel_editorial(tela, painel, p["destaque"], p["destaque"], 16)

        cor_t = p["texto_claro"] if p["card_bg"][0] < 40 else p["texto_escuro"]
        tit = self.f_sub.render(
            "MURAL DE REFERENCIA EM LIBRAS", True, p["destaque"]
        )
        tela.blit(tit, (140, 96))
        self._desenhar_botao(
            tela,
            "fechar_mural",
            "FECHAR [TAB / ESC]",
            pygame.Rect(LARGURA - 410, 86, 268, 52),
            p["dourado"],
            p["texto_escuro"],
            fonte=self.f_peq,
        )

        ordem = ["oi", "cafe", "agua", "bolo", "suco", "pagar", "banheiro", "obrigado"]
        colunas = 4
        larg_card = 392
        alt_card = 382
        inicio_x = 138
        inicio_y = 162
        esp_x = 26
        esp_y = 28

        for idx, sid in enumerate(ordem):
            col = idx % colunas
            lin = idx // colunas
            cx = inicio_x + col * (larg_card + esp_x)
            cy = inicio_y + lin * (alt_card + esp_y)
            box = pygame.Rect(cx, cy, larg_card, alt_card)
            info = SINAIS_LIBRAS[sid]

            pygame.draw.rect(tela, p["sombra"], box.move(5, 5))
            pygame.draw.rect(tela, p["parede"], box)
            topo = pygame.Rect(cx, cy, larg_card, 50)
            pygame.draw.rect(tela, info["cor"], topo)
            pygame.draw.rect(tela, info["cor"], box, width=3)

            lbl_nome = self.f_hud.render(info["nome"], True, (255, 255, 255))
            tela.blit(lbl_nome, lbl_nome.get_rect(center=topo.center))

            frame = libras.obter_frame(sid, tamanho=210)
            tela.blit(frame, frame.get_rect(center=(box.centerx, cy + 174)))

            dica = self.f_peq.render(info["dica_curta"], True, cor_t)
            tela.blit(dica, dica.get_rect(center=(box.centerx, cy + 314)))
            cat = self.f_peq.render(f"[{info['categoria'].upper()}]", True, info["cor"])
            tela.blit(cat, cat.get_rect(center=(box.centerx, cy + 350)))

    def desenhar_pausa(self, tela: pygame.Surface, tela_cheia: bool) -> None:
        """Renderiza painel quadrado de pausa com botao de Tela Cheia / Janela."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((16, 12, 10, 190))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(520, 210, LARGURA - 1040, 640)
        self._desenhar_painel_editorial(tela, card, p["destaque"], p["destaque"], 16)

        tit = self.f_titulo.render("PAUSADO", True, p["destaque"])
        tela.blit(tit, tit.get_rect(center=(LARGURA // 2, 298)))

        self._desenhar_botao(
            tela,
            "continuar",
            "CONTINUAR  [P / ESC]",
            pygame.Rect(LARGURA // 2 - 260, 380, 520, 74),
            p["verde"],
            (255, 255, 255),
        )
        lbl_tela = "MODO JANELA  [F11]" if tela_cheia else "TELA CHEIA  [F11]"
        self._desenhar_botao(
            tela,
            "alternar_tela",
            lbl_tela,
            pygame.Rect(LARGURA // 2 - 260, 474, 520, 74),
            p["dourado"],
            p["texto_escuro"],
        )
        self._desenhar_botao(
            tela,
            "reiniciar_fase",
            "REINICIAR FASE  [R]",
            pygame.Rect(LARGURA // 2 - 260, 568, 520, 74),
            p["azul"],
            (255, 255, 255),
        )
        self._desenhar_botao(
            tela,
            "voltar_menu",
            "MENU PRINCIPAL",
            pygame.Rect(LARGURA // 2 - 260, 662, 520, 74),
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
        """Renderiza relatorio quadrado de aprendizado em Full HD."""
        self.botoes_clicaveis.clear()
        p = self.paleta
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((18, 14, 10, 210))
        tela.blit(overlay, (0, 0))

        card = pygame.Rect(220, 100, LARGURA - 440, 860)
        cor_borda = p["vermelho"] if tipo == "derrota" else p["verde"]
        self._desenhar_painel_editorial(tela, card, cor_borda, cor_borda, 18)

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
        tela.blit(t1, t1.get_rect(center=(LARGURA // 2, 192)))
        tela.blit(t2, t2.get_rect(center=(LARGURA // 2, 260)))

        autonomia = fase.taxa_autonomia()
        tempo_med = fase.tempo_medio_reacao()
        revisar = fase.sinais_para_revisar()
        revisar_str = ", ".join(revisar) if revisar else "Nenhum — memoria excelente!"

        box_m = pygame.Rect(card.left + 72, 316, card.width - 144, 344)
        pygame.draw.rect(tela, p["parede"], box_m)
        pygame.draw.rect(tela, p["card_borda"], box_m, 3)

        metricas = [
            f"Pontuacao acumulada: {score} pts   |   Melhor sequencia: x{fase.melhor_combo}",
            f"Clientes atendidos: {fase.clientes_atendidos}/{fase.config_atual['meta_clientes']}",
            f"Autonomia (sem consultar o Mural): {autonomia:.0f}% ({fase.clientes_sem_mural} clientes)",
            f"Tempo medio de reconhecimento: {tempo_med:.1f}s por sinal",
            f"Sinais para revisar: {revisar_str}",
        ]
        for idx, linha in enumerate(metricas):
            txt = self.f_hud.render(linha, True, cor_t)
            tela.blit(txt, txt.get_rect(center=(LARGURA // 2, 368 + idx * 60)))

        if tipo == "vitoria_fase":
            self._desenhar_botao(
                tela,
                "proxima_fase",
                "PROXIMA FASE  [ENTER]",
                pygame.Rect(LARGURA // 2 - 280, 720, 560, 82),
                p["verde"],
                (255, 255, 255),
            )
        elif tipo == "derrota":
            self._desenhar_botao(
                tela,
                "reiniciar_fase",
                "TENTAR NOVAMENTE  [R / ENTER]",
                pygame.Rect(LARGURA // 2 - 300, 720, 600, 82),
                p["destaque"],
                (255, 255, 255),
            )
        else:
            self._desenhar_botao(
                tela,
                "jogar_novamente",
                "JOGAR NOVAMENTE  [ENTER]",
                pygame.Rect(LARGURA // 2 - 300, 720, 600, 82),
                p["verde"],
                (255, 255, 255),
            )

        rod = self.f_peq.render(
            "Pressione [ESC] para voltar ao menu principal", True, cor_t
        )
        tela.blit(rod, rod.get_rect(center=(LARGURA // 2, 876)))
