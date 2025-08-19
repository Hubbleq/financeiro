import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AnaliseFinanceira:
    def __init__(self):
        self.custos_fixos = {
            'aluguel': 0, 'luz': 0, 'agua': 0, 'energia': 0,
            'funcionarios': 0, 'outros': 0
        }
        self.produtos = pd.DataFrame()
        self.volume_vendas_estimado = 1000
        # Markups baseados na pesquisa de mercado (fontes do usuário)
        self.category_markups = {
            'HIGIENE': 0.40,          # Categoria com maior margem
            'BEBIDAS ALCOOLICAS': 0.30,
            'LIMPEZA': 0.35,
            'LATICINIOS': 0.30,
            'CONGELADOS': 0.30,
            'BEBIDAS': 0.25, # Reduzido para competitividade
            'MERCEARIA': 0.25,        # Itens de alto giro
            'GRAOS': 0.25,
            'MASSAS': 0.25,
            'OLEO': 0.25,
            'ACUCAR': 0.25,
            'DEFAULT': 0.30
        }
        
    def definir_custos_fixos(self, custos: Dict[str, float]):
        self.custos_fixos.update(custos)
            
    def definir_volume_vendas(self, volume: int):
        if volume > 0:
            self.volume_vendas_estimado = volume
        else:
            raise ValueError("Volume de vendas deve ser maior que zero")

    def definir_category_markups(self, new_markups: Dict[str, float]):
        for category, markup in new_markups.items():
            self.category_markups[category.upper()] = markup / 100

    def calcular_markup(self, custo_produto: float, categoria: str = None) -> Dict:
        if self.volume_vendas_estimado > 0:
            custos_fixos_por_produto = sum(self.custos_fixos.values()) / self.volume_vendas_estimado
        else:
            custos_fixos_por_produto = 0
            
        custo_total_unitario = custo_produto + custos_fixos_por_produto

        categoria_upper = str(categoria).upper() if categoria else 'DEFAULT'
        markup_value = self.category_markups.get(categoria_upper, self.category_markups['DEFAULT'])

        preco_venda_unitario = custo_total_unitario * (1 + markup_value)
        lucro_unitario = preco_venda_unitario - custo_total_unitario
        
        return {
            'custo_produto_unitario': custo_produto,
            'custo_fixo_alocado_unitario': custos_fixos_por_produto,
            'custo_total_unitario': custo_total_unitario,
            'preco_venda_unitario': preco_venda_unitario,
            'markup_aplicado': markup_value * 100,
            'lucro_unitario': lucro_unitario,
        }
    
    def carregar_produtos_excel(self, arquivo: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(arquivo)
            required_columns = ['Nome_Produto', 'Custo_Compra']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Arquivo deve conter as colunas: {required_columns}")
            if 'Quantidade' not in df.columns:
                df['Quantidade'] = 1
            if 'Categoria' not in df.columns:
                df['Categoria'] = 'DEFAULT'
            df['Custo_Compra'] = pd.to_numeric(df['Custo_Compra'], errors='coerce')
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(1)
            df['Categoria'] = df['Categoria'].fillna('DEFAULT')
            df = df.dropna(subset=['Custo_Compra'])
            self.produtos = df
            return df
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo Excel: {str(e)}")
    
    def calcular_markup_lote(self) -> pd.DataFrame:
        if self.produtos.empty:
            raise ValueError("Nenhum produto carregado.")
        
        resultados = []
        for _, produto in self.produtos.iterrows():
            markup_info = self.calcular_markup(
                produto['Custo_Compra'], 
                produto.get('Categoria')
            )
            
            resultado = {
                'Nome_Produto': produto['Nome_Produto'],
                'Custo_Compra_Unitario': produto['Custo_Compra'],
                'Quantidade': produto['Quantidade'],
                'Categoria': produto.get('Categoria'),
                **markup_info
            }
            resultados.append(resultado)
        
        df = pd.DataFrame(resultados)
        df['preco_venda_total'] = df['preco_venda_unitario'] * df['Quantidade']
        df['lucro_total'] = df['lucro_unitario'] * df['Quantidade']
        return df

    def criar_template_excel(self, arquivo_template: str):
        # Atualiza categorias para refletir a nova estratégia
        dados_template = {
            'Nome_Produto': ['Gatorade 500ML', 'Arroz 5kg', 'Sabão em Pó OMO', 'Cerveja Heineken'],
            'Custo_Compra': [4.69, 15.50, 9.98, 3.99],
            'Quantidade': [12, 20, 24, 1],
            'Categoria': ['BEBIDAS', 'MERCEARIA', 'LIMPEZA', 'BEBIDAS ALCOOLICAS']
        }
        df_template = pd.DataFrame(dados_template)
        df_template.to_excel(arquivo_template, index=False, sheet_name='Produtos')
        print(f"Template criado: {arquivo_template}")