import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AnaliseFinanceira:
    def __init__(self):
        self.custos_fixos = {
            'aluguel': 0, 'salario': 0, 'programa': 0,
            'internet': 0, 'contador': 0, 'outros': 0
        }
        self.produtos = pd.DataFrame()
        self.margem_lucro_desejada = 0.25
        
    def definir_custos_fixos(self, custos: Dict[str, float]):
        self.custos_fixos.update(custos)

    def definir_margem_lucro(self, margem: float):
        if 0 <= margem < 1:
            self.margem_lucro_desejada = margem
        else:
            raise ValueError("Margem de lucro deve ser um valor entre 0 e 0.99")

    def calcular_preco_venda(self, custo_produto: float, custo_fixo_por_produto: float) -> Dict:
        custo_total_unitario = custo_produto + custo_fixo_por_produto
        preco_venda_unitario = custo_total_unitario / (1 - self.margem_lucro_desejada)
        lucro_unitario = preco_venda_unitario - custo_total_unitario
        
        return {
            'custo_produto_unitario': custo_produto,
            'custo_fixo_alocado_unitario': custo_fixo_por_produto,
            'custo_total_unitario': custo_total_unitario,
            'preco_venda_unitario': preco_venda_unitario,
            'lucro_unitario': lucro_unitario,
        }
    
    def carregar_produtos_excel(self, arquivo: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(arquivo)
            required_columns = ['Nome_Produto', 'Custo_Compra', 'Quantidade']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"O arquivo precisa ter as colunas: {required_columns}")
            df['Custo_Compra'] = pd.to_numeric(df['Custo_Compra'], errors='coerce')
            df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(1)
            df = df.dropna(subset=['Custo_Compra'])
            self.produtos = df
            return df
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo Excel: {str(e)}")
    
    def calcular_preco_lote(self) -> pd.DataFrame:
        if self.produtos.empty:
            raise ValueError("Nenhum produto carregado.")
        
        custo_fixo_mensal_total = sum(self.custos_fixos.values())
        custo_fixo_diario = custo_fixo_mensal_total / 30
        total_itens_lote = self.produtos['Quantidade'].sum()

        if total_itens_lote > 0:
            custo_fixo_por_produto = custo_fixo_diario / total_itens_lote
        else:
            custo_fixo_por_produto = 0

        resultados = []
        for _, produto in self.produtos.iterrows():
            info_preco = self.calcular_preco_venda(produto['Custo_Compra'], custo_fixo_por_produto)
            resultado = {
                'Nome_Produto': produto['Nome_Produto'],
                'Custo_Compra_Unitario': produto['Custo_Compra'],
                'Quantidade': produto['Quantidade'],
                **info_preco
            }
            resultados.append(resultado)
        
        df = pd.DataFrame(resultados)
        df['preco_venda_total'] = df['preco_venda_unitario'] * df['Quantidade']
        df['lucro_total'] = df['lucro_unitario'] * df['Quantidade']
        df['custo_total_compra'] = df['custo_produto_unitario'] * df['Quantidade']
        df['custo_fixo_total'] = df['custo_fixo_alocado_unitario'] * df['Quantidade']
        df['custo_total_geral'] = df['custo_total_unitario'] * df['Quantidade']
        return df

    def gerar_relatorio(self, df_resultados: pd.DataFrame) -> Dict:
        return {
            'total_produtos_diferentes': len(df_resultados),
            'total_itens_comprados': df_resultados['Quantidade'].sum(),
            'custo_total_compra': df_resultados['custo_total_compra'].sum(),
            'custo_fixo_total': df_resultados['custo_fixo_total'].sum(),
            'custo_total_geral': df_resultados['custo_total_geral'].sum(),
            'receita_total_estimada': df_resultados['preco_venda_total'].sum(),
            'lucro_total_estimado': df_resultados['lucro_total'].sum(),
        }

    def exportar_resultados(self, df_resultados: pd.DataFrame, arquivo_saida: str):
        with pd.ExcelWriter(arquivo_saida, engine='xlsxwriter') as writer:
            # Planilha principal - Análise de Produtos
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
                ['Lucro total estimado', f"R$ {relatorio['lucro_total_estimado']:,.2f}"]
            ], columns=['Métrica', 'Valor'])
            df_resumo.to_excel(writer, sheet_name='Resumo_Financeiro', index=False)
            
            # Planilha de custos fixos
            df_custos = pd.DataFrame(list(self.custos_fixos.items()), columns=['Custo', 'Valor Mensal'])
            df_custos.to_excel(writer, sheet_name='Custos_Fixos', index=False)
            
            # Formatação profissional
            workbook = writer.book
            
            # Cores e formatos
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#4F81BD',
                'font_color': 'white',
                'border': 1,
                'align': 'center'
            })
            
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'fg_color': '#4F81BD',
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
            col_widths = [25, 12, 10, 15, 15, 15, 15, 15, 15, 12, 15, 15, 15, 15] # Ajustar conforme as colunas reais
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
            
            # Formatar seção de produtos extremos (se houver)
            # for row_num in range(len(df_resumo)):
            #     if 'PRODUTOS EXTREMOS' in str(df_resumo.iloc[row_num]['Métrica']):
            #         worksheet_resumo.write(row_num + 3, 0, df_resumo.iloc[row_num]['Métrica'], total_format)
            #         worksheet_resumo.write(row_num + 3, 1, df_resumo.iloc[row_num]['Valor'], total_format)
            
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

            # Adicionar gráficos na planilha de resumo
            # Gráfico de Pizza para Custos Fixos
            chart_pie = workbook.add_chart({'type': 'pie'})
            chart_pie.add_series({
                'name':       'Composição dos Custos Fixos',
                'categories': '=Custos_Fixos!$A$4:$A$9', # Ajustado para os dados reais
                'values':     '=Custos_Fixos!$B$4:$B$9', # Ajustado para os dados reais
            })
            chart_pie.set_title({'name': 'Composição dos Custos Fixos Mensais'})
            worksheet_resumo.insert_chart('D2', chart_pie, {'x_offset': 25, 'y_offset': 10})

            # Gráfico de Colunas para Receita vs Custo vs Lucro
            chart_column = workbook.add_chart({'type': 'column'})
            chart_column.add_series({
                'name':       'Receita Estimada',
                'categories': '=Resumo_Financeiro!$A$4',
                'values':     '=Resumo_Financeiro!$B$4',
            })
            chart_column.add_series({
                'name':       'Custo Total Geral',
                'categories': '=Resumo_Financeiro!$A$6',
                'values':     '=Resumo_Financeiro!$B$6',
            })
            chart_column.add_series({
                'name':       'Lucro Estimado',
                'categories': '=Resumo_Financeiro!$A$7',
                'values':     '=Resumo_Financeiro!$B$7',
            })
            chart_column.set_title({'name': 'Receita, Custo e Lucro Estimados'})
            chart_column.set_y_axis({'name': 'Valor (R$)'})
            worksheet_resumo.insert_chart('D18', chart_column, {'x_offset': 25, 'y_offset': 10})

        print(f"Resultados exportados para: {arquivo_saida}")

    def criar_template_excel(self, arquivo_template: str):
        dados_template = {
            'Nome_Produto': ['Leite Longa Vida 1L', 'Macarrão Instantâneo', 'Arroz 5kg'],
            'Custo_Compra': [4.50, 1.50, 15.50],
            'Quantidade': [50, 100, 20]
        }
        df_template = pd.DataFrame(dados_template)
        df_template.to_excel(arquivo_template, index=False, sheet_name='Produtos')
        print(f"Template criado: {arquivo_template}")
