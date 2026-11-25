"""Estacoes fisicas interativas da cafeteria Expresso Libras.

Cada estacao fornece um item ou servico correspondente a um sinal em Libras,
alem do Mural de Referencia e da Lixeira para descartar itens errados.
"""

from typing import Optional

import pygame

from config import caminho_arquivo


class Estacao(pygame.sprite.Sprite):
    """Equipamento interativo posicionado no salao de atendimento."""

    def __init__(
        self,
        estacao_id: str,
        rotulo: str,
        x: int,
        y: int,
        sinal_associado: Optional[str] = None,
    ) -> None:
        """Inicializa a estacao carregando seu sprite e caixa de colisao."""
        super().__init__()
        self.estacao_id = estacao_id
        self.rotulo = rotulo
        self.sinal_associado = sinal_associado
        self.image = pygame.image.load(
            caminho_arquivo(f"estacao_{estacao_id}.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.colisor = pygame.Rect(
            self.rect.left + 16,
            self.rect.top + 60,
            self.rect.width - 32,
            self.rect.height - 72,
        )
        self.destacada = False

    def desenhar_rotulo(
        self,
        tela: pygame.Surface,
        fonte: pygame.font.Font,
        paleta: dict,
    ) -> None:
        """Desenha etiqueta quadrada editorial abaixo da estacao e halo quando proxima."""
        if self.destacada:
            halo = self.rect.inflate(12, 12)
            pygame.draw.rect(tela, paleta["destaque"], halo, width=4)

        txt = fonte.render(self.rotulo, True, paleta["texto_claro"])
        bg = pygame.Rect(
            self.rect.centerx - txt.get_width() // 2 - 12,
            self.rect.bottom - 8,
            txt.get_width() + 24,
            txt.get_height() + 8,
        )
        cor_bg = paleta["destaque"] if self.destacada else paleta["hud_bg"]
        cor_txt = paleta["texto_escuro"] if self.destacada else paleta["texto_claro"]
        pygame.draw.rect(tela, paleta["sombra"], bg.move(3, 3))
        pygame.draw.rect(tela, cor_bg, bg)
        pygame.draw.rect(tela, paleta["hud_borda"], bg, width=2)
        txt_final = fonte.render(self.rotulo, True, cor_txt)
        tela.blit(txt_final, (bg.x + 12, bg.y + 4))
