"""Minimal MCP JSON-RPC stdio server; no third-party dependencies."""
import json,sys
from connectors import TOOLS,call_tool,ConnectorError
def handle(m):
    method=m.get("method"); p=m.get("params") or {}; i=m.get("id")
    if method=="notifications/initialized": return None
    if method=="initialize":
        return {"jsonrpc":"2.0","id":i,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":"ai-agent-connectors-plugins","version":"0.1.0"}}}
    if method=="ping": return {"jsonrpc":"2.0","id":i,"result":{}}
    if method=="tools/list": return {"jsonrpc":"2.0","id":i,"result":{"tools":TOOLS}}
    if method=="tools/call":
        try:
            out=call_tool(p.get("name"),p.get("arguments") or {})
            return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":json.dumps(out,ensure_ascii=False)}],"isError":False}}
        except (ConnectorError,TypeError,ValueError) as e:
            return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":str(e)}],"isError":True}}
        except Exception as e:
            return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":f"Connector failed: {type(e).__name__}: {e}"}],"isError":True}}
    if i is not None: return {"jsonrpc":"2.0","id":i,"error":{"code":-32601,"message":"Method not found: "+str(method)}}
    return None
def main():
    for line in sys.stdin:
        try:
            msg=json.loads(line)
            if isinstance(msg,dict):
                response=handle(msg)
                if response is not None: sys.stdout.write(json.dumps(response,separators=(",",":"))+"\n"); sys.stdout.flush()
        except json.JSONDecodeError:
            sys.stdout.write('{"jsonrpc":"2.0","id":null,"error":{"code":-32700,"message":"Parse error"}}\n'); sys.stdout.flush()
if __name__=="__main__": main()
