import os
from dotenv import load_dotenv
load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "")
GAODE_API_KEY = os.getenv("GAODE_API_KEY", "")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))  # 增加到30秒
