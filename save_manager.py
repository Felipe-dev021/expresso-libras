"""Gerenciador de persistencia em JSON para o jogo Sinal Aberto.

Salva recordes por fase, estatisticas de aprendizado de sinais em Libras
e preferencias de acessibilidade com fallback seguro contra corrupcao.
"""

import json
import os
from typing import Any, Dict

from config import ARQUIVO_SAVE


def _dados_padrao() -> Dict[str, Any]:
    """Retorna a estrutura inicial padrao do arquivo de progresso."""
    return {
        "melhor_score": 0,
        "fases_concluidas": [],
        "total_atendidos": 0,
        "total_sem_mural": 0,
        "sinais_acertados": {},
        "sinais_errados": {},
        "preferencias": {
            "alto_contraste": False,
            "fonte_grande": False,
            "mudo": False,
        },
    }


class GerenciadorSave:
    """Responsavel por carregar e persistir o progresso do jogador em disco."""

    def __init__(self, caminho: str = ARQUIVO_SAVE) -> None:
        """Inicializa o gerenciador carregando dados existentes ou padrao."""
        self.caminho = caminho
        self.dados = self.carregar()

    def carregar(self) -> Dict[str, Any]:
        """Le o JSON de progresso com fallback seguro caso falhe."""
        padrao = _dados_padrao()
        if not os.path.exists(self.caminho):
            return padrao
        try:
            with open(self.caminho, "r", encoding="utf-8") as arq:
                carregado = json.load(arq)
            if not isinstance(carregado, dict):
                return padrao
            for chave, valor in padrao.items():
                if chave not in carregado:
                    carregado[chave] = valor
            if not isinstance(carregado.get("preferencias"), dict):
                carregado["preferencias"] = padrao["preferencias"]
            return carregado
        except (OSError, json.JSONDecodeError, TypeError):
            return padrao

    def salvar(self) -> None:
        """Grava o estado atual em disco de forma atomica e segura."""
        try:
            temp = f"{self.caminho}.tmp"
            with open(temp, "w", encoding="utf-8") as arq:
                json.dump(self.dados, arq, ensure_ascii=False, indent=2)
            os.replace(temp, self.caminho)
        except OSError:
            pass

    def registrar_fase(
        self,
        numero_fase: int,
        score: int,
        atendidos: int,
        sem_mural: int,
        acertos_sinal: Dict[str, int],
        erros_sinal: Dict[str, int],
    ) -> None:
        """Atualiza recordes e historico pedagogico apos uma fase concluida."""
        if score > self.dados["melhor_score"]:
            self.dados["melhor_score"] = score
        if numero_fase not in self.dados["fases_concluidas"]:
            self.dados["fases_concluidas"].append(numero_fase)
            self.dados["fases_concluidas"].sort()

        self.dados["total_atendidos"] += atendidos
        self.dados["total_sem_mural"] += sem_mural

        for sinal, qtd in acertos_sinal.items():
            atual = self.dados["sinais_acertados"].get(sinal, 0)
            self.dados["sinais_acertados"][sinal] = atual + qtd

        for sinal, qtd in erros_sinal.items():
            atual = self.dados["sinais_errados"].get(sinal, 0)
            self.dados["sinais_errados"][sinal] = atual + qtd

        self.salvar()

    def salvar_preferencias(
        self, alto_contraste: bool, fonte_grande: bool, mudo: bool
    ) -> None:
        """Persiste as opcoes de acessibilidade escolhidas pelo jogador."""
        self.dados["preferencias"] = {
            "alto_contraste": alto_contraste,
            "fonte_grande": fonte_grande,
            "mudo": mudo,
        }
        self.salvar()
