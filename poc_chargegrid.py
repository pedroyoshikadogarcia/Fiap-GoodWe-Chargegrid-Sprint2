import time
import random

POTENCIA_CONTRATADA_KW = 150.0  # Limite máximo que o prédio suporta
CAPACIDADE_MAX_CARREGADOR = 22.0  # Potência máxima de cada carregador comercial

estacoes_recarga = {
    "Estacao_01_VanFrota": {"carro_conectado": True, "potencia_atual_kw": 22.0, "prioridade": "Alta"},
    "Estacao_02_Diretoria": {"carro_conectado": True, "potencia_atual_kw": 22.0, "prioridade": "Media"},
    "Estacao_03_Visitante": {"carro_conectado": True, "potencia_atual_kw": 22.0, "prioridade": "Baixa"}
}

def rodar_algoritmo_dlb(consumo_predio, geracao_solar):
    print("\n" + "=" * 60)
    print(f" LOG CHARGEGRID INTELLIGENCE - MONITORAMENTO EM TEMPO REAL")
    print("=" * 60)
    print(f"[-] Consumo Atual do Prédio: {consumo_predio:.2f} kW")
    print(f"[+] Geração Solar Fotovoltaica: {geracao_solar:.2f} kW")

    demanda_liquida_predio = max(0.0, consumo_predio - geracao_solar)

    demanda_carregadores = sum(estacao["potencia_atual_kw"] for estacao in estacoes_recarga.values())

    demanda_total_sistema = demanda_liquida_predio + demanda_carregadores

    print(f"[~] Demanda Atual dos Carregadores: {demanda_carregadores:.2f} kW")
    print(f"[*] Demanda Total Estimada na Rede: {demanda_total_sistema:.2f} kW / Limite: {POTENCIA_CONTRATADA_KW} kW")

    if demanda_total_sistema > POTENCIA_CONTRATADA_KW:
        print("\n[ ALERTA DE SOBRECARGA DETECTADO! ATUANDO VIA PROTOCOLO DLB ]")
        excesso = demanda_total_sistema - POTENCIA_CONTRATADA_KW
        print(f"Sobrecarga de: {excesso:.2f} kW. Reduzindo carga dos carros de menor prioridade...")
        ordem_corte = ["Baixa", "Media", "Alta"]

        for prioridade in ordem_corte:
            for nome_estacao, dados in estacoes_recarga.items():
                if dados["prioridade"] == prioridade and dados["potencia_atual_kw"] > 0:
                    if excesso >= dados["potencia_atual_kw"]:
                        excesso -= dados["potencia_atual_kw"]
                        print(f" -> [DLB] Estação '{nome_estacao}' ({prioridade}) DESLIGADA temporariamente (0 kW).")
                        dados["potencia_atual_kw"] = 0.0
                    else:
                        dados["potencia_atual_kw"] -= excesso
                        print(
                            f" -> [DLB] Estação '{nome_estacao}' ({prioridade}) LIMITADA para {dados['potencia_atual_kw']:.2f} kW.")
                        excesso = 0
                        break
            if excesso <= 0:
                break
    else:
        print("\n[ STATUS: REDE ESTÁVEL ]")
        print("Potência dentro dos limites. Carregamento em velocidade máxima autorizado.")

        for dados in estacoes_recarga.values():
            dados["potencia_atual_kw"] = CAPACIDADE_MAX_CARREGADOR


if __name__ == "__main__":

    rodar_algoritmo_dlb(consumo_predio=90.0, geracao_solar=45.0)
    time.sleep(2)
    rodar_algoritmo_dlb(consumo_predio=130.0, geracao_solar=0.0)