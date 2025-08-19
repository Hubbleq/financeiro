# Sistema de Análise Financeira - Mercado de Bairro

Sistema inteligente para ajudar donos de mercados de bairro a calcular o preço certo dos produtos, de forma rápida e realista, considerando todos os custos fixos (aluguel, salários, etc.).

## Para que serve?

Ajuda você a descobrir:
- Qual preço cobrar em cada produto, mesmo em compras pequenas.
- Quanto de lucro você pode esperar de cada lote de produtos.
- Como seus custos fixos diários impactam o preço final.
- Uma forma fácil de calcular o custo unitário de produtos comprados em pacotes/fardos.

## O que o sistema faz

### Funcionalidades principais
- **Calcula preços de venda** com base em uma única margem de lucro para todos os produtos.
- **Distribui custos fixos de forma inteligente** por lote de produtos (custo fixo diário).
- **Calculadora de Custo Unitário** para produtos comprados em pacotes/fardos.
- **Importa produtos do Excel** - você só precisa colocar o que comprou.
- **Mostra resultados claros** em tabelas e gráficos.
- **Exporta relatórios completos e profissionais** para Excel, com resumos e gráficos.
- **Cria template** para você preencher seus produtos.

### Informações que você vai ver
- Preço sugerido para cada produto.
- Custo de compra e custo total (com a parte do custo fixo).
- Lucro por unidade e lucro total estimado do lote.
- Resumo geral da receita e lucro do lote.

## Como instalar

### Opção 1: Instalação automática (mais fácil)
1. **Baixe os arquivos** do projeto
2. **Execute o arquivo**: `instalar_dependencias.bat`
3. **Ative o ambiente**: `ativar_ambiente.bat`

### Opção 2: Instalação manual
1. **Crie ambiente virtual**:
   ```bash
   python -m venv .venv
   ```

2. **Ative o ambiente**:
   ```bash
   # Windows
   .venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## Como usar

### Primeiro: Ative o ambiente
```bash
ativar_ambiente.bat
```

### Dashboard (recomendado)
```bash
streamlit run dashboard_financeiro.py
```
**Vantagens:**
- Interface visual, fácil de usar.
- Ajusta custos e margem de lucro em tempo real.
- Faz upload de arquivos Excel.
- **Calculadora de Custo Unitário integrada.**
- Mostra gráficos de análise do lote.
- **Exporta relatórios Excel completos e formatados.**

## Como preparar seu arquivo Excel

### Colunas obrigatórias:
- **Nome_Produto**: Nome do produto
- **Custo_Compra**: Quanto você pagou por unidade (se for pacote, use a calculadora para achar o custo por unidade)
- **Quantidade**: Quantos você comprou (se for pacote, use a calculadora para achar a quantidade total)

### Exemplo de como deve ficar:
| Nome_Produto | Custo_Compra | Quantidade |
|--------------|--------------|------------|
| Arroz 5kg    | 15.50        | 10         |
| Feijão 1kg   | 8.90         | 15         |
| Óleo de Soja | 12.30        | 8          |

## Como o sistema calcula os preços

### 1. Custo Fixo por Produto (para o lote)
O sistema calcula seu custo fixo diário (total de custos fixos mensais / 30 dias) e o distribui igualmente entre todas as unidades de produtos que você carregar na planilha.
```
Custo Fixo por Produto = (Total Custos Fixos Mensais / 30) / Total de Itens no Lote
```

### 2. Custo Total do Produto
```
Custo Total = Custo de Compra por Unidade + Custo Fixo por Produto
```

### 3. Preço de Venda Sugerido
```
Preço de Venda = Custo Total ÷ (1 - Margem de Lucro Desejada)
```

### 4. Lucro por Unidade
```
Lucro por Unidade = Preço de Venda - Custo Total
```

## Custos fixos típicos (por mês)

| **Custo** | **Valor Típico** |
|-----------|------------------|
| **Aluguel** | R$ 900 - 2.500 |
| **Salário** | R$ 1.500 - 4.000 |
| **Programa** | R$ 180 - 300 |
| **Internet** | R$ 100 - 200 |
| **Contador** | R$ 250 - 500 |
| **Outros** | R$ 0 - 500 |

## Arquivos do projeto

```
controle-financeiro/
├── analise_financeira.py          # Lógica de cálculo e exportação
├── dashboard_financeiro.py        # Interface visual (dashboard)
├── requirements.txt               # Bibliotecas necessárias
├── README.md                      # Este arquivo
├── ativar_ambiente.bat            # Ativa o ambiente virtual
├── instalar_dependencias.bat      # Instala as dependências
├── .venv/                         # Ambiente Python (criado automaticamente)
├── template_produtos.xlsx         # Modelo Excel (criado automaticamente)
└── relatorio_financeiro.xlsx      # Relatório Excel completo (gerado pelo sistema)
```

## Precisa de ajuda?

Se tiver dúvidas, o dashboard é a melhor forma de entender o sistema.

---

**Desenvolvido para mercados de bairro**