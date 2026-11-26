"""Gerenciador de fases progressivas, estacoes e metricas pedagogicas.

Controla o fluxo das 4 fases (canal de fluxo), o posicionamento das estacoes,
o nascimento de clientes no balcao e as metricas observaveis de aprendizado
em Libras (taxa de acerto sem consulta ao mural e tempo medio de reacao).
"""

import random
from typing import Dict, List, Optional, Tuple

import pygame

from cliente import Cliente
from config import FASES_CONFIG, PONTOS_BALCAO, SINAIS_LIBRAS
from estacao import Estacao


class GerenciadorFases:
    """Coordena o estado da fase atual, clientes, estacoes e indicadores de impacto."""

    def __init__(self) -> None:
        """Inicializa o gerenciador na fase 1 e cria as estacoes fixas do salao."""
        self.indice_fase = 0
        self.grupo_estacoes = pygame.sprite.Group()
        self.grupo_clientes = pygame.sprite.Group()
        self.slots_ocupados: Dict[int, Optional[Cliente]] = {
            i: None for i in range(len(PONTOS_BALCAO))
        }

        self.tempo_spawn = 0.0
        self.clientes_gerados = 0
        self.clientes_atendidos = 0
        self.clientes_sem_mural = 0
        self.consultas_mural = 0
        self.combo_atual = 0
        self.melhor_combo = 0

        # Metricas pedagogicas por sinal
        self.acertos_por_sinal: Dict[str, int] = {}
        self.erros_por_sinal: Dict[str, int] = {}
        self.tempos_reacao: List[float] = []

        self._montar_estacoes()

    @property
    def config_atual(self) -> dict:
        """Retorna o dicionario de configuracao da fase atual."""
        return FASES_CONFIG[self.indice_fase]

    @property
    def numero_fase(self) -> int:
        """Retorna o numero da fase atual (1 a 4)."""
        return self.config_atual["numero"]

    @property
    def total_fases(self) -> int:
        """Retorna a quantidade total de fases do jogo."""
        return len(FASES_CONFIG)

    def _montar_estacoes(self) -> None:
        """Posiciona as 8 estacoes fisicas no salao Full HD (1920x1080)."""
        definicoes = [
            ("cafe", "CAFE", 248, 560, "cafe"),
            ("agua", "AGUA", 248, 790, "agua"),
            ("bolo", "BOLO", 630, 865, "bolo"),
            ("suco", "SUCO", 960, 865, "suco"),
            ("lixeira", "DESCARTAR", 1290, 865, None),
            ("caixa", "CONTA", 1665, 545, "pagar"),
            ("banheiro", "CHAVE WC", 1665, 735, "banheiro"),
            ("mural", "MURAL [TAB]", 1665, 910, None),
        ]
        self.grupo_estacoes.empty()
        for est_id, rotulo, x, y, sinal in definicoes:
            self.grupo_estacoes.add(Estacao(est_id, rotulo, x, y, sinal))

    def iniciar_fase(self, indice: int) -> None:
        """Reinicia contadores, limpa clientes e prepara a fase escolhida."""
        self.indice_fase = max(0, min(len(FASES_CONFIG) - 1, indice))
        self.grupo_clientes.empty()
        for k in self.slots_ocupados:
            self.slots_ocupados[k] = None

        self.tempo_spawn = self.config_atual["intervalo_spawn"] - 0.6
        self.clientes_gerados = 0
        self.clientes_atendidos = 0
        self.clientes_sem_mural = 0
        self.consultas_mural = 0
        self.combo_atual = 0
        self.melhor_combo = 0
        self.acertos_por_sinal.clear()
        self.erros_por_sinal.clear()
        self.tempos_reacao.clear()

    def registrar_consulta_mural(self) -> None:
        """Marca que o jogador consultou o Mural de Libras durante o atendimento."""
        self.consultas_mural += 1
        for cliente in self.grupo_clientes:
            if cliente.estado == "esperando":
                cliente.consultou_mural_neste = True

    def registrar_acerto(self, sinal_id: str, tempo_reacao: float) -> None:
        """Registra reconhecimento correto de um sinal e seu tempo de resposta."""
        self.acertos_por_sinal[sinal_id] = self.acertos_por_sinal.get(sinal_id, 0) + 1
        if tempo_reacao > 0:
            self.tempos_reacao.append(tempo_reacao)

    def registrar_erro(self, sinal_esperado: str) -> None:
        """Registra erro de interpretacao para o relatorio de revisao final."""
        self.erros_por_sinal[sinal_esperado] = (
            self.erros_por_sinal.get(sinal_esperado, 0) + 1
        )
        self.combo_atual = 0

    def concluir_cliente(self, cliente: Cliente) -> bool:
        """Contabiliza atendimento concluido e informa se houve autonomia plena."""
        self.clientes_atendidos += 1
        self.combo_atual += 1
        if self.combo_atual > self.melhor_combo:
            self.melhor_combo = self.combo_atual
        sem_ajuda = (
            not cliente.consultou_mural_neste and not cliente.usou_apoio_visual
        )
        if sem_ajuda:
            self.clientes_sem_mural += 1
        return sem_ajuda

    def fase_concluida(self) -> bool:
        """Verifica se a meta de clientes atendidos da fase foi atingida."""
        return self.clientes_atendidos >= self.config_atual["meta_clientes"]

    def taxa_autonomia(self) -> float:
        """Calcula percentual de clientes atendidos sem consultar o mural."""
        if self.clientes_atendidos == 0:
            return 0.0
        return (self.clientes_sem_mural / self.clientes_atendidos) * 100.0

    def tempo_medio_reacao(self) -> float:
        """Retorna o tempo medio (em segundos) de reconhecimento dos sinais."""
        if not self.tempos_reacao:
            return 0.0
        return sum(self.tempos_reacao) / len(self.tempos_reacao)

    def sinais_para_revisar(self) -> List[str]:
        """Retorna lista de nomes de sinais que tiveram mais erros na fase."""
        ordenados = sorted(
            self.erros_por_sinal.items(), key=lambda par: par[1], reverse=True
        )
        return [
            SINAIS_LIBRAS[sid]["nome"]
            for sid, qtd in ordenados[:3]
            if qtd > 0 and sid in SINAIS_LIBRAS
        ]

    def _gerar_cliente_se_possivel(self) -> bool:
        """Cria um novo cliente em um lugar livre do balcao, se permitido."""
        cfg = self.config_atual
        ativos = sum(
            1 for c in self.grupo_clientes if c.estado in ("entrando", "esperando")
        )
        restantes_meta = cfg["meta_clientes"] - self.clientes_atendidos
        if ativos >= cfg["max_simultaneos"] or ativos >= restantes_meta:
            return False

        livres = [idx for idx, c in self.slots_ocupados.items() if c is None]
        if not livres:
            return False

        slot = random.choice(livres)
        sinais = cfg["sinais_permitidos"]
        consumiveis = [s for s in sinais if s in ("cafe", "agua", "bolo", "suco")]
        qtd_pedidos = 2 if random.random() < cfg["chance_pedido_duplo"] else 1
        pedidos = random.sample(sinais, k=min(qtd_pedidos, len(sinais)))

        # Quem pede CONTA/PAGAR sempre consome um item antes de pagar
        if "pagar" in pedidos:
            outros = [s for s in pedidos if s != "pagar" and s in consumiveis]
            item_consumo = outros[0] if outros else random.choice(consumiveis)
            pedidos = [item_consumo, "pagar"]

        mostrar_legenda = self.clientes_gerados < cfg["legendas_iniciais"]
        novo = Cliente(
            slot_index=slot,
            destino_balcao=PONTOS_BALCAO[slot],
            pedidos=pedidos,
            paciencia_max=cfg["paciencia_base"],
            mostrar_legenda=mostrar_legenda,
            exige_cumprimento=cfg["exige_cumprimento"],
        )
        self.slots_ocupados[slot] = novo
        self.grupo_clientes.add(novo)
        self.clientes_gerados += 1
        return True

    def atualizar(self, dt: float) -> Tuple[bool, int]:
        """Atualiza cronometro de spawn e clientes ativos.

        Retorna (entrou_novo_cliente, quantidade_desistencias).
        """
        entrou = False
        desistencias = 0

        self.tempo_spawn += dt
        if self.tempo_spawn >= self.config_atual["intervalo_spawn"]:
            if self._gerar_cliente_se_possivel():
                self.tempo_spawn = 0.0
                entrou = True

        for cliente in list(self.grupo_clientes):
            evento = cliente.update(dt)
            if evento == "desistiu":
                desistencias += 1
                self.combo_atual = 0
                if cliente.ultimo_sinal_ativo:
                    self.registrar_erro(cliente.ultimo_sinal_ativo)
            elif evento == "saiu":
                if self.slots_ocupados.get(cliente.slot_index) is cliente:
                    self.slots_ocupados[cliente.slot_index] = None

        return entrou, desistencias
