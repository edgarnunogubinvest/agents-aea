``` bash
aea create my_genesis_aea
cd my_genesis_aea
aea add connection fetchai/p2p_libp2p:0.12.0
aea config set agent.default_connection fetchai/p2p_libp2p:0.12.0
aea run --connections fetchai/p2p_libp2p:0.12.0
```
``` bash
aea create my_other_aea
cd my_other_aea
aea add connection fetchai/p2p_libp2p:0.12.0
aea config set agent.default_connection fetchai/p2p_libp2p:0.12.0
```
``` bash
aea run --connections fetchai/p2p_libp2p:0.12.0
```
  ``` bash
  svn export https://github.com/fetchai/agents-aea.git/trunk/packages/fetchai/connections/p2p_libp2p
  cd p2p_libp2p
  go build
  chmod +x libp2p_node
  ```
  ``` bash
  docker build -t acn_node_standalone -f scripts/acn/Dockerfile .
  ```
  ``` bash
  python3 run_acn_node_standalone.py libp2p_node --config-from-env
  ```
  ``` bash
  python3 run_acn_node_standalone.py libp2p_node --config-from-file <env-file-path>
  ```
  ``` bash
  docker run -v <acn_config_file>:/acn/acn_config -it acn_node_standalone --config-from-file /acn/acn_config
  ```
  ``` bash
  python3 run_acn_node_standalone.py libp2p_node --key-file <node_private_key.txt> \
    --uri <AEA_P2P_URI> --uri-external <AEA_P2P_URI_PUBLIC>  \
    --uri-delegate <AEA_P2P_DELEGATE_URI> \
    --entry-peers-maddrs <AEA_P2P_ENTRY_URI_1> <AEA_P2P_ENTRY_URI_2> ...
  ```
  ``` bash
  docker run -v <node_private_key.txt>:/acn/key.txt -it acn_node_standalone --key-file /acn/key.txt \
    --uri <AEA_P2P_URI> --uri-external <AEA_P2P_URI_PUBLIC>  \
    --uri-delegate <AEA_P2P_DELEGATE_URI> \
    --entry-peers-maddrs <AEA_P2P_ENTRY_URI_1> <AEA_P2P_ENTRY_URI_2> ...
  ```
``` yaml
config:
  delegate_uri: 127.0.0.1:11001
  entry_peers: MULTI_ADDRESSES
  local_uri: 127.0.0.1:9001
  log_file: libp2p_node.log
  public_uri: 127.0.0.1:9001
```
``` yaml
default_routing:
  ? "fetchai/oef_search:0.10.0"
  : "fetchai/oef:0.13.0"
```
``` yaml
config:
  delegate_uri: 127.0.0.1:11001
  entry_peers: MULTI_ADDRESSES
  local_uri: 127.0.0.1:9001
  log_file: libp2p_node.log
  public_uri: 127.0.0.1:9001
```
```yaml
/dns4/agents-p2p-dht.sandbox.fetch-ai.com/tcp/9000/p2p/16Uiu2HAkw1ypeQYQbRFV5hKUxGRHocwU5ohmVmCnyJNg36tnPFdx
/dns4/agents-p2p-dht.sandbox.fetch-ai.com/tcp/9001/p2p/16Uiu2HAmVWnopQAqq4pniYLw44VRvYxBUoRHqjz1Hh2SoCyjbyRW
```
``` yaml
config:
  delegate_uri: 127.0.0.1:11001
  entry_peers: [/dns4/agents-p2p-dht.sandbox.fetch-ai.com/tcp/9000/p2p/16Uiu2HAkw1ypeQYQbRFV5hKUxGRHocwU5ohmVmCnyJNg36tnPFdx,/dns4/agents-p2p-dht.sandbox.fetch-ai.com/tcp/9001/p2p/16Uiu2HAmVWnopQAqq4pniYLw44VRvYxBUoRHqjz1Hh2SoCyjbyRW]
  local_uri: 127.0.0.1:9001
  log_file: libp2p_node.log
  public_uri: 127.0.0.1:9001
```