import json
import sys


def generate_config(input_json):
    # 基础端口
    base_port = 37800

    # 提取 outbounds
    outbounds = input_json.get("outbounds", [])

    outbounds = [
        outbound
        for outbound in outbounds
        if outbound["tag"] != "direct"
        and not (
            "到期时间" in outbound["tag"]
            or "当前流量" in outbound["tag"]
            or "剩余流量" in outbound["tag"]
            or "距离下次重置剩余" in outbound["tag"]
            or "套餐到期" in outbound["tag"]
        )
    ]

    if not outbounds:
        raise ValueError("输入 JSON 中没有 outbounds 数组")

    # 生成 inbounds 和 route rules
    inbounds = []
    route_rules = []

    for i, outbound in enumerate(outbounds):
        tag = outbound.get("tag", f"outbound-{i}")
        # 跳过多余的 direct
        if tag == "direct":
            break
        port = base_port + i

        # 创建对应的 inbound
        inbound = {
            "type": "socks",
            "tag": tag,
            "listen": "127.0.0.1",
            "listen_port": port,
        }
        inbounds.append(inbound)

        # 创建路由规则：该 inbound 流量走对应的 outbound
        rule = {"inbound": tag, "outbound": tag}
        route_rules.append(rule)

    # 构造新的 outbounds：原 outbound + direct
    new_outbounds = outbounds + [{"type": "direct", "tag": "direct"}]

    # 最终输出结构
    output_config = {
        "log": {"level": "info"},
        "inbounds": inbounds,
        "outbounds": new_outbounds,
        "route": {"rules": route_rules, "auto_detect_interface": True},
    }

    return output_config


if __name__ == "__main__":
    # 从标准输入读取 JSON（支持管道或直接粘贴）
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = generate_config(input_data)
        # 美化输出 JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"生成配置失败: {e}", file=sys.stderr)
        sys.exit(1)
