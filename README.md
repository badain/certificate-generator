# certificate-generator
Um programa simples para automatizar a geração de certificados dos avaliadores da FEBRACE, mas pode ser estendido para outros propósitos!


## Dependências
- ReportLab `pip install reportlab`
- Unidecode `pip install unidecode`

### Arquivos especiais
O programa depende de arquivos especiais, que devem ser obtidos em outras fontes
- Libre Caslon: Disponível no Google Fonts, inserir os arquivos `.ttf` na pasta `fonts` 
- A imagem de fundo do certificado: Disponível para os membros da banca de avaliação, inserir `background.png` na pasta `background`
- `pessoas.csv` é o arquivo csv que contém o nome, cargo e horas que os avaliadores passaram na FEBRACE, no formato:

```
nome, cargo, horas
"Sedento do Saber", "Banca de Avaliação", "30"
```

### Output
O programa vai gerar um certificado para cada pessoa em `pessoas.csv` e salvá-lo em PDF na pasta `certificados`
