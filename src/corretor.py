from pathlib import Path
from typing import List

import google.generativeai as genai
from tqdm import tqdm

from config.config import BASE_DIR, OUTPUTS_DIR, GOOGLE_API_KEY, MODEL_NAME, MAX_TOKENS


class CorretorPerguntas:
    """Corretor/professor para perguntas de lógica, programação e cálculos.

    Lê perguntas em data/PERGUNTAS.md e gera respostas didáticas
    usando o modelo configurado na API do Google Gemini.
    """

    def __init__(self) -> None:
        self.base_dir: Path = BASE_DIR
        self.output_dir: Path = OUTPUTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": MAX_TOKENS,
            },
        )

    def _ler_arquivo(self, caminho: Path) -> str:
        if not caminho.exists():
            return ""
        return caminho.read_text(encoding="utf-8")

    def carregar_perguntas(self) -> List[str]:
        """Lê o arquivo PERGUNTAS.md e extrai as perguntas.

        Estratégia:
        - Ignora linhas que começam com '#'
        - Agrupa blocos de linhas não vazias (separados por linhas em branco)
          em uma única pergunta.

        Assim, você pode escrever enunciado + alternativas em um bloco contínuo,
        separado por linhas em branco entre uma questão e outra.

        Exemplo de PERGUNTAS.md:

        # Lógica
        Explique o que é um laço while e dê um exemplo em pseudocódigo.

        # Cálculo
        Como calcular a complexidade de tempo de um algoritmo de busca binária?
        """
        perguntas_path = self.base_dir / "data" / "PERGUNTAS.md"
        conteudo = self._ler_arquivo(perguntas_path)

        perguntas: List[str] = []
        buffer: List[str] = []

        for linha in conteudo.splitlines():
            linha_limpa = linha.rstrip("\n")

            # Ignora títulos em markdown
            if linha_limpa.strip().startswith("#"):
                continue

            # Linha em branco: fecha pergunta atual (se houver)
            if not linha_limpa.strip():
                if buffer:
                    perguntas.append("\n".join(buffer).strip())
                    buffer = []
                continue

            # Linha de conteúdo: acumula no buffer
            buffer.append(linha_limpa)

        # Última pergunta (se arquivo não terminar com linha em branco)
        if buffer:
            perguntas.append("\n".join(buffer).strip())

        return perguntas

    def responder_pergunta(self, pergunta: str) -> str:
        """Responde uma pergunta técnica de programação/lógica/cálculos.

        O modelo é instruído a agir como professor, explicar passo a passo
        e, quando fizer sentido, usar exemplos em Python ou pseudocódigo.
        """
        try:
            prompt = f"""
Você é um professor experiente de lógica de programação, algoritmos,
estruturas de dados, linguagens de programação e matemática básica
para computação (como aritmética, álgebra, análise de complexidade).

Responda à pergunta abaixo de forma:
- clara e didática
- passo a passo quando envolver raciocínio lógico ou contas
- com exemplos em pseudocódigo ou Python quando isso ajudar

Se a pergunta for ambígua, explique as possíveis interpretações.

Pergunta do aluno:
{pergunta}
"""

            response = self.model.generate_content(prompt, stream=False)
            return response.text
        except Exception as e:
            return f"Erro ao responder pergunta com Gemini: {str(e)}"

    def gerar_respostas(self) -> Path:
        """Lê PERGUNTAS.md, responde tudo e salva em RESPOSTAS_PERGUNTAS.md."""
        print("❓ Carregando perguntas...")
        perguntas = self.carregar_perguntas()

        if not perguntas:
            print("⚠️ Nenhuma pergunta encontrada em data/PERGUNTAS.md")
            return self.output_dir / "RESPOSTAS_PERGUNTAS.md"

        respostas_markdown: List[str] = []
        respostas_markdown.append("# ❓ Respostas às Perguntas de Programação e Lógica\n")
        respostas_markdown.append(
            "Respostas geradas automaticamente pelo corretor de programação, "
            "focadas em lógica, algoritmos, código e cálculos relacionados.\n"
        )

        for i, pergunta in enumerate(tqdm(perguntas, desc="Respondendo perguntas"), start=1):
            respostas_markdown.append(f"\n---\n\n## Pergunta {i}\n")
            respostas_markdown.append(pergunta + "\n")

            resposta = self.responder_pergunta(pergunta)

            respostas_markdown.append("\n### Resposta\n")
            respostas_markdown.append(resposta + "\n")

        saida = self.output_dir / "RESPOSTAS_PERGUNTAS.md"
        saida.write_text("\n".join(respostas_markdown), encoding="utf-8")

        print(f"\n✅ Respostas geradas com sucesso em: {saida}")
        return saida


if __name__ == "__main__":
    corretor = CorretorPerguntas()
    corretor.gerar_respostas()
