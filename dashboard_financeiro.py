import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from analise_financeira import AnaliseFinanceira
import io

# Configuração da página
st.set_page_config(
    page_title="Análise Financeira - Mercado",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("Sistema de Análise Financeira - Mercado")
st.markdown("---")

# Inicializar sistema
@st.cache_resource
def inicializar_sistema():
    return AnaliseFinanceira()

analise = inicializar_sistema()

# Sidebar para configurações
with st.sidebar:
    st.header("Seus Custos Mensais")
    
    # Custos fixos
    st.subheader("Custos Fixos")
    aluguel = st.number_input("Aluguel (R$)", value=2500.0, step=100.0)
    luz = st.number_input("Luz (R$)", value=800.0, step=50.0)
    agua = st.number_input("Água (R$)", value=300.0, step=50.0)
    energia = st.number_input("Energia (R$)", value=1200.0, step=100.0)
    funcionarios = st.number_input("Funcionários (R$)", value=4000.0, step=500.0)
    outros = st.number_input("Outros (R$)", value=500.0, step=50.0)
    
    custos_fixos = {
        'aluguel': aluguel,
        'luz': luz,
        'agua': agua,
        'energia': energia,
        'funcionarios': funcionarios,
        'outros': outros
    }
    
    analise.definir_custos_fixos(custos_fixos)
    
    # Margem de lucro
    st.subheader("Quanto quer ganhar?")
    margem_lucro = st.slider("Margem de Lucro (%)", 10, 50, 25) / 100
    analise.definir_margem_lucro(margem_lucro)

    # Volume de vendas
    st.subheader("Estimativa de Vendas")
    volume_vendas = st.number_input("Itens vendidos por mês", min_value=1, value=1000, step=100, help="Quantos itens você espera vender no total por mês? Isso ajuda a dividir os custos fixos.")
    analise.definir_volume_vendas(volume_vendas)
    
    # Resumo dos custos
    st.subheader("Resumo")
    total_custos = sum(custos_fixos.values())
    st.metric("Total Custos Fixos", f"R$ {total_custos:,.2f}")
    st.metric("Margem de Lucro", f"{margem_lucro*100:.1f}%")

# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Seus Produtos")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Carregar arquivo Excel com seus produtos",
        type=['xlsx', 'xls'],
        help="Arquivo deve ter: Nome_Produto, Custo_Compra, Quantidade (opcional), Categoria (opcional)"
    )
    
    # Botão para criar template
    if st.button("Criar modelo Excel"):
        analise.criar_template_excel('template_produtos.xlsx')
        st.success("Modelo criado: template_produtos.xlsx")
        
        # Download do template
        with open('template_produtos.xlsx', 'rb') as f:
            st.download_button(
                label="Baixar Modelo",
                data=f.read(),
                file_name="template_produtos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with col2:
    st.header("Resumo Rápido")
    
    if uploaded_file is not None:
        try:
            # Carregar dados
            df_produtos = analise.carregar_produtos_excel(uploaded_file)
            st.success(f"{len(df_produtos)} produtos carregados")
            
            # Calcular markup
            df_resultados = analise.calcular_markup_lote()
            
            # Métricas principais
            st.metric("Total Produtos", len(df_resultados))
            st.metric("Total Itens", f"{df_resultados['Quantidade'].sum():,}")
            st.metric("Gastou", f"R$ {df_resultados['custo_total_compra'].sum():,.2f}")
            st.metric("Vai receber", f"R$ {df_resultados['preco_venda_total'].sum():,.2f}")
            st.metric("Vai ganhar", f"R$ {df_resultados['lucro_total'].sum():,.2f}")
            
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {str(e)}")

# Análise detalhada
if uploaded_file is not None:
    try:
        df_produtos = analise.carregar_produtos_excel(uploaded_file)
        df_resultados = analise.calcular_markup_lote()
        
        st.markdown("---")
        st.header("Análise dos Produtos")
        
        # Tabs para diferentes visualizações
        tab1, tab2, tab3 = st.tabs([
            "Resultados", "Gráficos", "Exportar"
        ])
        
        with tab1:
            st.subheader("Preços Sugeridos")
            
            # Filtros simples
            col1, col2 = st.columns(2)
            with col1:
                if 'Categoria' in df_resultados.columns:
                    categorias = ['Todas'] + list(df_resultados['Categoria'].unique())
                    categoria_filtro = st.selectbox("Filtrar por Categoria", categorias)
                    
                    if categoria_filtro != 'Todas':
                        df_filtrado = df_resultados[df_resultados['Categoria'] == categoria_filtro]
                    else:
                        df_filtrado = df_resultados
                else:
                    df_filtrado = df_resultados
            
            # Tabela de resultados simplificada
            colunas_mostrar = ['Nome_Produto', 'Custo_Compra_Unitario', 'Quantidade', 'preco_venda_unitario', 'lucro_total']
            df_mostrar = df_filtrado[colunas_mostrar].copy()
            df_mostrar.columns = ['Produto', 'Custo Unit.', 'Qtd', 'Preço Sugerido', 'Lucro Total']
            
            st.dataframe(
                df_mostrar.round(2),
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.subheader("Visualizações")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de preços por produto
                fig_precos = px.bar(
                    df_resultados.head(15),
                    x='Nome_Produto',
                    y='preco_venda_unitario',
                    title='Preços Sugeridos por Produto (Top 15)',
                    labels={'preco_venda_unitario': 'Preço (R$)', 'Nome_Produto': 'Produto'}
                )
                fig_precos.update_xaxes(tickangle=45)
                st.plotly_chart(fig_precos, use_container_width=True)
                
                # Distribuição de custos
                fig_custos = px.histogram(
                    df_resultados,
                    x='Custo_Compra_Unitario',
                    nbins=15,
                    title='Distribuição dos Custos de Compra',
                    labels={'Custo_Compra_Unitario': 'Custo (R$)', 'count': 'Quantidade'}
                )
                st.plotly_chart(fig_custos, use_container_width=True)
            
            with col2:
                # Gráfico de lucro por produto
                fig_lucro = px.bar(
                    df_resultados.head(15),
                    x='Nome_Produto',
                    y='lucro_total',
                    title='Lucro Total por Produto (Top 15)',
                    labels={'lucro_total': 'Lucro (R$)', 'Nome_Produto': 'Produto'}
                )
                fig_lucro.update_xaxes(tickangle=45)
                st.plotly_chart(fig_lucro, use_container_width=True)
                
                # Gráfico de pizza - custos fixos
                fig_custos_fixos = px.pie(
                    values=list(custos_fixos.values()),
                    names=list(custos_fixos.keys()),
                    title='Seus Custos Fixos'
                )
                st.plotly_chart(fig_custos_fixos, use_container_width=True)
        
        with tab3:
            st.subheader("Exportar Resultados")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Exportar para Excel"):
                    analise.exportar_resultados(df_resultados, 'resultados_analise_financeira.xlsx')
                    st.success("Arquivo exportado: resultados_analise_financeira.xlsx")
                    
                    # Download do arquivo
                    with open('resultados_analise_financeira.xlsx', 'rb') as f:
                        st.download_button(
                            label="Baixar Resultados",
                            data=f.read(),
                            file_name="resultados_analise_financeira.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            with col2:
                # Exportar CSV
                csv = df_resultados.to_csv(index=False)
                st.download_button(
                    label="Exportar CSV",
                    data=csv,
                    file_name="resultados_analise_financeira.csv",
                    mime="text/csv"
                )
    
    except Exception as e:
        st.error(f"Erro na análise: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Sistema de Análise Financeira para Mercados | Desenvolvido para mercados de bairro</p>
    </div>
    """,
    unsafe_allow_html=True
)
