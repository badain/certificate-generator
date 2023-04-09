# certificate-generator
Um programa simples para automatizar a geração de certificados dos avaliadores da FEBRACE, mas pode ser estendido para outros propósitos!

## Dependências
- ReportLab `pip install reportlab`
- Unidecode `pip install unidecode`

## Uso
```
usage: certificado.py [-h] [-a ASSINANTES] [-b BACKGROUND] pessoas

positional arguments:
  pessoas               [csv] Dados das pessoas que serão utilizados para
                        geração dos certificados

options:
  -h, --help            show this help message and exit
  -a ASSINANTES, --assinantes ASSINANTES
                        [csv] Dados das pessoas que assinarão os certificados
  -b BACKGROUND, --background BACKGROUND
                        [image] Imagem de fundo do certificado
```

### Arquivos especiais
O programa depende de arquivos especiais, que devem ser obtidos em outras fontes
- Libre Caslon: Disponível no Google Fonts, inserir os arquivos `.ttf` na pasta `fonts` 
- A imagem de fundo do certificado: Disponível para os membros da banca de avaliação, especificar no argumento `--background`
- `pessoas.csv` é o arquivo csv que contém o nome, cargo e horas que os avaliadores passaram na FEBRACE, no formato:
```
nome, cargo, horas
"Sedento do Saber", "Banca de Avaliação", "30"
```
- `signature.csv`é o arquivo csv que contém o nome e título da(s) pessoa(s) assinante do certificado, no formato:
```
nome,titulo
Prof.ª Dr.ª Mestra do Conhecimento,Coordenadora do Curso de Ciências Moleculares
```

### Output
O programa vai gerar um certificado para cada pessoa em `pessoas.csv` e salvá-lo em PDF na pasta `certificados`
