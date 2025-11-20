# /home/bfelipef/Documentos/desafio/Méliuz/analise_ia/src/analisador_grafico.py
import os
from pathlib import Path
from typing import Dict, List, Optional
# import google.generativeai as genai
from tqdm import tqdm
from PIL import Image
import time
import google.generativeai as genai
from config.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
models = genai.list_models()
for model in models:
    if 'vision' in model.name.lower() or 'image' in model.name.lower():
        print(f"Modelo de visão encontrado: {model.name}")

# Importa configurações
from config.config import (
    BASE_DIR, OUTPUTS_DIR, 
    GOOGLE_API_KEY, MODEL_NAME, MAX_TOKENS
)

class AnalisadorGraficos:
    def __init__(self):
        self.output_dir = OUTPUTS_DIR
        self.output_dir.mkdir(exist_ok=True, parents=True)
        # Usando um modelo disponível que suporte visão
        self.modelo_visao = 'gemini-2.5-pro'  # Atualizado para um modelo disponível
        
    def carregar_graficos(self) -> Dict[str, str]:
        """Carrega os arquivos de gráficos para análise"""
        graficos_dir = BASE_DIR.parent / 'test_outputs'
        graficos = {}
        
        # Lista de gráficos esperados
        graficos_esperados = [
            'daily_metrics_improved.png',
            'partner_metrics_improved.png',
            'user_segmentation_improved.png',
            'cashback_impact_improved.png',
            'seasonality_improved.png'
        ]
        
        for grafico in graficos_esperados:
            caminho = graficos_dir / grafico
            if caminho.exists():
                graficos[grafico] = str(caminho.absolute())
                
        return graficos
    
    def analisar_imagem(self, caminho_imagem: str, contexto: str = "") -> str:
        """Analisa uma imagem usando o modelo de visão computacional"""
        try:
            # Carrega a imagem
            img = Image.open(caminho_imagem)
            
            # Configura o modelo
            model = genai.GenerativeModel(self.modelo_visao)
            
            # Prepara o prompt
            prompt = f"""
            Você é um especialista em análise de dados e visualização. 
            Por favor, analise este gráfico detalhadamente e forneça:
            
            1. Descrição detalhada do que o gráfico está mostrando
            2. Principais tendências e padrões observados
            3. Insights acionáveis baseados nos dados
            4. Possíveis preocupações ou oportunidades
            
            {contexto}
            """
            
            # Converte a imagem para base64
            import base64
            from io import BytesIO
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Gera a análise
            response = model.generate_content([
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": img_str}}
            ])
            
            return response.text
            
        except Exception as e:
            return f"Erro ao analisar a imagem {caminho_imagem}: {str(e)}"
    
    def gerar_relatorio_graficos(self):
        """Gera um relatório com a análise de todos os gráficos"""
        print("📊 Iniciando análise dos gráficos...")
        
        # Carrega os gráficos
        graficos = self.carregar_graficos()
        
        if not graficos:
            print("❌ Nenhum gráfico encontrado para análise.")
            return
        
        # Mapeamento de descrições para cada tipo de gráfico
        descricoes = {
            'daily_metrics_improved.png': 'Painel de Métricas Diárias mostrando a evolução temporal das principais métricas de negócio',
            'partner_metrics_improved.png': 'Análise de Desempenho dos Parceiros com ranking e métricas-chave',
            'user_segmentation_improved.png': 'Segmentação de Usuários mostrando diferentes perfis de clientes',
            'cashback_impact_improved.png': 'Análise do Impacto do Cashback nas Vendas',
            'seasonality_improved.png': 'Análise de Sazonalidade e Padrões Temporais'
        }
        
        # Carrega o contexto do README se disponível
        contexto_geral = ""
        readme_path = BASE_DIR.parent / 'test_outputs' / 'README_GRAFICOS.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                contexto_geral = f"Contexto adicional sobre os gráficos:\n{f.read()}"
        
        # Inicia o relatório
        relatorio = ["# 📊 Análise Detalhada dos Gráficos\n"]
        relatorio.append("Análise gerada automaticamente usando IA para extrair insights dos gráficos.\n")
        
        # Processa cada gráfico
        for nome_arquivo, caminho in tqdm(graficos.items(), desc="Analisando gráficos"):
            try:
                descricao = descricoes.get(nome_arquivo, f'Gráfico: {nome_arquivo}')
                relatorio.append(f"## 📊 {descricao}\n")
                relatorio.append(f"![{nome_arquivo}]({caminho})\n")
                
                # Adiciona contexto específico do gráfico se disponível
                contexto = f"Contexto específico para {nome_arquivo}:\n{descricao}\n\n{contexto_geral}"
                
                # Realiza a análise
                relatorio.append("### Análise Detalhada\n")
                analise = self.analisar_imagem(caminho, contexto)
                relatorio.append(analise)
                
                # Adiciona separador
                relatorio.append("\n" + "-"*80 + "\n")
                
                # Pequeno delay para evitar sobrecarga da API
                time.sleep(2)
                
            except Exception as e:
                relatorio.append(f"⚠️ Erro ao processar o gráfico {nome_arquivo}: {str(e)}\n")
        
        # Salva o relatório
        caminho_relatorio = self.output_dir / 'analise_graficos.md'
        with open(caminho_relatorio, 'w', encoding='utf-8') as f:
            f.write('\n'.join(relatorio))
        
        print(f"\n✅ Análise de gráficos concluída! Relatório salvo em: {caminho_relatorio}")

if __name__ == "__main__":
    # Configura a API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Cria e executa o analisador
    analisador = AnalisadorGraficos()
    analisador.gerar_relatorio_graficos()