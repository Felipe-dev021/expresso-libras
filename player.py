"""Classe do personagem jogavel (Atendente) em Sinal Aberto.

Controla movimentacao normalizada em 8 direcoes com delta time,
corrida opcional com SHIFT, colisao suave com obstaculos e
carregamento do item preparado na bandeja.
"""

import math
from typing import Dict, Iterable, Optional

import pygame

from config import (
    AREA_ATENDENTE,
    SINAIS_ESTACAO,
    VELOCIDADE_CORRIDA,
    VELOCIDADE_JOGADOR,
    caminho_arquivo,
)


class Atendente(pygame.sprite.Sprite):
    """Atendente da cafeteria que se movimenta, prepara itens e sinaliza em Libras."""

    def __init__(self, x: int, y: int) -> None:
        """Carrega sprites de caminhada e icones de itens carregaveis."""
        super().__init__()
        self.frames = [
            pygame.image.load(caminho_arquivo("atendente_0.png")).convert_alpha(),
            pygame.image.load(caminho_arquivo("atendente_1.png")).convert_alpha(),
        ]
        self.icones_item: Dict[str, pygame.Surface] = {}
        for item_id in SINAIS_ESTACAO:
            self.icones_item[item_id] = pygame.image.load(
                caminho_arquivo(f"item_{item_id}.png")
            ).convert_alpha()

        self.frame_atual = 0
        self.tempo_passo = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

        self.item_na_mao: Optional[str] = None
        self.tempo_sinal_oi = 0.0
        self.limites = pygame.Rect(*AREA_ATENDENTE)

    @property
    def hitbox_pes(self) -> pygame.Rect:
        """Retorna caixa de colisao reduzida nos pes para movimento 2.5D confortavel."""
        return pygame.Rect(
            int(self.pos_x) - 28,
            int(self.pos_y) + 22,
            56,
            34,
        )

    def resetar(self, x: int, y: int) -> None:
        """Reposiciona o atendente no inicio de cada fase e limpa a mao."""
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect.center = (x, y)
        self.item_na_mao = None
        self.tempo_sinal_oi = 0.0

    def acionar_cumprimento(self) -> None:
        """Ativa um breve destaque visual de saudacao em Libras."""
        self.tempo_sinal_oi = 0.65

    def pegar_item(self, item_id: str) -> None:
        """Coloca o item ou cartao de servico na mao do atendente."""
        self.item_na_mao = item_id

    def limpar_mao(self) -> None:
        """Remove o item atualmente carregado."""
        self.item_na_mao = None

    def update(self, dt: float, obstaculos: Iterable[pygame.Rect] = ()) -> None:
        """Atualiza posicao via teclado (WASD/Setas + SHIFT) com deslize suave."""
        if self.tempo_sinal_oi > 0:
            self.tempo_sinal_oi = max(0.0, self.tempo_sinal_oi - dt)

        teclas = pygame.key.get_pressed()
        dx = int(teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - int(
            teclas[pygame.K_a] or teclas[pygame.K_LEFT]
        )
        dy = int(teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - int(
            teclas[pygame.K_w] or teclas[pygame.K_UP]
        )

        correndo = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        velocidade = VELOCIDADE_CORRIDA if correndo else VELOCIDADE_JOGADOR

        if dx != 0 or dy != 0:
            comprimento = math.hypot(dx, dy)
            nx = dx / comprimento
            ny = dy / comprimento

            antigo_x = self.pos_x
            self.pos_x += nx * velocidade * dt
            self.pos_x = max(
                self.limites.left + 32, min(self.limites.right - 32, self.pos_x)
            )
            hb = self.hitbox_pes
            for obs in obstaculos:
                if hb.colliderect(obs):
                    self.pos_x = antigo_x
                    break

            antigo_y = self.pos_y
            self.pos_y += ny * velocidade * dt
            self.pos_y = max(
                self.limites.top + 16, min(self.limites.bottom - 36, self.pos_y)
            )
            hb = self.hitbox_pes
            for obs in obstaculos:
                if hb.colliderect(obs):
                    self.pos_y = antigo_y
                    break

            self.tempo_passo += dt * (10.0 if correndo else 7.0)
            self.frame_atual = int(self.tempo_passo) % len(self.frames)
            self.image = self.frames[self.frame_atual]
        else:
            self.image = self.frames[0]

        self.rect.center = (round(self.pos_x), round(self.pos_y))

    def desenhar_extras(self, tela: pygame.Surface) -> None:
        """Desenha o item carregado na bandeja quadrada e o indicador de cumprimento."""
        if self.item_na_mao and self.item_na_mao in self.icones_item:
            icone = self.icones_item[self.item_na_mao]
            caixa = pygame.Rect(self.rect.right - 22, self.rect.centery - 22, 56, 56)
            pygame.draw.rect(tela, (14, 26, 22), caixa.move(4, 4))
            pygame.draw.rect(tela, (249, 247, 242), caixa)
            pygame.draw.rect(tela, (0, 112, 74), caixa, 3)
            tela.blit(icone, icone.get_rect(center=caixa.center))

        if self.tempo_sinal_oi > 0:
            lado = int(72 + (0.65 - self.tempo_sinal_oi) * 72)
            quad = pygame.Rect(0, 0, lado, lado)
            quad.center = self.rect.center
            pygame.draw.rect(tela, (0, 112, 74), quad, 4)
