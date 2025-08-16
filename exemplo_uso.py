#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Sistema de Análise Financeira para Mercados
"""

from analise_financeira import AnaliseFinanceira
import pandas as pd

def exemplo_calculo_individual():
    """Exemplo de cálculo para um produto só"""
    print("=" * 60)
    print(" EXEMPLO: CALCULAR PREÇO DE UM PRODUTO")
    print("=" * 60)
    
    # Inicia o sistema
    analise = AnaliseFinanceira()
    
    # Define os custos fixos mensais
    custos_fixos = {
        'aluguel': 2500.0,
        'luz': 800.0,
        'agua': 300.0,
        'energia': 1200.0,
        'funcionarios': 4000.0,
        'outros': 500.0
    }
    analise.definir_custos_fixos(custos_fixos)
    
    # Define quanto quer ganhar (25%)
    analise.definir_margem_lucro(0.25)
    
    # Calcula preço para arroz
    resultado = analise.calcular_markup(custo_produto=15.50, quantidade=10)
    
    print(f" Produto: Arroz 5kg")
    print(f" Custo de compra: R$ {resultado['custo_produto_unitario']:.2f}")
    print(f" Quantidade: {resultado['quantidade']}")
    print(f" Custo total da compra: R$ {resultado['custo_total_compra']:.2f}")
    print(f" Sua parte dos custos fixos: R$ {resultado['custo_fixo_alocado_unitario']:.2f}")
    print(f" Custo total por unidade: R$ {resultado['custo_total_unitario']:.2f}")
    print(f" Preço sugerido por unidade: R$ {resultado['preco_venda_unitario']:.2f}")
    print(f" Preço total sugerido: R$ {resultado['preco_venda_total']:.2f}")
    print(f" Markup: {resultado['markup_porcentagem']:.1f}%")
    print(f" Vai ganhar por unidade: R$ {resultado['lucro_unitario']:.2f}")
    print(f" Vai ganhar no total: R$ {resultado['lucro_total']:.2f}")
    print()

def exemplo_completo():
    """Exemplo completo com vários produtos"""
    print("=" * 60)
    print(" EXEMPLO COMPLETO: ANÁLISE DE VÁRIOS PRODUTOS")
    print("=" * 60)
    
    # Inicia o sistema
    analise = AnaliseFinanceira()
    
    # Define os custos fixos mensais
    custos_fixos = {
        'aluguel': 2500.0,
        'luz': 800.0,
        'agua': 300.0,
        'energia': 1200.0,
        'funcionarios': 4000.0,
        'outros': 500.0
    }
    analise.definir_custos_fixos(custos_fixos)
    
    # Define quanto quer ganhar (25%)
    analise.definir_margem_lucro(0.25)

    # Define a estimativa de vendas (quantos itens espera vender no mês)
    analise.definir_volume_vendas(2500)
    
    # Cria dados de exemplo
    produtos_exemplo = pd.DataFrame({
        'Nome_Produto': [
            'Arroz 5kg', 'Feijão 1kg', 'Óleo de Soja', 'Macarrão 500g',
            'Café 500g', 'Açúcar 1kg', 'Farinha de Trigo 1kg', 'Leite 1L',
            'Pão de Forma', 'Queijo Mussarela 500g'
        ],
        'Custo_Compra': [
            15.50, 8.90, 12.30, 4.20, 18.75, 6.80, 5.90, 4.50, 8.90, 25.80
        ],
        'Quantidade': [
            10, 15, 8, 20, 12, 25, 18, 30, 15, 8
        ],
        'Categoria': [
            'Grãos', 'Grãos', 'Óleos', 'Massas', 'Bebidas', 'Básicos',
            'Básicos', 'Laticínios', 'Pães', 'Laticínios'
        ]
    })
    
    # Carrega os produtos no sistema
    analise.produtos = produtos_exemplo
    
    # Calcula os preços
    df_resultados = analise.calcular_markup_lote()
    
    # Mostra os resultados
    print(" PRODUTOS ANALISADOS:")
    print("-" * 60)
    for _, produto in df_resultados.iterrows():
        print(f"  {produto['Nome_Produto']}")
        print(f"    Custo: R$ {produto['Custo_Compra_Unitario']:.2f} | "
              f"Qtd: {produto['Quantidade']} | "
              f"Preço: R$ {produto['preco_venda_unitario']:.2f} | "
              f"Markup: {produto['markup_porcentagem']:.1f}% | "
              f"Lucro: R$ {produto['lucro_total']:.2f}")
        print()
    
    # Gera relatório
    relatorio = analise.gerar_relatorio(df_resultados)
    
    print(" RELATÓRIO GERAL:")
    print("-" * 60)
    print(f" Produtos diferentes: {relatorio['total_produtos_diferentes']}")
    print(f" Total de itens comprados: {relatorio['total_itens_comprados']:,}")
    print(f" Gastou no total: R$ {relatorio['custo_total_compra']:,.2f}")
    print(f" Vai receber no total: R$ {relatorio['receita_total_estimada']:,.2f}")
    print(f" Vai ganhar no total: R$ {relatorio['lucro_total_estimado']:,.2f}")
    print(f" Markup médio: {relatorio['markup_medio']:.1f}%")
    print(f" Margem de lucro média: {relatorio['margem_lucro_media']:.1f}%")
    print()
    
    print(" TOP 5 PRODUTOS QUE DÃO MAIS LUCRO:")
    print("-" * 60)
    top_lucrativos = df_resultados.nlargest(5, 'lucro_total')
    for i, (_, produto) in enumerate(top_lucrativos.iterrows(), 1):
        print(f"{i}º {produto['Nome_Produto']} - "
              f"Qtd: {produto['Quantidade']} - "
              f"Lucro Total: R$ {produto['lucro_total']:.2f}")
    print()
    
    print(" TOP 5 PRODUTOS COM MAIOR MARKUP:")
    print("-" * 60)
    top_markup = df_resultados.nlargest(5, 'markup_porcentagem')
    for i, (_, produto) in enumerate(top_markup.iterrows(), 1):
        print(f"{i}º {produto['Nome_Produto']} - "
              f"Markup: {produto['markup_porcentagem']:.1f}% - "
              f"Preço Unit: R$ {produto['preco_venda_unitario']:.2f}")
    print()
    
    print(" TOP 5 PRODUTOS COM MAIOR QUANTIDADE:")
    print("-" * 60)
    top_quantidade = df_resultados.nlargest(5, 'Quantidade')
    for i, (_, produto) in enumerate(top_quantidade.iterrows(), 1):
        print(f"{i}º {produto['Nome_Produto']} - "
              f"Quantidade: {produto['Quantidade']} - "
              f"Custo Unit: R$ {produto['Custo_Compra_Unitario']:.2f}")
    print()
    
    print(" PRODUTOS EXTREMOS:")
    print("-" * 60)
    print(f" Produto mais caro (unitário): {relatorio['produto_mais_caro_unitario']}")
    print(f" Produto mais barato (unitário): {relatorio['produto_mais_barato_unitario']}")
    print(f" Produto com maior quantidade: {relatorio['produto_maior_quantidade']}")
    print()
    
    # Exporta os resultados
    analise.exportar_resultados(df_resultados, 'exemplo_resultados.xlsx')
    print(" Resultados exportados para: exemplo_resultados.xlsx")
    print()

if __name__ == "__main__":
    exemplo_calculo_individual()
    exemplo_completo()
    
    print(" Exemplo concluído! Agora você pode usar o sistema.")
    print(" Dica: Execute 'streamlit run dashboard_financeiro.py' para usar a interface visual.")
