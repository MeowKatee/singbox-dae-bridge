import sys
import json
from urllib.parse import quote

if __name__ == "__main__":
    # 从标准输入读取 JSON（支持管道或直接粘贴）
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)

    for inbound in input_data["inbounds"]:
        inbound: dict[str, str | int]
        name = inbound["tag"]
        port: int = inbound["listen_port"]
        host = f"127.0.0.1:{port}"

        print(f"socks5://{host}#{quote(name)}")
