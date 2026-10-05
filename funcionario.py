from datetime import date

class Funcionario:
    """Representa um funcionário da empresa."""

    def __init__(self, nome: str, data_contratacao: date, salario: float):
        self.nome = nome
        self.data_contratacao = data_contratacao
        self.salario = salario

    def anos_de_servico(self) -> int:
        """Retorna quantos anos completos de serviço o funcionário possui."""
        hoje = date.today()
        anos = hoje.year - self.data_contratacao.year
        # Ajuste: se ainda não fez aniversário de contratação neste ano
        if (hoje.month, hoje.day) < (self.data_contratacao.month, self.data_contratacao.day):
            anos -= 1
        return max(anos, 0)

    def aumentar_salario(self, percentual: float) -> None:
        """Aplica um aumento percentual simples ao salário."""
        self.salario *= 1 + percentual / 100

    def __str__(self) -> str:
        return (
            f"Funcionário : {self.nome}\n"
            f"  Contratado em : {self.data_contratacao.strftime('%d/%m/%Y')}\n"
            f"  Anos de serviço: {self.anos_de_servico()}\n"
            f"  Salário       : R$ {self.salario:,.2f}"
        )


class Gerente(Funcionario):
    """Representa um gerente — herda de Funcionario."""

    def aumentar_salario(self, percentual: float) -> None:
        """Aplica o percentual base + 1 % por cada ano de serviço."""
        bonus_antiguidade = self.anos_de_servico()          # 1 % por ano
        percentual_total = percentual + bonus_antiguidade
        self.salario *= 1 + percentual_total / 100

    def __str__(self) -> str:
        return (
            f"Gerente     : {self.nome}\n"
            f"  Contratado em : {self.data_contratacao.strftime('%d/%m/%Y')}\n"
            f"  Anos de serviço: {self.anos_de_servico()}\n"
            f"  Salário       : R$ {self.salario:,.2f}"
        )


# ------------------------------------------------------------------------------
# Demonstração
# ------------------------------------------------------------------------------

def aplicar_reajuste(pessoa: Funcionario, percentual: float) -> None:
    """
    Mensagem polimórfica: recebe qualquer Funcionario (ou subclasse)
    e chama aumentar_salario — o método correto é escolhido em tempo
    de execução (polimorfismo).
    """
    tipo = type(pessoa).__name__
    salario_antes = pessoa.salario
    pessoa.aumentar_salario(percentual)
    salario_depois = pessoa.salario
    diferenca = salario_depois - salario_antes

    print(f"\n{'-' * 52}")
    print(pessoa)                                        
    print(f"  Reajuste base  : {percentual:.1f} %")
    if isinstance(pessoa, Gerente):
        bonus = pessoa.anos_de_servico()
        print(f"  Bônus antiguidade: {bonus} %  ({pessoa.anos_de_servico()} anos × 1 %)")
        print(f"  Percentual total: {percentual + bonus:.1f} %")
    print(f"  Salário antes  : R$ {salario_antes:,.2f}")
    print(f"  Salário depois : R$ {salario_depois:,.2f}")
    print(f"  Ganho          : R$ {diferenca:,.2f}  (+{(diferenca/salario_antes)*100:.2f} %)")


if __name__ == "__main__":
    # Instanciação
    funcionario1 = Funcionario(
        nome="Ana Lima",
        data_contratacao=date(2022, 3, 15),
        salario=3_500.00,
    )

    funcionario2 = Funcionario(
        nome="Carlos Souza",
        data_contratacao=date(2020, 7, 1),
        salario=4_200.00,
    )

    gerente1 = Gerente(
        nome="Beatriz Melo",
        data_contratacao=date(2015, 9, 10),
        salario=9_800.00,
    )

    gerente2 = Gerente(
        nome="Roberto Dias",
        data_contratacao=date(2019, 1, 20),
        salario=11_000.00,
    )

    PERCENTUAL_BASE = 10.0 

    print("=" * 52)
    print("  SISTEMA DE REAJUSTE SALARIAL")
    print("  Percentual base aplicado:", PERCENTUAL_BASE, "%")
    print("=" * 52)

    # -- Mensagem polimórfica ------------------------------
    # A mesma função 'aplicar_reajuste' funciona para
    # Funcionario e Gerente sem nenhuma mudança de código.
    for pessoa in [funcionario1, funcionario2, gerente1, gerente2]:
        aplicar_reajuste(pessoa, PERCENTUAL_BASE)

    print(f"\n{'-' * 52}")
    print("Processamento concluído.")