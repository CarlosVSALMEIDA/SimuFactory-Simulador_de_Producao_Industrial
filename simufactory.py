import random
import time


def mostrar_menu():
    print("\n" + "=" * 42)
    print("             SIMUFACTORY")
    print("      Simulador de produção industrial")
    print("=" * 42)
    print("1. Iniciar turno de produção")
    print("2. Ver relatório do último turno")
    print("3. Alterar parâmetros da fábrica")
    print("4. Sair")


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def configurar_fabrica(config):
    print("\n--- Parâmetros da Fábrica ---")
    config["materia_prima"] = ler_inteiro(
        "Quantidade inicial de matéria-prima (1-500): ", 1, 500
    )
    config["taxa_defeito"] = ler_inteiro(
        "Percentual de defeitos esperado (0-50): ", 0, 50
    )
    config["velocidade"] = ler_inteiro(
        "Peças processadas por minuto simulado (1-60): ", 1, 60
    )
    print("Parâmetros atualizados.")


def simular_turno(config):
    print("\n--- Novo turno iniciado ---")
    print("A linha está iniciando...")
    time.sleep(0.5)

    materia_prima_inicial = config["materia_prima"]
    total = materia_prima_inicial
    aprovadas = 0
    defeituosas = 0
    eventos = []

    print("\nSensor da esteira: ATIVO")
    print("Inspeção de qualidade: ATIVA")
    print("-" * 42)

    for numero_peca in range(1, total + 1):
        defeito = random.randint(1, 100) <= config["taxa_defeito"]

        if defeito:
            defeituosas += 1
            status = "REPROVADA"
            eventos.append(f"Peça {numero_peca:03}: {status}")
        else:
            aprovadas += 1
            status = "APROVADA"
            eventos.append(f"Peça {numero_peca:03}: {status}")

        # Mostra atualizações sem transformar a simulação em uma espera longa.
        if numero_peca % config["velocidade"] == 0 or numero_peca == total:
            print(
                f"Peças processadas: {numero_peca}/{total} | "
                f"Aprovadas: {aprovadas} | Defeituosas: {defeituosas}"
            )

    eficiencia = (aprovadas / total * 100) if total else 0
    taxa_real_defeito = (defeituosas / total * 100) if total else 0

    relatorio = {
        "materia_prima_inicial": materia_prima_inicial,
        "total_processado": total,
        "aprovadas": aprovadas,
        "defeituosas": defeituosas,
        "eficiencia": eficiencia,
        "taxa_real_defeito": taxa_real_defeito,
        "eventos": eventos,
    }

    config["materia_prima"] = 0

    print("\n--- Turno finalizado ---")
    imprimir_relatorio(relatorio)
    return relatorio


def imprimir_relatorio(relatorio):
    if not relatorio:
        print("Nenhum turno foi executado ainda.")
        return

    print("\n========== RELATÓRIO INDUSTRIAL ==========")
    print(f"Matéria-prima utilizada: {relatorio['materia_prima_inicial']}")
    print(f"Peças processadas:       {relatorio['total_processado']}")
    print(f"Peças aprovadas:         {relatorio['aprovadas']}")
    print(f"Peças defeituosas:       {relatorio['defeituosas']}")
    print(f"Taxa real de defeitos:   {relatorio['taxa_real_defeito']:.1f}%")
    print(f"Eficiência de qualidade: {relatorio['eficiencia']:.1f}%")
    print("==========================================")

    if relatorio["taxa_real_defeito"] >= 15:
        print("ALERTA: taxa de defeitos elevada. Verifique o processo.")
    elif relatorio["taxa_real_defeito"] > 0:
        print("AVISO: foram encontradas peças defeituosas.")
    else:
        print("STATUS: nenhuma peça defeituosa detectada.")


def main():
    config = {
        "materia_prima": 30,
        "taxa_defeito": 10,
        "velocidade": 5,
    }
    ultimo_relatorio = None

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            if config["materia_prima"] <= 0:
                print("\nSem matéria-prima disponível. Configure a fábrica primeiro.")
            else:
                ultimo_relatorio = simular_turno(config)
        elif opcao == "2":
            imprimir_relatorio(ultimo_relatorio)
        elif opcao == "3":
            configurar_fabrica(config)
        elif opcao == "4":
            print("Encerrando o SimuFactory. Até a próxima!")
            break
        else:
            print("Opção inválida. Escolha de 1 a 4.")


if __name__ == "__main__":
    main()
