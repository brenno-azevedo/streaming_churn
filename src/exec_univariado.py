# -*- coding: utf-8 -*-
"""
exec_univariado.py

Pipeline consolidado de limpeza, saneamento e engenharia de atributos da base de
assinantes, reproduzindo as etapas da análise univariada do notebook.

Uso:
    from exec_univariado import executar_pipeline
    df = executar_pipeline()                  # lê do repositório público do curso
    df = executar_pipeline("dados/base.csv")  # ou de um caminho local
"""

import numpy as np
import pandas as pd

BASE_DADOS = (
    "https://raw.githubusercontent.com/unipds-ciencia-de-dados/ciencia-de-dados/"
    "main/disciplina-01-dados-ia-negocios/disc01-mod03-aula03"
)

COLUNAS_DATA = [
    "data_assinatura",
    "data_cancelamento",
    "data_ultimo_acesso",
    "data_extracao",
]

MAPA_PLANO = {
    "Basico": "básico", "BASICO": "básico", "básico": "básico",
    "Padrao": "padrão", "Padrão": "padrão", "padrão": "padrão",
    "Premium": "premium", "premium": "premium",
}

MAPA_CANAL = {
    "Organico": "orgânico", "orgânico": "orgânico",
    "Indicacao": "indicação", "indicação": "indicação",
    "IG": "instagram", "Instagram": "instagram", "instagram": "instagram",
    "Google": "google", "google": "google",
}


def executar_pipeline(caminho_csv=None, verboso=True):
    """Devolve o DataFrame limpo, deduplicado e enriquecido."""
    caminho_csv = caminho_csv or f"{BASE_DADOS}/clientes_base.csv"

    def log(msg):
        if verboso:
            print(msg)

    log("[1/7] Carregando a base...")
    df = pd.read_csv(caminho_csv)
    log(f"       {len(df)} registros carregados")

    log("[2/7] Padronizando categorias...")
    # A padronização vem ANTES da deduplicação de propósito: sem ela, linhas
    # idênticas escritas com grafias diferentes não são reconhecidas como duplicadas.
    df["plano"] = df["plano"].map(MAPA_PLANO).fillna(df["plano"])
    df["canal_aquisicao"] = df["canal_aquisicao"].map(MAPA_CANAL).fillna(df["canal_aquisicao"])
    df = df.replace("?", np.nan)

    log("[3/7] Removendo duplicatas...")
    antes = len(df)
    df = df.drop_duplicates(subset="cliente_id", keep="first").copy()
    log(f"       {antes - len(df)} registros duplicados removidos")

    log("[4/7] Convertendo datas...")
    for col in COLUNAS_DATA:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    log("[5/7] Aplicando filtros de integridade...")
    antes = len(df)
    dias_ate_ultimo_acesso = (df["data_ultimo_acesso"] - df["data_assinatura"]).dt.days
    df = df[(dias_ate_ultimo_acesso >= 0) | (dias_ate_ultimo_acesso.isnull())].copy()
    df = df[(df["idade"] >= 18) & (df["idade"] <= 90)].copy()
    log(f"       {antes - len(df)} registros inconsistentes removidos")

    log("[6/7] Corrigindo erro de escala em valor_mensal...")
    # Valores como 1990 e 3490 são 19,90 e 34,90 com a vírgula decimal perdida na exportação.
    fora_de_escala = df["valor_mensal"] > 1900
    df.loc[fora_de_escala, "valor_mensal"] = df.loc[fora_de_escala, "valor_mensal"] / 100
    log(f"       {int(fora_de_escala.sum())} valores corrigidos")

    log("[7/7] Criando métricas de negócio...")
    df["recencia"] = (df["data_extracao"] - df["data_ultimo_acesso"]).dt.days
    meses_ativo = (df["data_extracao"] - df["data_assinatura"]).dt.days / 30
    meses_cancelado = (df["data_cancelamento"] - df["data_assinatura"]).dt.days / 30
    df["meses_assinatura"] = np.where(
        df["data_cancelamento"].isnull(), meses_ativo, meses_cancelado
    )
    df["receita_acumulada"] = df["valor_mensal"] * df["meses_assinatura"]

    log(f"\nPipeline concluído: {len(df)} registros finais, {df.shape[1]} colunas")
    return df


if __name__ == "__main__":
    base = executar_pipeline()
    print(base[["plano", "valor_mensal", "recencia", "meses_assinatura", "receita_acumulada"]].head())
