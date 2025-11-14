# Analisador de Custos para YouTube (GV-AUTOMATION)

Este projeto é uma ferramenta de automação em Python projetada para interagir com a API do YouTube, coletar dados de vídeos de um canal específico e gerar um relatório detalhado de custos, simplificando o processo de contabilidade e cobrança para programas e podcasts.

## O Problema que Ele Resolve

Fazer a contabilidade manual de um programa no YouTube, que envolve verificar a data de cada episódio, sua duração e calcular o custo com base em um valor por hora, é um processo demorado, repetitivo e sujeito a erros. Este projeto automatiza completamente essa tarefa, fornecendo um relatório preciso e consolidado em segundos.

## Funcionalidades Principais

- **Busca Inteligente de Vídeos**: Busca todos os vídeos (lives e uploads) de um canal dentro de um período de tempo específico.
- **Gerenciamento de Fuso Horário**: Lida de forma robusta com as diferenças de fuso horário (UTC da API vs. horário local de Brasília), garantindo que os vídeos sejam atribuídos ao dia correto de sua exibição.
- **Configuração Externa**: Parâmetros como o mês/ano da busca e o valor cobrado por hora são definidos em um arquivo `config.json`, permitindo alterar a análise sem modificar o código.
- **Extração de Dados Detalhada**: Para cada vídeo encontrado, o script extrai:
  - Número do episódio.
  - Nome do convidado (limpando o resto do título).
  - Horário exato de início (priorizando o início real da live).
  - Duração precisa do vídeo.
  - Horário de término calculado.
  - Link direto para o vídeo.
- **Cálculo Automático de Custos**: Calcula o custo de cada episódio com base na sua duração e no valor por hora definido no arquivo de configuração.
- **Relatório Completo no Terminal**: Exibe um relatório detalhado para cada episódio e, ao final, um resumo geral com:
  - Total de episódios no mês.
  - Tempo total de gravação (em minutos e no formato HH:MM).
  - Custo total estimado para o período.

## Como Facilita a Contabilidade

Ao final da execução, o script fornece um **relatório financeiro e de tempo** pronto. Em vez de abrir vídeo por vídeo para anotar a duração e calcular o valor, basta executar o script para ter:

1.  **Custo por Episódio**: O valor exato a ser cobrado por cada gravação.
2.  **Custo Total Mensal**: A soma de todos os custos, pronta para ser usada em faturas ou relatórios financeiros.
3.  **Registro de Tempo**: O tempo total gravado no mês, útil para análises de produtividade e planejamento.

Essa automação economiza horas de trabalho manual e garante que os valores cobrados sejam sempre precisos e baseados em dados reais da plataforma.

## Pré-requisitos

- Python 3.10 ou superior
- `pip` (gerenciador de pacotes do Python)

## Instalação e Configuração

1.  **Clone o Repositório**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
    cd GV-AUTOMATION
    ```

2.  **Crie e Ative um Ambiente Virtual**
    ```bash
    # Criar o ambiente
    python3 -m venv .venv

    # Ativar no Linux/macOS
    source .venv/bin/activate

    # Ativar no Windows (PowerShell)
    # .\.venv\Scripts\Activate.ps1
    ```

3.  **Instale as Dependências**
    O projeto usa a biblioteca `requests`. Instale-a a partir do arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Obtenha uma Chave da API do YouTube**
    - Siga o guia do Google para criar um projeto no Google Cloud Console e ativar a "YouTube Data API v3".
    - Crie uma "Chave de API" e copie o valor.

5.  **Configure a Chave de API como Variável de Ambiente**
    No seu terminal, execute o comando abaixo, substituindo `SUA_CHAVE_AQUI` pela chave que você copiou. **Este passo é crucial para a segurança.**
    ```bash
    export YOUTUBE_API_KEY='SUA_CHAVE_AQUI'
    ```
    *Nota: Esta variável só dura para a sessão atual do terminal. Se você fechar e abrir o terminal, precisará executar o comando `export` novamente.*

6.  **Ajuste o Arquivo de Configuração**
    Abra o arquivo `config.json` e edite os valores conforme sua necessidade:
    ```json
    {
      "valor_por_hora": 99999999,
      "ano_alvo": 999999999,
      "mes_alvo": 12
    }
    ```

## Como Usar

Com o ambiente virtual ativado e a variável de ambiente `YOUTUBE_API_KEY` definida, basta executar o script principal:

```bash
python processar_pesquisa.py
```

O script irá carregar as configurações, buscar os dados na API do YouTube e imprimir o relatório detalhado e o resumo final no seu terminal.

---

*Este projeto foi desenvolvido com o auxílio do Gemini Code Assist.*
