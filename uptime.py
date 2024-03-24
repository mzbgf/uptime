# please run with `GITHUB_PAT=$GITHUB_PAT python3 uptime.py`

import requests, json, os

# 替换为你的GitHub个人访问令牌  # 作为输入参数
GITHUB_TOKEN = os.environ.get('GITHUB_PAT')

if not GITHUB_TOKEN:
    print('env GITHUB_PAT no set!!!')
    print('please run with `GITHUB_PAT=$GITHUB_PAT python3 uptime.py`')
    exit(1)

OWNER = "mzbgf"  # 替换为你的GitHub用户名
REPO = "uptime"   # 替换为你的仓库名

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/public-key"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}
response = requests.get(url, headers=headers)
if response.status_code == 404:
    print("Not Found")
    print(response.json().get("message"))
    print(response.json().get("documentation_url"))
    exit(1)
else:
    # 处理响应，例如打印JSON内容
    key_id = response.json()['key_id']
    key = response.json()['key']

from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

secret_name = "WEBAPPIO"
secret_value = os.environ.get('EXPOSE_WEBSITE_HOST')

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{secret_name}"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json"
}

data = {
    "encrypted_value": encrypt(key, secret_value),
    "key_id": key_id
}

response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 204:
    print(response.status_code)
else:
    print(response.text)
    exit(1)
