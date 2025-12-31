# singbox-dae-bridge

## Why?

- You want rule-set based routing
- You don't like manual migration of routing rules
- You want Shadowsocks 2022 EIH, which is not well implemented by most providers, and will cause performance lag for shadowsocks-rust and shadowsocks-go, and not implemented by dae-next yet.

## NOTE

Remember to have `pname(sing-box) -> must_direct`.

## How to use

```bash
python3 convert.py < your_singbox_conf.json > config.json

# for dae
python3 gen_dae_nodes.py < config.json | sudo tee --append /etc/dae/config.dae
```

