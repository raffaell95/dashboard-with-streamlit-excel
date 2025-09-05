import pandas as pd
import streamlit as st
import altair as alt

#CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='DASHBOARD DE VENDAS',
    page_icon='$',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://localhost.com',
        'Report a bug': 'http://localhost.com',
        'About': 'App desenvolvido para demonstração'
    }
)

#---criar datagrame----
df = pd.read_excel(
    io = './datasets/system_extraction.xlsx',
    engine='openpyxl',
    sheet_name='salesreport',
    usecols='A:J',
    nrows=4400
)

#-- Sidebar onde aparecera os filtros
with st.sidebar:
    st.subheader('MENU - DASHBOARD DE VENDAS')
    fVendedor = st.selectbox(
        'Selecione o Vendedor',
        options=df['Vendedor'].unique()
    )

    fProduto = st.selectbox(
        'Selecione o Produto',
        options=df['Produto vendido'].unique()
    )

    fCliente = st.selectbox(
        'Selecione o Cliente',
        options=df['Cliente'].unique()
    )

#Tabela Qtde vendida por produto
tabela1_qtde_produto = df.loc[
    (df['Vendedor'] == fVendedor) &
    (df['Cliente'] == fCliente)
]

tabela1_qtde_produto = tabela1_qtde_produto.groupby('Produto vendido', as_index=False).sum(numeric_only=True)

#Tabela de Vendas e Margem
tabela2_vendas_margem = df.loc[
    (df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]

#Tabela Vendas por Vendedor
tabela3_vendas_por_vendedor = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]

tabela3_vendas_por_vendedor = tabela3_vendas_por_vendedor.groupby('Vendedor', as_index=False).sum(numeric_only=True)
tabela3_vendas_por_vendedor = tabela3_vendas_por_vendedor.drop(columns=['Nº pedido', 'Preço'])

#Tabela Venda por Cliente
tabela4_venda_por_cliente = df.loc[
    (df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto)
]
tabela4_venda_por_cliente = tabela4_venda_por_cliente.groupby('Cliente', as_index=False).sum(numeric_only=True)

#Tabela Vendas Mensais
tabela5_vendas_mensais = df.loc[
    (df['Vendedor'] == fVendedor) &
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]

tabela5_vendas_mensais['mm'] = tabela5_vendas_mensais['Data'].dt.strftime('%m/%Y')

###### PADRÕES ########
COR_GRAFICO = '#9DD1F1'
ALTURA_GRAFICO = 250

#Grafico 1.0 Qtde vendida por produto
graf1_qtde_produto = alt.Chart(tabela1_qtde_produto).mark_bar(
    color=COR_GRAFICO,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9
).encode(
    x = 'Produto vendido',
    y = 'Quantidade',
    tooltip=['Produto vendido', 'Quantidade']
).properties(height=ALTURA_GRAFICO, title='QUANTIDADE VENDIDA POR PRODUTO'
             ).configure_axis(grid=False).configure_view(strokeWidth=0)


#Grafico 1.1 Valor de venda por produto
graf1_valor_produto = alt.Chart(tabela1_qtde_produto).mark_bar(
    color=COR_GRAFICO,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9
).encode(
    x = 'Produto vendido',
    y = 'Quantidade',
    tooltip=['Produto vendido', 'Valor Pedido']
).properties(height=ALTURA_GRAFICO, title='VALOR TOTAL POR PRODUTO'
             ).configure_axis(grid=False).configure_view(strokeWidth=0)

# Grafico Vendas por Vendedor
graf2_vendas_vendedor = alt.Chart(tabela3_vendas_por_vendedor).mark_arc(
    innerRadius=100,
    outerRadius=150,
).encode(
    theta = alt.Theta(field='Valor Pedido', type='quantitative', stack=True),
    color=alt.Color(
        field='Vendedor',
        type='nominal',
        legend=None
    ),
    tooltip=['Vendedor', 'Valor Pedido']
).properties(height=300, width=360, title='VALOR VENDA POR VENDEDOR')
rot2Ve = graf2_vendas_vendedor.mark_text(radius=110, size=14).encode(text='Vendedor')
rot2Vp = graf2_vendas_vendedor.mark_text(radius=180, size=12).encode(text='Valor Pedido')

#Grafico Vendas por Cliente
graf4_vendas_cliente = alt.Chart(tabela4_venda_por_cliente).mark_bar(
    color=COR_GRAFICO,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9
).encode(
    x = 'Cliente',
    y = 'Valor Pedido',
    tooltip=['Cliente', 'Valor Pedido']
).properties(height=ALTURA_GRAFICO, title='VENDAS POR CLIENTE'
             ).configure_axis(grid=False).configure_view(strokeWidth=0)

#Grafico Vendas Mensais
graf5_vendas_mensais = alt.Chart(tabela5_vendas_mensais).mark_line(
    color=COR_GRAFICO,
).encode(
    alt.X('monthdate(Data):T'),
    y = 'Valor Pedido:Q'
).properties(height=ALTURA_GRAFICO, title='VENDAS MENSAIS').configure_axis(grid=False
            ).configure_view(strokeWidth=0)


###### PAGINA PRINCIPAL #######
total_vendas = round(tabela2_vendas_margem['Valor Pedido'].sum(), 2)
total_margem = round(tabela2_vendas_margem['Margem Lucro'].sum(), 2)
porc_margem = int(100*total_margem/total_vendas)

st.header(":bar_chart: DASHBOARD DE VENDAS")

dst1, dst2, dst3, dst4 = st.columns([1,1,1,1])

with dst1:
    st.write('**VENDAS TOTAIS:**')
    st.info(f'R$ {total_vendas}')

with dst2:
    st.write('**MARGEM TOTAL:**')
    st.info(f'R$ {total_margem}')

with dst3:
    st.write('**MARGEM %:**')
    st.info(f'{porc_margem}%')

st.markdown("---")


### COLUNAS DOS GRAFICOS ###
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.altair_chart(graf4_vendas_cliente, use_container_width=True)
    st.altair_chart(graf5_vendas_mensais, use_container_width=True)

with col2:
    st.altair_chart(graf1_qtde_produto, use_container_width=True)
    st.altair_chart(graf1_valor_produto, use_container_width=True)

with col3:
    st.altair_chart(graf2_vendas_vendedor+rot2Ve+rot2Vp)

st.markdown("---")