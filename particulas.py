"""Sistema de particulas e textos flutuantes para retorno visual (juice).

Garante feedback imediato e inclusivo para jogadores surdos e ouvintes:
toda acao (pegar item, acertar sinal, errar, combo) gera retorno visual claro.
"""

import math
import random
from typing import List, Tuple

import pygame


class Particula:
    """Particula simples com velocidade, tempo de vida e encolhimento suave."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        cor: Tuple[int, int, int],
        raio: float,
        vida: float,
    ) -> None:
        """Inicializa uma particula individual."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.raio = raio
        self.vida = vida
        self.vida_max = vida

    def atualizar(self, dt: float) -> bool:
        """Atualiza posicao e vida; retorna False quando expirar."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vida -= dt
        return self.vida > 0

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha a particula proporcional ao tempo de vida restante."""
        fator = max(0.0, self.vida / self.vida_max)
        r = max(1, int(self.raio * fator))
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), r)


class TextoFlutuante:
    """Mensagem curta que sobe e desaparece para reforco visual de acoes."""

    def __init__(
        self,
        texto: str,
        x: float,
        y: float,
        cor: Tuple[int, int, int],
        vida: float = 1.15,
    ) -> None:
        """Inicializa um texto flutuante na tela."""
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.vida = vida
        self.vida_max = vida

    def atualizar(self, dt: float) -> bool:
        """Desloca o texto suavemente para cima; retorna False ao expirar."""
        self.y -= 38.0 * dt
        self.vida -= dt
        return self.vida > 0


class SistemaParticulas:
    """Gerencia todas as particulas, vapores e textos flutuantes ativos."""

    def __init__(self) -> None:
        """Inicializa listas vazias e temporizador de vapor ambiente."""
        self.particulas: List[Particula] = []
        self.textos: List[TextoFlutuante] = []
        self.tempo_vapor = 0.0

    def limpar(self) -> None:
        """Remove todos os efeitos ativos ao trocar ou reiniciar fase."""
        self.particulas.clear()
        self.textos.clear()

    def emitir_explosao(
        self,
        x: float,
        y: float,
        cor: Tuple[int, int, int],
        quantidade: int = 14,
    ) -> None:
        """Emite particulas radiais para celebrar acerto ou destacar erro."""
        for _ in range(quantidade):
            ang = random.uniform(0, math.tau)
            vel = random.uniform(45, 135)
            raio = random.uniform(3.0, 6.5)
            vida = random.uniform(0.35, 0.75)
            self.particulas.append(
                Particula(
                    x,
                    y,
                    math.cos(ang) * vel,
                    math.sin(ang) * vel - 25,
                    cor,
                    raio,
                    vida,
                )
            )

    def emitir_vapor(self, x: float, y: float, dt: float) -> None:
        """Emite particulas leves de vapor sobre a maquina de cafe."""
        self.tempo_vapor += dt
        if self.tempo_vapor >= 0.28:
            self.tempo_vapor = 0.0
            self.particulas.append(
                Particula(
                    x + random.uniform(-8, 8),
                    y,
                    random.uniform(-6, 6),
                    random.uniform(-26, -16),
                    (242, 236, 228),
                    random.uniform(3.0, 5.0),
                    0.85,
                )
            )

    def adicionar_texto(
        self,
        texto: str,
        x: float,
        y: float,
        cor: Tuple[int, int, int],
        vida: float = 1.25,
    ) -> None:
        """Cria um texto flutuante na posicao indicada."""
        self.textos.append(TextoFlutuante(texto, x, y, cor, vida))

    def atualizar(self, dt: float) -> None:
        """Atualiza todas as particulas e textos ativos."""
        self.particulas = [p for p in self.particulas if p.atualizar(dt)]
        self.textos = [t for t in self.textos if t.atualizar(dt)]

    def desenhar(self, tela: pygame.Surface, fonte: pygame.font.Font) -> None:
        """Renderiza particulas e textos flutuantes com contorno de leitura."""
        for p in self.particulas:
            p.desenhar(tela)

        for t in self.textos:
            sombra = fonte.render(t.texto, True, (24, 18, 14))
            frente = fonte.render(t.texto, True, t.cor)
            pos = (int(t.x - frente.get_width() // 2), int(t.y))
            tela.blit(sombra, (pos[0] + 1, pos[1] + 2))
            tela.blit(frente, pos)
