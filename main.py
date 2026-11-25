"""Ponto de entrada e loop principal do jogo Sinal Aberto.

Orquestra a maquina de estados (menu, instrucoes, briefing, jogando, mural,
pausa e telas finais), eventos de teclado e mouse, audio, colisoes,
interacoes em Libras e persistencia de progresso.
"""

import math
import os
import sys
from typing import Dict, Optional

import pygame

from cliente import Cliente
from config import (
    ALTURA,
    BONUS_COMBO,
    BONUS_RAPIDEZ_MAX,
    BONUS_SEM_MURAL,
    FPS,
    LARGURA,
    PASTA_DATA,
    PONTOS_ACERTO_BASE,
    RAIO_INTERACAO,
    SINAIS_LIBRAS,
    TITULO_JOGO,
    VIDAS_INICIAIS,
    caminho_arquivo,
)
from estacao import Estacao
from fase import GerenciadorFases
from hud import InterfaceHUD
from libras import BibliotecaLibras
from particulas import SistemaParticulas
from player import Atendente
from save_manager import GerenciadorSave


def _garantir_assets() -> None:
    """Gera automaticamente os sprites e audios se a pasta data/ estiver ausente."""
    arquivo_teste = os.path.join(PASTA_DATA, "atendente_0.png")
    if not os.path.exists(arquivo_teste):
        from gerar_assets import gerar_todos_assets

        gerar_todos_assets()


