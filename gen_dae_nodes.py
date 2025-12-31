import sys
import json

if __name__ == "__main__":
    # 从标准输入读取 JSON（支持管道或直接粘贴）
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)

    print("node {")
    for inbound in input_data["inbounds"]:
        inbound: dict[str, str | int]
        name = inbound["tag"].replace(" ", "-")
        port: int = inbound["listen_port"]
        print(f"    {name}: 'socks5://127.0.0.1:{port}'")
    print("}")
