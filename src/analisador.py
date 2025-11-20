# /home/bfelipef/Documentos/desafio/Méliuz/analise_ia/src/analisador.py
import os
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from tqdm import tqdm

# Importa configurações
from config.config import (
    BASE_DIR, DATA_DIR, OUTPUTS_DIR, 
    GOOGLE_API_KEY, MODEL_NAME, CHUNK_SIZE, MAX_TOKENS
)

# Configura a API
genai.configure(api_key=GOOGLE_API_KEY)

class AnalisadorRelatorio:
    def __init__(self):
        self.output_dir = OUTPUTS_DIR
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def listar_modelos_disponiveis(self):
        """Lista os modelos disponíveis na API do Google"""
        try:
            models = genai.list_models()
            print("Modelos disponíveis:")
            for model in models:
                print(f"- {model.name}")
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
        
    def carregar_arquivos(self) -> Dict[str, str]:
        """Carrega todos os arquivos relevantes para análise"""
        arquivos = {
            'relatorio': self._ler_arquivo(BASE_DIR.parent / 'test_outputs' / 'relatorio.md'),
            'analise_avancada': self._ler_arquivo(BASE_DIR.parent / 'outputs' / 'analise_avancada.json'),
            'analise_graficos': self._ler_arquivo(BASE_DIR.parent / 'outputs' / 'analise_graficos.json'),
            'resumo_executivo': self._ler_arquivo(BASE_DIR.parent / 'RESUMO_EXECUTIVO.md'),
            'readme_graficos': self._ler_arquivo(BASE_DIR.parent / 'test_outputs' / 'README_GRAFICOS.md')
        }
        return {k: v for k, v in arquivos.items() if v}
    
    def _ler_arquivo(self, caminho: Path) -> Optional[str]:
        """Lê um arquivo e retorna seu conteúdo como string"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Erro ao ler {caminho}: {e}")
            return None

    def dividir_em_partes(self, texto: str, tamanho: int = CHUNK_SIZE) -> List[str]:
        """Divide o texto em partes menores para análise"""
        palavras = texto.split()
        partes = []
        parte_atual = []
        contador = 0
        
        for palavra in palavras:
            parte_atual.append(palavra)
            contador += len(palavra) + 1
            if contador >= tamanho:
                partes.append(' '.join(parte_atual))
                parte_atual = []
                contador = 0
        
        if parte_atual:
            partes.append(' '.join(parte_atual))
            
        return partes

    # Substitua o método analisar_com_ia por:
    def analisar_com_ia(self, prompt: str, contexto: str = "") -> str:
        """Envia uma solicitação para a API do Google Gemini"""
        try:
            model = genai.GenerativeModel(
                MODEL_NAME,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": MAX_TOKENS,
                }
            )
            
            response = model.generate_content(
                f"{contexto}\n\n{prompt}",
                stream=False
            )
            return response.text
        except Exception as e:
            return f"Erro na análise com Gemini: {str(e)}"

    def gerar_analise_completa(self):
        """Gera uma análise completa com base em todos os arquivos"""
        print("📂 Carregando arquivos...")
        arquivos = self.carregar_arquivos()
        
        if not arquivos:
            print("❌ Nenhum arquivo encontrado para análise.")
            return
        
        print("📊 Iniciando análise com IA...")
        relatorio_final = ["# 📊 Análise Completa - Projeto Méliuz\n"]
        
        # Adiciona sumário executivo
        if 'resumo_executivo' in arquivos:
            relatorio_final.append("## 📌 Sumário Executivo\n")
            relatorio_final.append(arquivos['resumo_executivo'].split("## ")[1])
        
        # Análise do relatório principal
        if 'relatorio' in arquivos:
            relatorio_final.append("\n## 🔍 Análise Detalhada do Relatório\n")
            partes = self.dividir_em_partes(arquivos['relatorio'])
            
            for i, parte in enumerate(tqdm(partes, desc="Analisando relatório")):
                prompt = f"Analise a seguinte seção do relatório e forneça insights detalhados, exemplos práticos e recomendações acionáveis:\n\n{parte}"
                analise = self.analisar_com_ia(prompt)
                relatorio_final.append(analise)
                time.sleep(1)  # Evita atingir limites de taxa
        
        # Análise dos gráficos
        if 'analise_graficos' in arquivos:
            try:
                graficos = json.loads(arquivos['analise_graficos'])
                relatorio_final.append("\n## 📈 Análise dos Gráficos\n")
                
                for nome, dados in graficos['graficos_analisados'].items():
                    if dados['status'] == 'encontrado':
                        relatorio_final.append(f"### 📊 {dados.get('tipo', nome)}\n")
                        relatorio_final.append(f"**Arquivo:** `{dados.get('arquivo', 'N/A')}`\n")
                        
                        if 'insights' in dados:
                            relatorio_final.append("#### Principais Insights\n")
                            for insight in dados['insights']:
                                relatorio_final.append(f"- {insight}")
                            
                            # Adiciona análise adicional da IA
                            prompt = f"Com base nestes insights, quais ações práticas você recomendaria para melhorar os resultados?\n\n{json.dumps(dados['insights'], indent=2)}"
                            recomendacoes = self.analisar_com_ia(prompt)
                            relatorio_final.append("\n#### Recomendações Estratégicas\n")
                            relatorio_final.append(recomendacoes)
                            
                        relatorio_final.append("\n" + "-"*50 + "\n")
            except Exception as e:
                relatorio_final.append(f"\n⚠️ Erro ao analisar gráficos: {str(e)}\n")
        
        # Salva o relatório final
        caminho_relatorio = self.output_dir / 'analise_completa.md'
        with open(caminho_relatorio, 'w', encoding='utf-8') as f:
            f.write('\n'.join(relatorio_final))
        
        print(f"\n✅ Análise concluída com sucesso! Relatório salvo em: {caminho_relatorio}")

if __name__ == "__main__":
    analisador = AnalisadorRelatorio()
    # Primeiro lista os modelos disponíveis
    analisador.listar_modelos_disponiveis()
    # Depois executa a análise
    analisador.gerar_analise_completa()