# /home/bfelipef/Documentos/desafio/Méliuz/analise_ia/config/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações de diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
OUTPUTS_DIR = BASE_DIR / 'outputs'
SRC_DIR = BASE_DIR / 'src'

# Configurações da API Google Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = "gemini-2.5-pro"  # Modelo atualizado para uma versão disponível

# Configurações de análise
CHUNK_SIZE = 3000
MAX_TOKENS = 4000