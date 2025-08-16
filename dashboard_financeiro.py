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
st.markdown("""
<div style="
    height: 2px;
    background: linear-gradient(to right, #444444, #666666, #444444);
    margin: 2rem 0;
    border-radius: 1px;
"></div>
""", unsafe_allow_html=True)

# CSS para o tema
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Global Styles */
html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow-x: hidden; /* Prevent horizontal scroll */
}

.stApp {
    background-color: #1A1A1A; /* Very dark gray, almost black */
    color: #E0E0E0; /* Light gray for general text */
    font-family: 'Roboto', sans-serif;
    line-height: 1.6;
    font-size: 16px; /* Base font size */
}

/* Sidebar */
.stSidebar {
    background-color: #2C2C2C; /* Darker gray for sidebar */
    border-right: 1px solid #444444;
    box-shadow: 2px 0 10px rgba(0,0,0,0.5); /* More pronounced shadow */
    padding: 2.5rem 1.5rem; /* Increased padding */
}

/* Headers */
h1 {
    color: #5DADE2; /* Steel Blue for headers */
    font-weight: 700;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #5DADE2;
    font-size: 2rem;
    transition: all 0.3s ease;
}

h2, h3, h4, h5, h6 {
    color: #5DADE2; /* Steel Blue for headers */
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #5DADE2;
    letter-spacing: 0.05rem;
    text-transform: uppercase;
    transition: color 0.3s ease; /* Smooth color transition */
}

.stSidebar h2 {
    color: #5DADE2;
    border-bottom: none;
    margin-top: 2.5rem; /* More space above sidebar subheaders */
    margin-bottom: 1rem;
    font-size: 1.6rem;
}

/* Labels */
label {
    color: #E0E0E0;
    font-weight: 500;
    margin-bottom: 0.6rem; /* Increased space below labels */
    display: block;
}

/* Input Fields */
.stNumberInput, .stTextInput {
    margin-bottom: 1.8rem; /* Increased space between inputs */
}
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    background-color: #3A3A3A; /* Medium dark gray for inputs */
    border-radius: 0.5rem;
    border: 1px solid #555555;
    color: white;
    padding: 0.9rem 1.2rem;
    font-size: 1rem;
    width: 100%;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
}
.stNumberInput>div>div>input:focus, .stTextInput>div>div>input:focus {
    border-color: #5DADE2;
    box-shadow: 0 0 0 0.2rem rgba(93, 173, 226, 0.35); /* Stronger focus shadow */
    background-color: #4A4A4A; /* Slightly lighter on focus */
    outline: none;
}

/* Slider */
.stSlider {
    margin-bottom: 2rem; /* More space for slider */
}
.stSlider .st-bh { /* Slider track */
    background-color: #555555;
    height: 0.6rem;
    border-radius: 0.3rem;
}
.stSlider .st-bi { /* Slider thumb */
    background-color: #5DADE2;
    border: 3px solid #00BFFF;
    width: 1.4rem;
    height: 1.4rem;
    margin-top: -0.4rem;
    transition: background-color 0.3s ease, transform 0.2s ease;
}
.stSlider .st-bi:hover {
    transform: scale(1.2);
}

/* Buttons */
.stButton>button {
    background-color: #5DADE2;
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 0.6rem;
    font-weight: 600;
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    cursor: pointer;
    font-size: 1.05rem;
    box-shadow: 0 3px 8px rgba(93, 173, 226, 0.3);
}
.stButton>button:hover {
    background-color: #009ACD; /* Darker blue on hover */
    transform: translateY(-0.2rem);
    box-shadow: 0 5px 12px rgba(93, 173, 226, 0.4);
}

/* Metrics */
.stMetric {
    background-color: #2C2C2C;
    border-radius: 0.8rem;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stMetric:hover {
    transform: translateY(-0.4rem);
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}
.stMetric > div > div:first-child { /* Metric label */
    color: #AAAAAA;
    font-size: 0.85rem;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.stMetric > div > div:last-child { /* Metric value */
    color: #5DADE2;
    font-size: 1.5rem; /* Further reduced for better fit */
    font-weight: 700;
    overflow-wrap: break-word;
    word-wrap: break-word;
    line-height: 1.1;
    white-space: normal;
}

/* Dataframe */
.stDataFrame {
    border-radius: 0.6rem;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid #444444;
    box-shadow: 0 5px 15px rgba(0,0,0,0.4);
}
.stDataFrame table {
    background-color: #2C2C2C;
    color: #E0E0E0;
    width: 100%;
}
.stDataFrame th {
    background-color: #3A3A3A;
    color: #5DADE2;
    font-weight: 600;
    padding: 1rem 1.2rem;
    text-align: left;
    border-bottom: 2px solid #00BFFF;
}
.stDataFrame td {
        border-top: 1px solid #444444;
    padding: 0.9rem 1.2rem;
}

/* Metric Bar Styling */
.metric-bar {
    height: 5px;
    background-color: #444444; /* Dark grey background */
    border-radius: 2.5px;
    margin-top: 0.5rem;
    overflow: hidden;
}

.metric-bar-fill {
    height: 100%;
    background-color: #5DADE2; /* New accent color */
    width: 100%; /* Static fill for now */
    border-radius: 2.5px;
}


/* Responsive Adjustments */
@media (max-width: 768px) {
    .stApp {
        font-size: 15px;
    }
    .stSidebar {
        padding: 2rem 1rem;
    }
    h1 {
        font-size: 1.8rem;
    }
    h2 {
        font-size: 1.4rem;
    }
    .stMetric {
        padding: 1.2rem;
    }
    .stMetric > div > div:last-child {
        font-size: 1.3rem;
    }
    .stButton>button {
        padding: 0.8rem 1.5rem;
        font-size: 0.9rem;
    }
}

@media (max-width: 480px) {
    .stApp {
        font-size: 14px;
    }
    h1 {
        font-size: 1.5rem;
    }
    h2 {
        font-size: 1.2rem;
    }
    .stMetric > div > div:last-child {
        font-size: 1.1rem;
    }
    .stButton>button {
        padding: 0.7rem 1.2rem;
        font-size: 0.8rem;
    }
}
</style>
""", unsafe_allow_html=True)

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
    # Resumo dos custos
    st.subheader("Resumo")
    total_custos = sum(custos_fixos.values())
    st.metric("Total Custos Fixos", f"R$ {total_custos:,.2f}")
    st.markdown("""
    <div class="metric-bar">
        <div class="metric-bar-fill"></div>
    </div>
    """, unsafe_allow_html=True)
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

        st.markdown("""
<div style="
    height: 2px;
    background: linear-gradient(to right, #444444, #666666, #444444);
    margin: 2rem 0;
    border-radius: 1px;
"></div>
""", unsafe_allow_html=True)
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
st.markdown("""
<div style="
    height: 2px;
    background: linear-gradient(to right, #444444, #666666, #444444);
    margin: 2rem 0;
    border-radius: 1px;
"></div>
""", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Sistema de Análise Financeira para Mercados | Desenvolvido para mercados de bairro</p>
    </div>
    """,
    unsafe_allow_html=True
)