import streamlit as st
import pandas as pd
import plotly.express as px
from analise_financeira import AnaliseFinanceira

st.set_page_config(
    page_title="Análise de Preços Inteligente",
    page_icon="💡",
    layout="wide"
)

@st.cache_resource
def inicializar_sistema():
    return AnaliseFinanceira()

analise = inicializar_sistema()

st.title("💡 Análise de Preços Inteligente")
st.markdown("Uma ferramenta para precificar lotes de produtos de forma rápida e realista.")

# --- Sidebar (Configurações) ---
with st.sidebar:
    st.header("Configurações")
    st.subheader("1. Custos Fixos Mensais")
    aluguel = st.number_input("Aluguel (R$)", value=900.0, step=100.0)
    salario = st.number_input("Salários (R$)", value=1500.0, step=100.0)
    programa = st.number_input("Programa (R$)", value=180.0, step=10.0)
    internet = st.number_input("Internet (R$)", value=100.0, step=10.0)
    contador = st.number_input("Contador (R$)", value=250.0, step=10.0)
    outros = st.number_input("Outros (R$)", value=0.0, step=50.0)
    custos_fixos = {
        'aluguel': aluguel, 'salario': salario, 'programa': programa,
        'internet': internet, 'contador': contador, 'outros': outros
    }
    analise.definir_custos_fixos(custos_fixos)
    st.info(f"Custo Fixo Diário: **R$ {sum(custos_fixos.values())/30:.2f}**")

    st.subheader("2. Margem de Lucro Desejada")
    margem_desejada = st.slider(
        "Margem de Lucro para todos os produtos (%)", 
        min_value=1, max_value=99, value=30, step=1,
        help="A margem de lucro sobre o preço de venda."
    )
    analise.definir_margem_lucro(margem_desejada / 100.0)

# --- Área Principal ---

# --- Calculadora Unitária e Upload ---
col1, col2 = st.columns([0.5, 1.5])

with col1:
    st.subheader("Calculadora Unitária")
    st.write("Para produtos comprados em caixas ou fardos.")
    custo_pacote = st.number_input("Custo do Pacote/Caixa (R$)", min_value=0.01, step=0.1, key="custo_pacote")
    unidades_pacote = st.number_input("Unidades por Pacote", min_value=1, step=1, key="unidades_pacote")
    qtd_pacotes = st.number_input("Qtd. de Pacotes Comprados", min_value=1, step=1, key="qtd_pacotes")
    
    if st.button("Calcular Valores"):
        if unidades_pacote > 0 and custo_pacote > 0:
            custo_unitario = custo_pacote / unidades_pacote
            quantidade_total = unidades_pacote * qtd_pacotes
            calc_col1, calc_col2 = st.columns(2)
            with calc_col1:
                st.metric("Custo por Unidade", f"R$ {custo_unitario:.2f}")
            with calc_col2:
                st.metric("Quantidade Total", f"{quantidade_total} un.")
            st.info("Use estes valores nas colunas 'Custo_Compra' e 'Quantidade' da sua planilha.")

with col2:
    st.subheader("Precificação de Lote")
    uploaded_file = st.file_uploader(
        "Carregue sua planilha para precificar (Nome_Produto, Custo_Compra, Quantidade)",
        type=['xlsx', 'xls']
    )

# --- Resultados ---
if uploaded_file is not None:
    try:
        df_produtos = analise.carregar_produtos_excel(uploaded_file)
        df_resultados = analise.calcular_preco_lote()

        st.header("Resultados da Precificação do Lote")
        
        # Resumo
        total_itens = df_resultados['Quantidade'].sum()
        receita_estimada = df_resultados['preco_venda_total'].sum()
        lucro_estimado = df_resultados['lucro_total'].sum()
        
        resumo_col1, resumo_col2, resumo_col3 = st.columns(3)
        resumo_col1.metric("Total de Itens no Lote", f"{total_itens} unidades")
        resumo_col2.metric("Receita Estimada do Lote", f"R$ {receita_estimada:,.2f}")
        resumo_col3.metric("Lucro Estimado do Lote", f"R$ {lucro_estimado:,.2f}")
        
        tab1, tab2, tab3 = st.tabs(["📄 Tabela de Preços", "📊 Gráficos", "📥 Exportar"])

        with tab1:
            st.write("**Preços Sugeridos por Unidade:**")
            df_display = df_resultados[[
                'Nome_Produto', 'Custo_Compra_Unitario',
                'custo_fixo_alocado_unitario', 'custo_total_unitario', 'preco_venda_unitario', 'lucro_unitario'
            ]].copy()
            df_display.columns = [
                'Produto', 'Custo Compra',
                'Custo Fixo Adic.', 'Custo Final', 'Preço Venda', 'Lucro Unid.'
            ]
            st.dataframe(df_display.style.format({
                'Custo Compra': 'R${:,.2f}',
                'Custo Fixo Adic.': 'R${:,.2f}',
                'Custo Final': 'R${:,.2f}',
                'Preço Venda': 'R${:,.2f}',
                'Lucro Unid.': 'R${:,.2f}'
            }))

        with tab2:
            st.subheader("Análises Visuais do Lote")
            col_graph1, col_graph2 = st.columns(2)
            with col_graph1:
                fig_lucro = px.bar(df_resultados.sort_values('lucro_total', ascending=False).head(15), x='Nome_Produto', y='lucro_total', title='Top 15 Produtos por Lucro Total')
                st.plotly_chart(fig_lucro, use_container_width=True)
                fig_custo_compra = px.histogram(df_resultados, x='Custo_Compra_Unitario', nbins=10, title='Distribuição dos Custos de Compra')
                st.plotly_chart(fig_custo_compra, use_container_width=True)
            with col_graph2:
                fig_receita = px.bar(df_resultados.sort_values('preco_venda_total', ascending=False).head(15), x='Nome_Produto', y='preco_venda_total', title='Top 15 Produtos por Receita Total')
                st.plotly_chart(fig_receita, use_container_width=True)
                fig_lucro_unitario = px.histogram(df_resultados, x='lucro_unitario', nbins=10, title='Distribuição do Lucro por Unidade')
                st.plotly_chart(fig_lucro_unitario, use_container_width=True)

        with tab3:
            st.subheader("Exportar Relatório Completo para Excel")
            if st.button("Gerar e Baixar Relatório Excel"):
                analise.exportar_resultados(df_resultados, 'relatorio_financeiro.xlsx')
                with open('relatorio_financeiro.xlsx', 'rb') as f:
                    st.download_button(
                        label="Clique para Baixar o Excel",
                        data=f.read(),
                        file_name="relatorio_financeiro.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")