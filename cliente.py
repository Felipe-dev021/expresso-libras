"""Classe Cliente que representa pessoas surdas atendidas no balcao.

Cada cliente chega caminhando ao seu lugar, apresenta sinais animados em Libras
(cumprimento inicial + 1 ou 2 pedidos), controla sua barra de paciencia e
fornece feedback visual claro ao ser atendido corretamente ou com erro.
"""

import random
from typing import List, Optional, Tuple

import pygame

from config import (
    HUD_ALTURA,
    LIMIAR_DICA_AUTOMATICA,
    PENALIDADE_ERRO_PACIENCIA,
    SINAIS_LIBRAS,
    caminho_arquivo,
)
from libras import BibliotecaLibras


class Cliente(pygame.sprite.Sprite):
    """Cliente surdo que interage com o atendente por meio de sinais em Libras."""

    def __init__(
        self,
        slot_index: int,
        destino_balcao: Tuple[int, int],
        pedidos: List[str],
        paciencia_max: float,
        mostrar_legenda: bool = False,
        exige_cumprimento: bool = True,
    ) -> None:
        """Cria um cliente com aparencia variada, lista de pedidos e paciencia."""
        super().__init__()
        perfil = random.randint(0, 3)
        self.image = pygame.image.load(
            caminho_arquivo(f"cliente_{perfil}.png")
        ).convert_alpha()

        self.slot_index = slot_index
        self.destino_x, self.destino_y = destino_balcao
        self.pos_x = 176.0
        self.pos_y = float(destino_balcao[1] - 58)
        self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))

        self.pedidos = list(pedidos)
        self.indice_pedido = 0
        self.precisa_oi = exige_cumprimento
        self.mostrar_legenda = mostrar_legenda

        self.paciencia_max = paciencia_max
        self.paciencia = paciencia_max
        self.tempo_espera_sinal = 0.0
        self.consultou_mural_neste = False

        self.estado = "entrando"
        self.tempo_saida = 0.0
        self.tempo_erro_visual = 0.0
        self.destacado = False

    @property
    def sinal_atual(self) -> Optional[str]:
        """Retorna o ID do sinal em Libras que o cliente esta fazendo agora."""
        if self.estado == "feliz":
            return "obrigado"
        if self.estado != "esperando":
            return None
        if self.precisa_oi:
            return "oi"
        if self.indice_pedido < len(self.pedidos):
            return self.pedidos[self.indice_pedido]
        return None

    @property
    def percentual_paciencia(self) -> float:
        """Retorna proporcao [0.0, 1.0] da paciencia restante."""
        return max(0.0, min(1.0, self.paciencia / self.paciencia_max))

    def cumprimentar(self) -> Tuple[bool, float]:
        """Responde ao sinal de OI do cliente; retorna (acertou, tempo_reacao)."""
        if self.estado != "esperando" or not self.precisa_oi:
            return False, 0.0
        tempo = self.tempo_espera_sinal
        self.precisa_oi = False
        self.tempo_espera_sinal = 0.0
        # Pequeno ganho de paciencia pelo acolhimento
        self.paciencia = min(self.paciencia_max, self.paciencia + 2.0)
        return True, tempo

    def entregar_item(self, item_id: str) -> Tuple[str, float, str]:
        """Valida se o item entregue corresponde ao sinal atual em Libras.

        Retorna tupla (resultado, tempo_reacao, sinal_esperado), onde resultado
        pode ser 'precisa_oi', 'etapa_ok', 'concluido' ou 'errado'.
        """
        if self.estado != "esperando":
            return "inativo", 0.0, ""
        if self.precisa_oi:
            self.tempo_erro_visual = 0.45
            return "precisa_oi", 0.0, "oi"

        esperado = self.pedidos[self.indice_pedido]
        if item_id == esperado:
            tempo = self.tempo_espera_sinal
            self.tempo_espera_sinal = 0.0
            self.indice_pedido += 1
            if self.indice_pedido >= len(self.pedidos):
                self.estado = "feliz"
                self.tempo_saida = 1.25
                return "concluido", tempo, esperado
            # Ainda ha um segundo pedido: renova parte da paciencia
            self.paciencia = min(self.paciencia_max, self.paciencia + 5.0)
            return "etapa_ok", tempo, esperado

        # Erro de interpretacao do sinal
        self.paciencia = max(
            1.5, self.paciencia - self.paciencia_max * PENALIDADE_ERRO_PACIENCIA
        )
        self.tempo_erro_visual = 0.55
        return "errado", 0.0, esperado

    def update(self, dt: float) -> Optional[str]:
        """Atualiza animacao de entrada, paciencia e saida do cliente.

        Retorna 'desistiu' se a paciencia zerou, ou 'saiu' quando concluiu a saida.
        """
        if self.tempo_erro_visual > 0:
            self.tempo_erro_visual = max(0.0, self.tempo_erro_visual - dt)

        if self.estado == "entrando":
            vel = 390.0
            dx = self.destino_x - self.pos_x
            dy = self.destino_y - self.pos_y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= vel * dt + 2.0:
                self.pos_x = float(self.destino_x)
                self.pos_y = float(self.destino_y)
                self.estado = "esperando"
            else:
                self.pos_x += (dx / dist) * vel * dt
                self.pos_y += (dy / dist) * vel * dt
            self.rect.center = (round(self.pos_x), round(self.pos_y))
            return None

        if self.estado == "esperando":
            self.paciencia -= dt
            self.tempo_espera_sinal += dt
            if self.paciencia <= 0:
                self.paciencia = 0.0
                self.estado = "triste"
                self.tempo_saida = 0.9
                return "desistiu"
            return None

        if self.estado in ("feliz", "triste"):
            self.tempo_saida -= dt
            if self.tempo_saida <= 0:
                self.kill()
                return "saiu"
        return None

    def desenhar_balao(
        self,
        tela: pygame.Surface,
        libras: BibliotecaLibras,
        fonte_peq: pygame.font.Font,
        paleta: dict,
    ) -> None:
        """Desenha o balao de Libras acima do cliente e sua barra de paciencia."""
        if self.estado == "entrando":
            return

        # Halo quadrado de destaque quando o jogador esta em frente ao cliente
        if self.destacado and self.estado == "esperando":
            base = pygame.Rect(self.rect.centerx - 46, self.rect.bottom - 22, 92, 28)
            pygame.draw.rect(tela, paleta["destaque"], base, width=4)

        sinal_id = self.sinal_atual
        if not sinal_id:
            return

        tremor = 6 if (self.tempo_erro_visual > 0 and int(self.tempo_erro_visual * 30) % 2 == 0) else 0
        dica_urgente = (
            self.estado == "esperando"
            and self.percentual_paciencia <= LIMIAR_DICA_AUTOMATICA
        )
        tem_legenda = (
            self.mostrar_legenda
            or dica_urgente
            or self.estado == "feliz"
            or sinal_id == "oi"
        )
        largura_balao = 176
        altura_balao = 148 if tem_legenda else 124
        bx = self.rect.centerx - largura_balao // 2 + tremor
        by = max(HUD_ALTURA + 10, self.rect.top - altura_balao - 12)

        ret = pygame.Rect(bx, by, largura_balao, altura_balao)
        cor_borda = paleta["vermelho"] if self.tempo_erro_visual > 0 else (
            paleta["verde"] if self.estado == "feliz" else paleta["card_borda"]
        )
        if self.destacado and self.estado == "esperando":
            cor_borda = paleta["destaque"]

        # Balao quadrado autoral com sombra projetada solida
        pygame.draw.rect(tela, paleta["sombra"], ret.move(6, 6))
        pygame.draw.rect(tela, paleta["card_bg"], ret)
        pygame.draw.rect(tela, cor_borda, ret, width=4)
        ponta = [
            (self.rect.centerx - 12, ret.bottom - 1),
            (self.rect.centerx + 12, ret.bottom - 1),
            (self.rect.centerx, ret.bottom + 14),
        ]
        pygame.draw.polygon(tela, paleta["card_bg"], ponta)
        pygame.draw.lines(tela, cor_borda, False, [ponta[0], ponta[2], ponta[1]], 3)

        # Ilustracao desenhada em alta nitidez (102x102)
        frame = libras.obter_frame(sinal_id, tamanho=102)
        tela.blit(frame, frame.get_rect(center=(ret.centerx, ret.top + 58)))

        # Indicador de pedido duplo (quadradinhos no topo direito)
        if self.estado == "esperando" and len(self.pedidos) > 1:
            for i in range(len(self.pedidos)):
                cor_q = (
                    paleta["verde"]
                    if i < self.indice_pedido
                    else (
                        paleta["destaque"]
                        if i == self.indice_pedido and not self.precisa_oi
                        else paleta["card_borda"]
                    )
                )
                pygame.draw.rect(
                    tela, cor_q, (ret.right - 24 - i * 18, ret.top + 10, 12, 12)
                )

        # Legenda educativa (clientes iniciais, pista de baixa paciencia ou agradecimento)
        if tem_legenda:
            nome = SINAIS_LIBRAS[sinal_id]["nome"].split("/")[0].strip()
            if sinal_id == "oi" and self.estado == "esperando":
                nome = "OI [E]"
            elif dica_urgente and not self.mostrar_legenda and sinal_id != "oi":
                nome = f"DICA: {nome}"
            cor_txt = paleta["verde"] if self.estado == "feliz" else (
                paleta["vermelho"]
                if dica_urgente and not self.mostrar_legenda and sinal_id != "oi"
                else (
                    paleta["texto_claro"]
                    if paleta["card_bg"][0] < 40
                    else paleta["texto_escuro"]
                )
            )
            txt = fonte_peq.render(nome, True, cor_txt)
            tela.blit(txt, txt.get_rect(center=(ret.centerx, ret.bottom - 18)))

        # Barra de paciencia quadrada logo abaixo do cliente
        if self.estado == "esperando":
            pct = self.percentual_paciencia
            cor_barra = (
                paleta["verde"]
                if pct > 0.5
                else (paleta["amarelo"] if pct > 0.25 else paleta["vermelho"])
            )
            barra_bg = pygame.Rect(self.rect.centerx - 52, self.rect.bottom + 4, 104, 13)
            barra_fg = pygame.Rect(barra_bg.x + 2, barra_bg.y + 2, int(100 * pct), 9)
            pygame.draw.rect(tela, (28, 20, 16), barra_bg)
            if barra_fg.width > 0:
                pygame.draw.rect(tela, cor_barra, barra_fg)
