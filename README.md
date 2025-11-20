# Análise de Dados - Desafio Méliuz

Este repositório contém a análise de dados do case técnico da Méliuz, incluindo processamento de dados, geração de relatórios e visualizações.

## 📊 Visão Geral

O projeto realiza uma análise detalhada dos dados de transações da Méliuz, fornecendo insights estratégicos através de métricas, gráficos e relatórios automatizados.

## 🚀 Funcionalidades Principais

- **Análise de Métricas Diárias**: Vendas, faturamento e conversões
- **Análise por Parceiro**: Desempenho e margens por parceiro
- **Segmentação de Usuários**: Análise de comportamento de novos vs. antigos usuários
- **Geração de Relatórios**: Relatórios em PDF e Word com análises detalhadas
- **Visualizações Interativas**: Gráficos e dashboards para análise exploratória

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes do Python)
- Ambiente virtual (recomendado)

## 🛠️ Instalação

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/desafio-meliuz.git
   cd desafio-meliuz
   ```

2. **Criar e ativar ambiente virtual**
   ```bash
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 🚦 Executando a Análise

1. **Executar a análise principal**
   ```bash
   python run.py
   ```

2. **Gerar relatórios**
   ```bash
   python generate_reports.py
   ```

3. **Visualizar resultados**
   - Gráficos: `outputs/plots/`
   - Relatórios: `outputs/reports/`
   - Análises: `analise_ia/outputs/`

## 📁 Estrutura do Projeto

```
.
├── analise_ia/           # Análises avançadas e relatórios
├── meliuz_analysis/      # Código-fonte principal
│   ├── data/            # Dados de entrada
│   ├── outputs/         # Saídas geradas
│   ├── plots/           # Código de visualizações
│   └── utils/           # Utilitários e funções auxiliares
├── outputs/             # Arquivos de saída gerados
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

## 📈 Relatório de Análise

O relatório completo de diagnóstico e plano de ação está disponível em [relatorio_diagnostico_plano_de_acao.pdf](relatorio_diagnostico_plano_de_acao.pdf).

## 🛠️ Solução de Problemas Comuns

### Erro: "python: can't open file 'run.py'"
**Causa:** Pasta de trabalho incorreta  
**Solução:** Navegue até a pasta raiz do projeto:
```bash
cd /caminho/para/desafio-meliuz
```

### Erro: "Arquivo de credenciais do Google não encontrado"
**Causa:** Tentativa de exportar para Google Sheets sem credenciais  
**Solução:** Este erro pode ser ignorado - os arquivos locais são gerados normalmente.

### Se os gráficos não forem gerados:
1. Verifique se o arquivo de dados existe:
   ```bash
   ls meliuz_analysis/data/base_de_dados_meliuz_case.xlsx
   ```
2. Verifique as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙋‍♂️ Suporte

Para suporte, entre em contato ou abra uma issue no repositório.
