import streamlit as st
import pandas as pd
from analise_financeira import AnaliseFinanceira

# Configuração da página
st.set_page_config(
    page_title="Análise de Preços - Mercado de Bairro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar sistema
@st.cache_resource
def inicializar_sistema():
    return AnaliseFinanceira()

analise = inicializar_sistema()

st.title("🛒 Análise de Preços para seu Mercado")
st.markdown("Defina preços competitivos com base em uma estratégia de markup por categoria.")

# --- Sidebar --- #
with st.sidebar:
    st.header("Configurações do Seu Negócio")

    with st.expander("1. Custos Fixos Mensais", expanded=True):
        aluguel = st.number_input("Aluguel (R$)", value=2500.0, step=100.0)
        luz = st.number_input("Luz (R$)", value=800.0, step=50.0)
        agua = st.number_input("Água (R$)", value=300.0, step=50.0)
        funcionarios = st.number_input("Funcionários (R$)", value=4000.0, step=500.0)
        outros = st.number_input("Outros (R$)", value=500.0, step=50.0)
        custos_fixos = {
            'aluguel': aluguel, 'luz': luz, 'agua': agua,
            'funcionarios': funcionarios, 'outros': outros
        }
        analise.definir_custos_fixos(custos_fixos)

    with st.expander("2. Estimativa de Vendas", expanded=True):
        volume_vendas = st.number_input(
            "Volume Total de Vendas no Mês (unidades)", 
            value=5000, 
            step=100,
            help="Crucial para distribuir os custos fixos de forma justa."
        )
        analise.definir_volume_vendas(volume_vendas)

    with st.expander("3. Estratégia de Markup (%)", expanded=True):
        st.info("Ajuste o markup para cada categoria. Estes valores são baseados em pesquisa de mercado para varejo.")
        custom_markups = {}
        # Usar uma cópia para evitar modificar o dicionário durante a iteração
        for category, markup in list(analise.category_markups.items()):
            default_value = markup * 100 # Converte para %
            custom_markups[category] = st.number_input(
                f"Markup {category.title()} (%)", 
                value=default_value, 
                step=1.0,
                key=f"markup_{category}" # Chave única para cada input
            )
        analise.definir_category_markups(custom_markups)

# --- Área Principal --- #
st.header("4. Carregue sua Planilha de Produtos")
uploaded_file = st.file_uploader(
    "O arquivo Excel deve conter: Nome_Produto, Custo_Compra, Quantidade, Categoria",
    type=['xlsx', 'xls']
)

if st.button("Gerar Modelo de Planilha Excel"):
    analise.criar_template_excel('template_produtos.xlsx')
    st.success("Modelo gerado: template_produtos.xlsx. Use-o para preencher seus produtos!")
    with open('template_produtos.xlsx', 'rb') as f:
        st.download_button(
            label="Baixar Modelo Excel",
            data=f.read(),
            file_name="template_produtos.xlsx"
        )

if uploaded_file is not None:
    try:
        df_produtos = analise.carregar_produtos_excel(uploaded_file)
        df_resultados = analise.calcular_markup_lote()

        st.header("Resultados da Análise de Preços")
        
        col1, col2 = st.columns(2)
        col1.metric("Receita Total Estimada", f"R$ {df_resultados['preco_venda_total'].sum():,.2f}")
        col2.metric("Lucro Total Estimado", f"R$ {df_resultados['lucro_total'].sum():,.2f}")

        st.subheader("Preços Sugeridos e Markups Aplicados")
        df_display = df_resultados[[
            'Nome_Produto', 'Categoria', 'Custo_Compra_Unitario',
            'custo_fixo_alocado_unitario', 'custo_total_unitario',
            'markup_aplicado', 'preco_venda_unitario', 'lucro_unitario'
        ]].copy()
        df_display.columns = [
            'Produto', 'Categoria', 'Custo de Compra',
            'Custo Fixo p/ Unid.', 'Custo Total p/ Unid.',
            'Markup Aplicado (%)', 'Preço de Venda Sugerido', 'Lucro p/ Unid.'
        ]

        st.dataframe(df_display.style.format({
            'Custo de Compra': 'R$ {:,.2f}',
            'Custo Fixo p/ Unid.': 'R$ {:,.2f}',
            'Custo Total p/ Unid.': 'R$ {:,.2f}',
            'Markup Aplicado (%)': '{:,.1f}%',
            'Preço de Venda Sugerido': 'R$ {:,.2f}',
            'Lucro p/ Unid.': 'R$ {:,.2f}'
        }))

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
