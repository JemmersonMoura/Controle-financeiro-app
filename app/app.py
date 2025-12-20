import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

class ControleFinanceiro:
    def __init__(self):
        self.arquivo_dados = os.path.join(os.path.dirname(__file__), "dados_financeiros.json")
        self.dados = {
            "saldo": 12450.75,
            "salario_jemmerson": 5000.0,
            "salario_vyviane": 4500.0,
            "historico": [],
            "gasto_semana": 1850.40,
            "meta_economia": 2000.00
        }
        self.carregar_dados()

    def carregar_dados(self):
        """Tenta carregar os dados do arquivo JSON se ele existir."""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r') as f:
                self.dados = json.load(f)
        else:
            # If the file doesn't exist, we save the default data.
            self.salvar_dados()

    def salvar_dados(self):
        """Salva o estado atual no arquivo JSON."""
        with open(self.arquivo_dados, 'w') as f:
            json.dump(self.dados, f, indent=4)

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

    def registrar_despesa(self, valor, descricao):
        self.dados["saldo"] -= valor
        self.dados["historico"].append({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "descricao": f"Saída: {descricao}",
            "valor": valor,
            "tipo": "saida"
        })
        self.salvar_dados()

# Instantiate the class once
controle_financeiro = ControleFinanceiro()

@app.route('/')
def index():
    return render_template('index.html', dados=controle_financeiro.dados)

@app.route('/api/dados')
def get_dados():
    dados_completos = controle_financeiro.dados.copy()
    dados_completos['gastos_da_semana_chart'] = [
        {"dia": "Seg", "valor": 120},
        {"dia": "Ter", "valor": 450},
        {"dia": "Qua", "valor": 300},
        {"dia": "Qui", "valor": 75},
        {"dia": "Sex", "valor": 620},
        {"dia": "Sab", "valor": 210},
        {"dia": "Dom", "valor": 150}
    ]
    return jsonify(dados_completos)


if __name__ == '__main__':
    app.run(debug=True)
