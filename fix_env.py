import os

content = """# Gemini API Key
GEMINI_API_KEY=AIzaSyDb9aryszWzzm3k_bRYuA6lp3LqRzjZ0LU

# Project Info
PROJECT_ID=projects/910276685596
PROJECT_NUMBER=910276685596

# File Upload Settings
MAX_FILE_SIZE_MB=50

# App Settings
APP_TITLE=NaraStore 제안서 분석 서비스
DEBUG_MODE=False
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)

print(".env file recreated with UTF-8 encoding.")
