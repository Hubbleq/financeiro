import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AnaliseFinanceira:
    """
    Sistema de análise financeira para mercado autônomo
    Calcula markup ideal baseado em custos fixos e variáveis
    """
    
    def __init__(self):
        self.custos_fixos = {
            'aluguel': 0,
            'luz': 0,
            'agua': 0,
            'energia': 0,
            'funcionarios': 0,
            'outros': 0
        }
        self.margem_lucro_desejada = 0.25  # 25% de margem de lucro
        self.produtos = pd.DataFrame()
        self.volume_vendas_estimado = 1000  # Estimativa padrão de 1000 itens/mês
        
    def definir_custos_fixos(self, custos: Dict[str, float]):
        """Define os custos fixos mensais do mercado"""
        self.custos_fixos.update(custos)
        
    def definir_margem_lucro(self, margem: float):
        """Define a margem de lucro desejada (0.0 a 1.0)"""
        if 0 <= margem <= 1:
            self.margem_lucro_desejada = margem
        else:
            raise ValueError("Margem deve estar entre 0 e 1")
            
    def definir_volume_vendas(self, volume: int):
        """Define o volume de vendas mensal estimado"""
        if volume > 0:
            self.volume_vendas_estimado = volume
        else:
            raise ValueError("Volume de vendas deve ser maior que zero")
    
    def calcular_markup(self, custo_produto: float, quantidade: int = 1, custos_fixos_por_produto: float = None) -> Dict:
        """
        Calcula o markup ideal para um produto
        
        Args:
            custo_produto: Custo de compra do produto por unidade
            quantidade: Quantidade de itens comprados
            custos_fixos_por_produto: Custos fixos alocados por produto (opcional)
            
        Returns:
            Dicionário com informações de markup e preços
        """
        if custos_fixos_por_produto is None:
            # Usa o volume de vendas estimado para alocar custos fixos
            if self.volume_vendas_estimado > 0:
                custos_fixos_por_produto = sum(self.custos_fixos.values()) / self.volume_vendas_estimado
            else:
                custos_fixos_por_produto = 0
            
        # Cálculo do markup
        custo_total_unitario = custo_produto + custos_fixos_por_produto
        preco_venda_unitario = custo_total_unitario / (1 - self.margem_lucro_desejada)
        markup_porcentagem = ((preco_venda_unitario - custo_produto) / custo_produto) * 100
        lucro_unitario = preco_venda_unitario - custo_total_unitario
        
        # Cálculos totais baseados na quantidade
        custo_total_compra = custo_produto * quantidade
        custo_fixo_total = custos_fixos_por_produto * quantidade
        custo_total_geral = custo_total_compra + custo_fixo_total
        preco_venda_total = preco_venda_unitario * quantidade
        lucro_total = lucro_unitario * quantidade
        
        return {
            'custo_produto_unitario': custo_produto,
            'quantidade': quantidade,
            'custo_total_compra': custo_total_compra,
            'custo_fixo_alocado_unitario': custos_fixos_por_produto,
            'custo_fixo_total': custo_fixo_total,
            'custo_total_unitario': custo_total_unitario,
            'custo_total_geral': custo_total_geral,
            'preco_venda_unitario': preco_venda_unitario,
            'preco_venda_total': preco_venda_total,
            'markup_porcentagem': markup_porcentagem,
            'lucro_unitario': lucro_unitario,
            'lucro_total': lucro_total,
            'margem_lucro_real': (lucro_unitario / preco_venda_unitario) * 100
        }
    
    def carregar_produtos_excel(self, arquivo: str) -> pd.DataFrame:
        """
        Carrega produtos de um arquivo Excel
        
        Formato esperado:
        - Nome_Produto: Nome do produto
        - Custo_Compra: Custo de compra do produto por unidade
        - Quantidade: Quantidade de itens comprados (opcional, padrão: 1)
        - Categoria: Categoria do produto (opcional)
        """
        try:
            df = pd.read_excel(arquivo)
            required_columns = ['Nome_Produto', 'Custo_Compra']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Arquivo deve conter as colunas: {required_columns}")
            
            # Adicionar coluna Quantidade se não existir
            if 'Quantidade' not in df.columns:
                df['Quantidade'] = 1
                print("⚠️ Coluna 'Quantidade' não encontrada. Usando quantidade = 1 para todos os produtos.")
            
            # Validar dados
            df['Custo_Compra'] = pd.to_numeric(df['Custo_Compra'], errors='coerce')
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(1)
            df = df.dropna(subset=['Custo_Compra'])
            
            self.produtos = df
            return df
            
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo Excel: {str(e)}")
    
    def calcular_markup_lote(self, custos_fixos_por_produto: float = None) -> pd.DataFrame:
        """
        Calcula markup para todos os produtos carregados
        """
        if self.produtos.empty:
            raise ValueError("Nenhum produto carregado. Use carregar_produtos_excel() primeiro.")
        
        resultados = []
        
        for _, produto in self.produtos.iterrows():
            markup_info = self.calcular_markup(
                produto['Custo_Compra'], 
                produto['Quantidade'],
                custos_fixos_por_produto
            )
            
            resultado = {
                'Nome_Produto': produto['Nome_Produto'],
                'Custo_Compra_Unitario': produto['Custo_Compra'],
                'Quantidade': produto['Quantidade'],
                **markup_info
            }
            
            if 'Categoria' in produto:
                resultado['Categoria'] = produto['Categoria']
                
            resultados.append(resultado)
        
        return pd.DataFrame(resultados)
    
    def gerar_relatorio(self, df_resultados: pd.DataFrame) -> Dict:
        """
        Gera relatório financeiro consolidado
        """
        relatorio = {
            'total_produtos_diferentes': len(df_resultados),
            'total_itens_comprados': df_resultados['Quantidade'].sum(),
            'custo_total_compra': df_resultados['custo_total_compra'].sum(),
            'custo_fixo_total': df_resultados['custo_fixo_total'].sum(),
            'custo_total_geral': df_resultados['custo_total_geral'].sum(),
            'receita_total_estimada': df_resultados['preco_venda_total'].sum(),
            'lucro_total_estimado': df_resultados['lucro_total'].sum(),
            'markup_medio': df_resultados['markup_porcentagem'].mean(),
            'margem_lucro_media': df_resultados['margem_lucro_real'].mean(),
            'produto_mais_caro_unitario': df_resultados.loc[df_resultados['Custo_Compra_Unitario'].idxmax()]['Nome_Produto'],
            'produto_mais_barato_unitario': df_resultados.loc[df_resultados['Custo_Compra_Unitario'].idxmin()]['Nome_Produto'],
            'produto_maior_quantidade': df_resultados.loc[df_resultados['Quantidade'].idxmax()]['Nome_Produto'],
            'markup_maior': df_resultados.loc[df_resultados['markup_porcentagem'].idxmax()]['Nome_Produto'],
            'markup_menor': df_resultados.loc[df_resultados['markup_porcentagem'].idxmin()]['Nome_Produto'],
            'lucro_total_maior': df_resultados.loc[df_resultados['lucro_total'].idxmax()]['Nome_Produto']
        }
        
        return relatorio
    
    def exportar_resultados(self, df_resultados: pd.DataFrame, arquivo_saida: str):
        """Exporta resultados para Excel com formatação profissional"""
        with pd.ExcelWriter(arquivo_saida, engine='xlsxwriter') as writer:
            # Planilha principal - Análise de Produtos
            # Usamos startrow=1 para deixar a primeira linha livre para o título
            # O pandas escreve o cabeçalho automaticamente na linha seguinte.
            df_resultados.to_excel(writer, sheet_name='Analise_Produtos', index=False, startrow=1)
            
            # Gerar relatório
            relatorio = self.gerar_relatorio(df_resultados)
            
            # Planilha de resumo
            df_resumo = pd.DataFrame([
                ['Total de produtos diferentes', relatorio['total_produtos_diferentes']],
                ['Total de itens comprados', f"{relatorio['total_itens_comprados']:,}"],
                ['Custo total de compra', f"R$ {relatorio['custo_total_compra']:,.2f}"],
                ['Custo fixo total', f"R$ {relatorio['custo_fixo_total']:,.2f}"],
                ['Custo total geral', f"R$ {relatorio['custo_total_geral']:,.2f}"],
                ['Receita total estimada', f"R$ {relatorio['receita_total_estimada']:,.2f}"],
                ['Lucro total estimado', f"R$ {relatorio['lucro_total_estimado']:,.2f}"],
                ['Markup médio', f"{relatorio['markup_medio']:.1f}%"],
                ['Margem de lucro média', f"{relatorio['margem_lucro_media']:.1f}%"],
                ['', ''],
                ['PRODUTOS EXTREMOS', ''],
                ['Produto mais caro (unitário)', relatorio['produto_mais_caro_unitario']],
                ['Produto mais barato (unitário)', relatorio['produto_mais_barato_unitario']],
                ['Produto com maior quantidade', relatorio['produto_maior_quantidade']],
                ['Produto com maior lucro total', relatorio['lucro_total_maior']],
                ['Produto com maior markup', relatorio['markup_maior']],
                ['Produto com menor markup', relatorio['markup_menor']]
            ], columns=['Métrica', 'Valor'])
            
            df_resumo.to_excel(writer, sheet_name='Resumo_Financeiro', index=False)
            
            # Planilha de custos fixos
            df_custos = pd.DataFrame([
                ['Aluguel', f"R$ {self.custos_fixos.get('aluguel', 0):,.2f}"],
                ['Luz', f"R$ {self.custos_fixos.get('luz', 0):,.2f}"],
                ['Água', f"R$ {self.custos_fixos.get('agua', 0):,.2f}"],
                ['Energia', f"R$ {self.custos_fixos.get('energia', 0):,.2f}"],
                ['Funcionários', f"R$ {self.custos_fixos.get('funcionarios', 0):,.2f}"],
                ['Outros', f"R$ {self.custos_fixos.get('outros', 0):,.2f}"],
                ['', ''],
                ['TOTAL CUSTOS FIXOS', f"R$ {sum(self.custos_fixos.values()):,.2f}"],
                ['Margem de Lucro', f"{self.margem_lucro_desejada*100:.1f}%"]
            ], columns=['Custo', 'Valor Mensal'])
            
            df_custos.to_excel(writer, sheet_name='Custos_Fixos', index=False)
            
            # Formatação profissional
            workbook = writer.book
            
            # Cores e formatos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center'
            })
            
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'fg_color': '#2E75B6',
                'font_color': 'white',
                'border': 1,
                'align': 'center'
            })
            
            money_format = workbook.add_format({
                'num_format': 'R$ #,##0.00',
                'border': 1,
                'align': 'right'
            })
            
            percent_format = workbook.add_format({
                'num_format': '0.0%',
                'border': 1,
                'align': 'right'
            })
            
            data_format = workbook.add_format({
                'border': 1,
                'align': 'left'
            })
            
            total_format = workbook.add_format({
                'bold': True,
                'fg_color': '#D9E2F3',
                'border': 1,
                'align': 'right'
            })
            
            # Formatar planilha Analise_Produtos
            worksheet_produtos = writer.sheets['Analise_Produtos']
            
            # Título
            worksheet_produtos.merge_range('A1:N1', 'ANÁLISE FINANCEIRA DE PRODUTOS', title_format)
            
            # Observação: o pandas já escreveu o cabeçalho (devido a to_excel with startrow=1)
            # Portanto NÃO escrevemos os cabeçalhos manualmente para evitar duplicação.
            # Precisamos ajustar a posição onde escrevemos os dados formatados.
            # Os dados reais começam em startrow + 1 (ou seja, linha 2 -> índice 2 no Excel é 1-based).
            data_start_row = 2  # 0-based index para xlsxwriter: linha onde começam os dados (após título e cabeçalho)

            # Dados (aplicando formatação por coluna)
            for row_num in range(len(df_resultados)):
                for col_num, col_name in enumerate(df_resultados.columns):
                    value = df_resultados.iloc[row_num][col_name]
                    excel_row = data_start_row + row_num
                    if 'custo' in col_name.lower() or 'preco' in col_name.lower() or 'lucro' in col_name.lower():
                        worksheet_produtos.write(excel_row, col_num, value, money_format)
                    elif 'markup' in col_name.lower() or 'margem' in col_name.lower():
                        # marcar porcentagens: os valores em df_resultados estão em porcentagem (ex: 25.0)
                        worksheet_produtos.write(excel_row, col_num, value / 100, percent_format)
                    else:
                        worksheet_produtos.write(excel_row, col_num, value, data_format)
            
            # Ajustar largura das colunas
            col_widths = [25, 12, 10, 15, 15, 15, 15, 15, 15, 12, 15, 15, 15, 15]
            for i, width in enumerate(col_widths):
                worksheet_produtos.set_column(i, i, width)
            
            # Formatar planilha Resumo_Financeiro
            worksheet_resumo = writer.sheets['Resumo_Financeiro']
            
            # Título
            worksheet_resumo.merge_range('A1:B1', 'RESUMO FINANCEIRO', title_format)
            
            # Cabeçalhos
            worksheet_resumo.write(2, 0, 'Métrica', header_format)
            worksheet_resumo.write(2, 1, 'Valor', header_format)
            
            # Dados
            for row_num in range(len(df_resumo)):
                worksheet_resumo.write(row_num + 3, 0, df_resumo.iloc[row_num]['Métrica'], data_format)
                worksheet_resumo.write(row_num + 3, 1, df_resumo.iloc[row_num]['Valor'], data_format)
            
            # Formatar seção de produtos extremos
            for row_num in range(len(df_resumo)):
                if 'PRODUTOS EXTREMOS' in str(df_resumo.iloc[row_num]['Métrica']):
                    worksheet_resumo.write(row_num + 3, 0, df_resumo.iloc[row_num]['Métrica'], total_format)
                    worksheet_resumo.write(row_num + 3, 1, df_resumo.iloc[row_num]['Valor'], total_format)
            
            # Ajustar largura das colunas
            worksheet_resumo.set_column('A:A', 35)
            worksheet_resumo.set_column('B:B', 25)
            
            # Formatar planilha Custos_Fixos
            worksheet_custos = writer.sheets['Custos_Fixos']
            
            # Título
            worksheet_custos.merge_range('A1:B1', 'CUSTOS FIXOS MENSAIS', title_format)
            
            # Cabeçalhos
            worksheet_custos.write(2, 0, 'Custo', header_format)
            worksheet_custos.write(2, 1, 'Valor Mensal', header_format)
            
            # Dados
            for row_num in range(len(df_custos)):
                worksheet_custos.write(row_num + 3, 0, df_custos.iloc[row_num]['Custo'], data_format)
                worksheet_custos.write(row_num + 3, 1, df_custos.iloc[row_num]['Valor Mensal'], data_format)
                
                # Destacar total
                if 'TOTAL' in str(df_custos.iloc[row_num]['Custo']):
                    worksheet_custos.write(row_num + 3, 0, df_custos.iloc[row_num]['Custo'], total_format)
                    worksheet_custos.write(row_num + 3, 1, df_custos.iloc[row_num]['Valor Mensal'], total_format)
            
            # Ajustar largura das colunas
            worksheet_custos.set_column('A:A', 25)
            worksheet_custos.set_column('B:B', 20)
        
        print(f"Resultados exportados para: {arquivo_saida}")
        print("Planilhas criadas:")
        print("- Analise_Produtos: Análise detalhada de cada produto")
        print("- Resumo_Financeiro: Resumo geral dos resultados")
        print("- Custos_Fixos: Detalhamento dos custos fixos")
    
    def criar_template_excel(self, arquivo_template: str):
        """Cria um template Excel para entrada de dados"""
        dados_template = {
            'Nome_Produto': [
                'Arroz 5kg', 'Feijão 1kg', 'Óleo de Soja 900ml', 'Macarrão 500g',
                'Café 500g', 'Açúcar 1kg', 'Farinha de Trigo 1kg', 'Leite 1L',
                'Pão de Forma', 'Manteiga 500g', 'Queijo 500g', 'Presunto 200g',
                'Banana 1kg', 'Maçã 1kg', 'Tomate 1kg', 'Cebola 1kg',
                'Batata 1kg', 'Cenoura 1kg', 'Alho 100g', 'Cebolinha 1 maço',
                'Salgadinho Cheetos 85g', 'Salgadinho Ruffles 100g', 'Salgadinho Doritos 100g',
                'Biscoito Recheado 130g', 'Biscoito Cream Cracker 200g', 'Chocolate 90g'
            ],
            'Custo_Compra': [
                15.50, 8.90, 12.30, 3.45, 18.75, 4.20, 3.80, 4.50,
                6.80, 8.90, 22.50, 12.80, 5.90, 8.40, 6.20, 4.80,
                3.90, 2.80, 3.50, 1.20, 2.50, 3.20, 3.80, 2.90, 4.50, 5.80
            ],
            'Quantidade': [
                20, 25, 15, 30, 10, 40, 35, 50, 25, 12, 8, 15,
                30, 20, 25, 40, 35, 30, 20, 50, 40, 35, 30, 45, 25, 20
            ],
            'Categoria': [
                'Grãos', 'Grãos', 'Óleos', 'Massas', 'Bebidas', 'Temperos', 'Farinhas', 'Laticínios',
                'Pães', 'Laticínios', 'Laticínios', 'Frios', 'Frutas', 'Frutas', 'Verduras', 'Verduras',
                'Verduras', 'Verduras', 'Temperos', 'Verduras', 'Salgadinhos', 'Salgadinhos', 'Salgadinhos',
                'Biscoitos', 'Biscoitos', 'Chocolates'
            ]
        }
        
        df_template = pd.DataFrame(dados_template)
        
        with pd.ExcelWriter(arquivo_template, engine='xlsxwriter') as writer:
            df_template.to_excel(writer, sheet_name='Produtos', index=False)
            
            # Formatação
            workbook = writer.book
            worksheet = writer.sheets['Produtos']
            
            # Formato para cabeçalhos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Formato para dados
            data_format = workbook.add_format({
                'border': 1
            })
            
            # Aplicar formatação
            for col_num, value in enumerate(df_template.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajustar largura das colunas
            worksheet.set_column('A:A', 25)  # Nome_Produto
            worksheet.set_column('B:B', 12)  # Custo_Compra
            worksheet.set_column('C:C', 12)  # Quantidade
            worksheet.set_column('D:D', 15)  # Categoria
        
        print(f"Template criado: {arquivo_template}")
        print("Colunas obrigatórias: Nome_Produto, Custo_Compra")
        print("Colunas opcionais: Quantidade (padrão: 1), Categoria")
        print("Exemplos incluídos: Grãos, Laticínios, Verduras, Salgadinhos, Biscoitos, etc.")

# Função de exemplo para uso rápido
def exemplo_uso():
    """
    Exemplo de como usar o sistema
    """
    # Inicializar sistema
    analise = AnaliseFinanceira()
    
    # Definir custos fixos mensais
    custos_fixos = {
        'aluguel': 2500,
        'luz': 800,
        'agua': 300,
        'energia': 1200,
        'funcionarios': 4000,
        'outros': 500
    }
    analise.definir_custos_fixos(custos_fixos)
    
    # Definir margem de lucro desejada (25%)
    analise.definir_margem_lucro(0.25)
    
    # Criar template de exemplo
    analise.criar_template_excel('template_produtos.xlsx')
    
    print("Sistema inicializado com sucesso!")
    print("Custos fixos mensais:", custos_fixos)
    print("Margem de lucro definida: 25%")
    print("Template criado: template_produtos.xlsx")
    
    return analise

if __name__ == "__main__":
    exemplo_uso()
