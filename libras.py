"""Modulo de gerenciamento e exibicao de sinais em Libras.

Carrega as ilustracoes desenhadas em alta resolucao da pasta data/ com cache
de escala suavizada para exibir gestos claros nos baloes, Briefing e Mural.
"""

import math
import os
from typing import Dict, Tuple

import pygame

from config import SINAIS_LIBRAS, caminho_arquivo


class BibliotecaLibras:
    """Armazena, anima suavemente e faz cache das ilustracoes de Libras."""

    def __init__(self) -> None:
        """Carrega as ilustracoes PNG de cada sinal a partir da pasta data/."""
        self.imagens: Dict[str, pygame.Surface] = {}
        self._cache_escala: Dict[Tuple[str, int, int], pygame.Surface] = {}
        self.tempo_animacao = 0.0
        self._carregar_sinais()

    def _carregar_sinais(self) -> None:
        """Carrega as ilustracoes 2D de cada sinal listado no catalogo."""
        for sinal_id in SINAIS_LIBRAS:
            principal = caminho_arquivo(f"sinal_{sinal_id}.png")
            if os.path.exists(principal):
                img = pygame.image.load(principal).convert_alpha()
            else:
                img = pygame.image.load(
                    caminho_arquivo(f"sinal_{sinal_id}_0.png")
                ).convert_alpha()
            self.imagens[sinal_id] = img

    def atualizar(self, dt: float) -> None:
        """Avanca o temporizador global para animacao sutil dos cartoes."""
        self.tempo_animacao += dt

    def obter_frame(self, sinal_id: str, tamanho: int = 64) -> pygame.Surface:
        """Retorna a ilustracao do sinal redimensionada com leve pulso animado."""
        # Dois niveis sutis de escala para dar vida sem distorcer o desenho
        pulso = 1 if math.sin(self.tempo_animacao * 3.5) > 0.35 else 0
        tam_efetivo = tamanho + (2 if pulso else 0)
        chave = (sinal_id, tam_efetivo, pulso)
        if chave not in self._cache_escala:
            surf = self.imagens[sinal_id]
            self._cache_escala[chave] = pygame.transform.smoothscale(
                surf, (tam_efetivo, tam_efetivo)
            )
        return self._cache_escala[chave]

    @staticmethod
    def obter_info(sinal_id: str) -> dict:
        """Retorna os metadados pedagogicos de um sinal (nome, dica, estacao)."""
        return SINAIS_LIBRAS[sinal_id]
