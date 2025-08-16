# Issue: Exportação para Excel duplica cabeçalho

## Resumo
Ao exportar os resultados para Excel com `AnaliseFinanceira.exportar_resultados`, o cabeçalho da planilha `Analise_Produtos` aparece duplicado.

## Comportamento observado
- O arquivo Excel contém o cabeçalho repetido (duas linhas de cabeçalho) na planilha `Analise_Produtos`.

## Causa provável
- O método usa `DataFrame.to_excel` (que escreve o cabeçalho automaticamente) e também escreve os cabeçalhos manualmente com `worksheet.write`, resultando na duplicação.

## Passos para reproduzir
1. Carregar produtos via `carregar_produtos_excel` ou criar um `DataFrame` de resultados.
2. Chamar `exportar_resultados(df_resultados, 'saida.xlsx')`.
3. Abrir `saida.xlsx` e verificar a planilha `Analise_Produtos`.

## Resultado esperado
- Um único cabeçalho (após o título), sem duplicação.

## Correção
- Usar `startrow` em `to_excel` para posicionar o cabeçalho na linha correta (após o título) e remover a escrita manual duplicada dos cabeçalhos. Documentei a correção e adicionei comentários no código.

## Notas
- Não foi possível criar a issue remota no GitHub a partir deste ambiente (sem credenciais/API). Este arquivo registra a issue localmente para referência e pode ser copiado para o sistema de issues remoto.
