import os
import json
from datetime import datetime

class ControleFinanceiro:
    def __init__(self):
        self.arquivo_dados = "dados_financeiros.json"
        self.dados = {
            "saldo": 0.0,
            "salario_jemmerson": 0.0,
            "salario_vyviane": 0.0,
            "historico": []
        }
        self.carregar_dados()

    def carregar_dados(self):
        """Tenta carregar os dados do arquivo JSON se ele existir."""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r') as f:
                self.dados = json.load(f)
            print("Dados carregados com sucesso!")
        else:
            print("Nenhum dado salvo encontrado. Iniciando nova configuração.")
            self.configurar_valores_iniciais()

    def salvar_dados(self):
        """Salva o estado atual no arquivo JSON."""
        with open(self.arquivo_dados, 'w') as f:
            json.dump(self.dados, f, indent=4)

    def configurar_valores_iniciais(self):
        print("\n--- CONFIGURAÇÃO INICIAL ---")
        try:
            self.dados["saldo"] = float(input("Digite o SALDO ATUAL da conta bancária: R$ "))
            self.dados["salario_jemmerson"] = float(input("Digite o Salário Líquido de JEMMERSON: R$ "))
            self.dados["salario_vyviane"] = float(input("Digite o Salário Líquido de VYVIANE: R$ "))
            self.salvar_dados()
            print("Configuração salva!")
        except ValueError:
            print("Erro: Digite apenas números.")

    def receber_salarios_mensais(self):
        total_salarios = self.dados["salario_jemmerson"] + self.dados["salario_vyviane"]
        self.dados["saldo"] += total_salarios
        
        self.dados["historico"].append({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "descricao": "Entrada: Salários Mensais",
            "valor": total_salarios,
            "tipo": "entrada"
        })
        self.salvar_dados()
        print(f"\nSalários adicionados! Novo Saldo: R$ {self.dados['saldo']:.2f}")

    def registrar_despesa(self):
        try:
            valor = float(input("Digite o valor da despesa: R$ "))
            descricao = input("Descrição da despesa: ")
            
            self.dados["saldo"] -= valor
            self.dados["historico"].append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "descricao": f"Saída: {descricao}",
                "valor": valor,
                "tipo": "saida"
            })
            self.salvar_dados()
            print("Despesa salva!")
        except ValueError:
            print("Valor inválido.")

    def ver_extrato(self):
        print("\n" + "="*30)
        print("       EXTRATO FINANCEIRO       ")
        print("="*30)
        for mov in self.dados["historico"]:
            sinal = "+" if mov['tipo'] == "entrada" else "-"
            # Código de cor simples (pode não funcionar em todos terminais windows, mas não quebra o código)
            print(f"[{mov['data']}] {mov['descricao']:<25} | {sinal} R$ {mov['valor']:.2f}")
        
        print("-" * 30)
        print(f"SALDO ATUAL: R$ {self.dados['saldo']:.2f}")
        print("="*30)

    def redefinir_configuracoes(self):
        """Caso queira mudar os salários base no futuro"""
        self.configurar_valores_iniciais()

# --- PROGRAMA PRINCIP