class JogoSinalAberto:
    """Controlador principal do jogo 2D de atendimento inclusivo em Libras."""

    def __init__(self) -> None:
        """Inicializa Pygame, mixer de audio, assets, entidades e estado inicial."""
        _garantir_assets()
        pygame.init()
        try:
            pygame.mixer.init()
            self.audio_disponivel = True
        except pygame.error:
            self.audio_disponivel = False

        self.tela_cheia = False
        self.tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
        pygame.display.set_caption(TITULO_JOGO)
        self.relogio = pygame.time.Clock()

        self.save = GerenciadorSave()
        self.hud = InterfaceHUD()
        self.libras = BibliotecaLibras()
        self.particulas = SistemaParticulas()
        self.fases = GerenciadorFases()
        self.jogador = Atendente(LARGURA // 2, 390)

        # Aplica preferencias de acessibilidade salvas
        prefs = self.save.dados.get("preferencias", {})
        self.hud.alto_contraste = bool(prefs.get("alto_contraste", False))
        self.hud.fonte_grande = bool(prefs.get("fonte_grande", False))
        if self.hud.fonte_grande:
            self.hud._carregar_fontes()
        self.mudo = bool(prefs.get("mudo", False))

        self.sons: Dict[str, pygame.mixer.Sound] = {}
        self._carregar_sons()

        # Maquina de estados:
        # menu, instrucoes, briefing, jogando, mural, pausa,
        # vitoria_fase, derrota, vitoria_final
        self.estado = "menu"
        self.score = 0
        self.vidas = VIDAS_INICIAIS
        self.mensagem_barra = ""
        self.tempo_mensagem = 0.0
        self.rodando = True

    def _carregar_sons(self) -> None:
        """Carrega trilha sonora em loop e efeitos sonoros WAV da pasta data/."""
        if not self.audio_disponivel:
            return
        nomes = ("acerto", "erro", "pegar", "campainha", "vitoria")
        for nome in nomes:
            try:
                som = pygame.mixer.Sound(caminho_arquivo(f"{nome}.wav"))
                som.set_volume(0.45)
                self.sons[nome] = som
            except pygame.error:
                pass
        try:
            pygame.mixer.music.load(caminho_arquivo("musica.wav"))
            pygame.mixer.music.set_volume(0.0 if self.mudo else 0.25)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def _tocar(self, nome: str) -> None:
        """Reproduz um efeito sonoro se o audio estiver ativo e nao mutado."""
        if not self.mudo and nome in self.sons:
            self.sons[nome].play()

    def _definir_mensagem(self, texto: str, duracao: float = 2.6) -> None:
        """Mostra uma mensagem curta de retorno na barra superior do HUD."""
        self.mensagem_barra = texto
        self.tempo_mensagem = duracao

    def _alternar_tela_cheia(self) -> None:
        """Alterna entre modo janela e tela cheia mantendo proporcao 1024x640."""
        self.tela_cheia = not self.tela_cheia
        flags = pygame.SCALED | (pygame.FULLSCREEN if self.tela_cheia else 0)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA), flags)

    def _alternar_mudo(self) -> None:
        """Liga ou desliga sons e musica salvando a preferencia do jogador."""
        self.mudo = not self.mudo
        if self.audio_disponivel:
            pygame.mixer.music.set_volume(0.0 if self.mudo else 0.25)
        self.save.salvar_preferencias(
            self.hud.alto_contraste, self.hud.fonte_grande, self.mudo
        )

    def _iniciar_nova_partida(self) -> None:
        """Comeca um novo jogo a partir da fase 1."""
        self.score = 0
        self.vidas = VIDAS_INICIAIS
        self._preparar_fase(0)

    def _preparar_fase(self, indice: int) -> None:
        """Configura o estado para o briefing de uma fase especifica."""
        self.vidas = VIDAS_INICIAIS
        self.fases.iniciar_fase(indice)
        self.jogador.resetar(LARGURA // 2, 390)
        self.particulas.limpar()
        self.mensagem_barra = ""
        self.estado = "briefing"

    def _encontrar_alvo_proximo(
        self,
    ) -> tuple[Optional[Estacao], Optional[Cliente]]:
        """Identifica a estacao ou cliente mais proximo dentro do raio de interacao."""
        px, py = self.jogador.rect.center
        melhor_est: Optional[Estacao] = None
        dist_est = RAIO_INTERACAO

        for est in self.fases.grupo_estacoes:
            est.destacada = False
            d = math.hypot(est.rect.centerx - px, est.rect.centery - py)
            if d < dist_est:
                dist_est = d
                melhor_est = est

        melhor_cli: Optional[Cliente] = None
        dist_cli = RAIO_INTERACAO + 42.0  # alcanca atraves do balcao
        for cli in self.fases.grupo_clientes:
            cli.destacado = False
            if cli.estado != "esperando":
                continue
            d = math.hypot(cli.rect.centerx - px, (cli.rect.centery + 52) - py)
            if d < dist_cli:
                dist_cli = d
                melhor_cli = cli

        # Prioriza quem estiver mais proximo
        if melhor_est and melhor_cli:
            if dist_est <= dist_cli:
                melhor_est.destacada = True
                return melhor_est, None
            melhor_cli.destacado = True
            return None, melhor_cli
        if melhor_est:
            melhor_est.destacada = True
        if melhor_cli:
            melhor_cli.destacado = True
        return melhor_est, melhor_cli

    def _interagir(self) -> None:
        """Executa a acao contextual da tecla [E]/[ESPACO] com estacao ou cliente."""
        estacao, cliente = self._encontrar_alvo_proximo()
        p = self.hud.paleta

        if estacao is not None:
            if estacao.estacao_id == "mural":
                self.fases.registrar_consulta_mural()
                self.estado = "mural"
                self._tocar("pegar")
                return
            if estacao.estacao_id == "lixeira":
                if self.jogador.item_na_mao:
                    self.jogador.limpar_mao()
                    self._tocar("pegar")
                    self.particulas.adicionar_texto(
                        "Item descartado",
                        estacao.rect.centerx,
                        estacao.rect.top - 10,
                        p["texto_claro"],
                    )
                return
            if estacao.sinal_associado:
                self.jogador.pegar_item(estacao.sinal_associado)
                self._tocar("pegar")
                nome = SINAIS_LIBRAS[estacao.sinal_associado]["nome"].split("/")[0].strip()
                self.particulas.emitir_explosao(
                    estacao.rect.centerx, estacao.rect.centery, p["destaque"], 8
                )
                self.particulas.adicionar_texto(
                    f"Pegou: {nome}",
                    self.jogador.rect.centerx,
                    self.jogador.rect.top - 14,
                    p["amarelo"],
                )
            return

        if cliente is not None:
            # 1. Se o cliente esta cumprimentando (OI), responde em Libras
            if cliente.precisa_oi:
                ok, tempo = cliente.cumprimentar()
                if ok:
                    self.jogador.acionar_cumprimento()
                    self.fases.registrar_acerto("oi", tempo)
                    self.score += 30
                    self._tocar("acerto")
                    self.particulas.emitir_explosao(
                        cliente.rect.centerx, cliente.rect.centery, p["azul"], 10
                    )
                    self.particulas.adicionar_texto(
                        "OI! +30", cliente.rect.centerx, cliente.rect.top - 20, p["azul"]
                    )
                    self._definir_mensagem("Cumprimento acolhedor! Veja o pedido em Libras.")
                return

            # 2. Entrega do item preparado
            if not self.jogador.item_na_mao:
                self._definir_mensagem("Va ate a estacao do sinal para pegar o item!")
                self._tocar("erro")
                return

            item = self.jogador.item_na_mao
            resultado, tempo, esperado = cliente.entregar_item(item)

            if resultado in ("etapa_ok", "concluido"):
                self.jogador.limpar_mao()
                self.fases.registrar_acerto(esperado, tempo)
                bonus_rapidez = int(cliente.percentual_paciencia * BONUS_RAPIDEZ_MAX)
                ganho = PONTOS_ACERTO_BASE + bonus_rapidez

                if resultado == "concluido":
                    sem_mural = self.fases.concluir_cliente(cliente)
                    if sem_mural:
                        ganho += BONUS_SEM_MURAL
                    ganho += min(100, (self.fases.combo_atual - 1) * BONUS_COMBO)
                    msg_extra = " (Sem Mural!)" if sem_mural else ""
                    self._definir_mensagem(f"Obrigado em Libras! +{ganho} pts{msg_extra}")
                else:
                    self._definir_mensagem("1o sinal certo! Observe o proximo sinal do cliente.")

                self.score += ganho
                self._tocar("acerto")
                self.particulas.emitir_explosao(
                    cliente.rect.centerx, cliente.rect.centery, p["verde"], 18
                )
                self.particulas.adicionar_texto(
                    f"+{ganho}!", cliente.rect.centerx, cliente.rect.top - 22, p["verde"]
                )

                if self.fases.fase_concluida():
                    self._finalizar_fase_com_vitoria()

            elif resultado == "errado":
                self.fases.registrar_erro(esperado)
                self._tocar("erro")
                info_esp = SINAIS_LIBRAS[esperado]
                nome_esp = info_esp["nome"].split("/")[0].strip()
                self.particulas.emitir_explosao(
                    cliente.rect.centerx, cliente.rect.centery, p["vermelho"], 12
                )
                self.particulas.adicionar_texto(
                    f"Era: {nome_esp}!",
                    cliente.rect.centerx,
                    cliente.rect.top - 22,
                    p["vermelho"],
                )
                self._definir_mensagem(
                    f"Dica: esse sinal e {nome_esp} ({info_esp['dica_curta']}).",
                    duracao=4.2,
                )

    def _finalizar_fase_com_vitoria(self) -> None:
        """Persiste estatisticas e avanca para a tela de vitoria correspondente."""
        self.save.registrar_fase(
            numero_fase=self.fases.numero_fase,
            score=self.score,
            atendidos=self.fases.clientes_atendidos,
            sem_mural=self.fases.clientes_sem_mural,
            acertos_sinal=self.fases.acertos_por_sinal,
            erros_sinal=self.fases.erros_por_sinal,
        )
        self._tocar("vitoria")
        if self.fases.numero_fase >= self.fases.total_fases:
            self.estado = "vitoria_final"
        else:
            self.estado = "vitoria_fase"

    def _processar_clique(self, pos: tuple[int, int]) -> None:
        """Trata cliques de mouse nos botoes das telas de interface."""
        for chave, ret in self.hud.botoes_clicaveis.items():
            if ret.collidepoint(pos):
                if chave == "jogar" or chave == "jogar_novamente":
                    self._iniciar_nova_partida()
                elif chave == "instrucoes":
                    self.estado = "instrucoes"
                elif chave == "voltar_menu":
                    self.estado = "menu"
                elif chave == "iniciar_fase":
                    self.estado = "jogando"
                elif chave == "continuar":
                    self.estado = "jogando"
                elif chave == "reiniciar_fase":
                    self._preparar_fase(self.fases.indice_fase)
                    self.estado = "jogando"
                elif chave == "proxima_fase":
                    self._preparar_fase(self.fases.indice_fase + 1)
                break

    def _processar_eventos(self) -> None:
        """Le toda a fila de eventos do Pygame preservando a ordem dos inputs."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                return

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._processar_clique(evento.pos)
                continue

            if evento.type != pygame.KEYDOWN:
                continue

            tecla = evento.key

            # Atalhos globais (tela cheia e acessibilidade) funcionam em qualquer tela
            if tecla == pygame.K_F11 or (
                tecla == pygame.K_RETURN and (evento.mod & pygame.KMOD_ALT)
            ):
                self._alternar_tela_cheia()
                continue
            if tecla == pygame.K_c:
                self.hud.alternar_contraste()
                self.save.salvar_preferencias(
                    self.hud.alto_contraste, self.hud.fonte_grande, self.mudo
                )
                continue
            if tecla == pygame.K_f:
                self.hud.alternar_fonte()
                self.save.salvar_preferencias(
                    self.hud.alto_contraste, self.hud.fonte_grande, self.mudo
                )
                continue
            if tecla == pygame.K_m:
                self._alternar_mudo()
                continue

            # Eventos especificos por estado da maquina
            if self.estado == "menu":
                if tecla in (pygame.K_RETURN, pygame.K_SPACE):
                    self._iniciar_nova_partida()
                elif tecla == pygame.K_i:
                    self.estado = "instrucoes"
                elif tecla == pygame.K_ESCAPE:
                    self.rodando = False

            elif self.estado == "instrucoes":
                if tecla in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                    self.estado = "menu"

            elif self.estado == "briefing":
                if tecla in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = "jogando"
                elif tecla == pygame.K_ESCAPE:
                    self.estado = "menu"

            elif self.estado == "jogando":
                if tecla in (pygame.K_e, pygame.K_SPACE):
                    self._interagir()
                elif tecla == pygame.K_TAB:
                    self.fases.registrar_consulta_mural()
                    self.estado = "mural"
                    self._tocar("pegar")
                elif tecla in (pygame.K_p, pygame.K_ESCAPE):
                    self.estado = "pausa"

            elif self.estado == "mural":
                if tecla in (pygame.K_TAB, pygame.K_ESCAPE, pygame.K_e, pygame.K_SPACE):
                    self.estado = "jogando"

            elif self.estado == "pausa":
                if tecla in (pygame.K_p, pygame.K_ESCAPE):
                    self.estado = "jogando"
                elif tecla == pygame.K_r:
                    self._preparar_fase(self.fases.indice_fase)
                    self.estado = "jogando"

            elif self.estado == "vitoria_fase":
                if tecla in (pygame.K_RETURN, pygame.K_SPACE):
                    self._preparar_fase(self.fases.indice_fase + 1)
                elif tecla == pygame.K_ESCAPE:
                    self.estado = "menu"

            elif self.estado == "derrota":
                if tecla in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                    self._preparar_fase(self.fases.indice_fase)
                    self.estado = "jogando"
                elif tecla == pygame.K_ESCAPE:
                    self.estado = "menu"

            elif self.estado == "vitoria_final":
                if tecla in (pygame.K_RETURN, pygame.K_SPACE):
                    self._iniciar_nova_partida()
                elif tecla == pygame.K_ESCAPE:
                    self.estado = "menu"

    def _atualizar(self, dt: float) -> None:
        """Atualiza animacoes, jogador, clientes e particulas no estado ativo."""
        self.libras.atualizar(dt)

        if self.estado != "jogando":
            return

        if self.tempo_mensagem > 0:
            self.tempo_mensagem = max(0.0, self.tempo_mensagem - dt)
            if self.tempo_mensagem == 0:
                self.mensagem_barra = ""

        colisores = [est.colisor for est in self.fases.grupo_estacoes]
        self.jogador.update(dt, colisores)
        self._encontrar_alvo_proximo()

        entrou, desistencias = self.fases.atualizar(dt)
        if entrou:
            self._tocar("campainha")
        if desistencias > 0:
            self.vidas = max(0, self.vidas - desistencias)
            self._tocar("erro")
            self._definir_mensagem("Um cliente desistiu da fila! Atencao a paciencia.")
            if self.vidas <= 0:
                self.estado = "derrota"

        # Vapor suave saindo da maquina de cafe (estacao na esquerda)
        self.particulas.emitir_vapor(136, 304, dt)
        self.particulas.atualizar(dt)

    def _desenhar_cena_jogo(self) -> None:
        """Renderiza o cenario, estacoes, clientes, jogador, baloes e HUD."""
        self.hud.desenhar_cenario(self.tela)

        # Clientes atras do balcao
        self.fases.grupo_clientes.draw(self.tela)

        # Estacoes e jogador ordenados por Y (profundidade 2.5D)
        desenhaveis = list(self.fases.grupo_estacoes) + [self.jogador]
        desenhaveis.sort(key=lambda sp: sp.rect.bottom)
        for sp in desenhaveis:
            self.tela.blit(sp.image, sp.rect)

        for est in self.fases.grupo_estacoes:
            est.desenhar_rotulo(self.tela, self.hud.f_peq, self.hud.paleta)

        self.jogador.desenhar_extras(self.tela)

        # Baloes de Libras por cima de tudo no cenario
        for cli in self.fases.grupo_clientes:
            cli.desenhar_balao(
                self.tela, self.libras, self.hud.f_peq, self.hud.paleta
            )

        self.particulas.desenhar(self.tela, self.hud.f_flutuante)
        self.hud.desenhar_hud(
            self.tela,
            self.fases,
            self.score,
            self.vidas,
            self.mudo,
            self.mensagem_barra,
        )

    def _desenhar(self) -> None:
        """Desenha o quadro atual conforme a maquina de estados."""
        if self.estado == "menu":
            self.hud.desenhar_menu(
                self.tela, self.save.dados["melhor_score"], self.libras
            )
        elif self.estado == "instrucoes":
            self.hud.desenhar_instrucoes(self.tela)
        elif self.estado == "briefing":
            self.hud.desenhar_briefing(self.tela, self.fases, self.libras)
        elif self.estado == "jogando":
            self._desenhar_cena_jogo()
        elif self.estado == "mural":
            self._desenhar_cena_jogo()
            self.hud.desenhar_mural(self.tela, self.libras)
        elif self.estado == "pausa":
            self._desenhar_cena_jogo()
            self.hud.desenhar_pausa(self.tela)
        elif self.estado in ("vitoria_fase", "derrota", "vitoria_final"):
            self._desenhar_cena_jogo()
            self.hud.desenhar_resultado(self.tela, self.estado, self.fases, self.score)

        pygame.display.flip()

    def executar(self) -> None:
        """Loop principal travado a 60 FPS com delta time independente de hardware."""
        while self.rodando:
            dt = min(self.relogio.tick(FPS) / 1000.0, 0.05)
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    JogoSinalAberto().executar()
