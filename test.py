from docmakerai.generator  import generate
from config.settings import groq_api_key , git_token

resp = generate("https://github.com/SyntaxByte-Solution/tap-mini-app.git",git_token=git_token,ai_token=groq_api_key)
print(resp)