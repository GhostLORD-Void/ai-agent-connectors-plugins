"""MCP JSON-RPC stdio server with tools, resources, and prompts."""
import json,sys
from connectors import TOOLS,call_tool,ConnectorError
from discovery import discover_connectors
RESOURCES=[
{"uri":"connectors://catalog","name":"Connector catalog","description":"Connector metadata, tools, categories and required environment variables.","mimeType":"application/json"},
{"uri":"connectors://setup","name":"Setup guide","description":"How to configure and run the MCP server.","mimeType":"text/markdown"}]
PROMPTS=[
{"name":"plan_connector","description":"Plan a safe implementation of a new service connector.","arguments":[{"name":"service","description":"Service or API to connect","required":True},{"name":"use_case","description":"What the agent should do","required":True}]},
{"name":"review_tool_call","description":"Review a proposed connector action for permissions and side effects.","arguments":[{"name":"tool_name","description":"MCP tool name","required":True},{"name":"arguments","description":"Proposed JSON arguments","required":True}]}]
SETUP="# MCP connector server setup\n\nRun python src/mcp_server.py with credentials in the process environment. Write tools make external changes; review arguments before use. Never commit tokens or webhook URLs. See docs/CONNECTORS.md.\n"
def handle(m):
    method=m.get("method"); p=m.get("params") or {}; i=m.get("id")
    if method=="notifications/initialized": return None
    if method=="initialize": return {"jsonrpc":"2.0","id":i,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":False},"resources":{"subscribe":False,"listChanged":False},"prompts":{"listChanged":False}},"serverInfo":{"name":"ai-agent-connectors-plugins","version":"0.2.0"}}}
    if method=="ping": return {"jsonrpc":"2.0","id":i,"result":{}}
    if method=="tools/list": return {"jsonrpc":"2.0","id":i,"result":{"tools":TOOLS}}
    if method=="resources/list": return {"jsonrpc":"2.0","id":i,"result":{"resources":RESOURCES}}
    if method=="resources/read":
        uri=p.get("uri")
        if uri=="connectors://catalog": value=json.dumps(discover_connectors(),ensure_ascii=False,indent=2); mime="application/json"
        elif uri=="connectors://setup": value=SETUP; mime="text/markdown"
        else: return {"jsonrpc":"2.0","id":i,"error":{"code":-32002,"message":"Resource not found"}}
        return {"jsonrpc":"2.0","id":i,"result":{"contents":[{"uri":uri,"mimeType":mime,"text":value}]}}
    if method=="prompts/list": return {"jsonrpc":"2.0","id":i,"result":{"prompts":PROMPTS}}
    if method=="prompts/get":
        name=p.get("name"); a=p.get("arguments") or {}
        if name=="plan_connector":
            msg=f"Design a least-privilege connector for {a.get('service','the service')}. Use case: {a.get('use_case','the requested workflow')}. Document auth scopes, input schema, timeouts, retries, tests, data handling and destructive side effects. Do not invent credentials."
        elif name=="review_tool_call":
            msg=f"Review this proposed tool call before execution. Tool: {a.get('tool_name')}. Arguments: {a.get('arguments')}. Identify permissions, sensitive data and external side effects. Do not execute it."
        else: return {"jsonrpc":"2.0","id":i,"error":{"code":-32602,"message":"Unknown prompt"}}
        return {"jsonrpc":"2.0","id":i,"result":{"description":"Connector engineering prompt","messages":[{"role":"user","content":{"type":"text","text":msg}}]}}
    if method=="tools/call":
        try:
            out=call_tool(p.get("name"),p.get("arguments") or {})
            return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":json.dumps(out,ensure_ascii=False)}],"isError":False}}
        except (ConnectorError,TypeError,ValueError) as e: return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":str(e)}],"isError":True}}
        except Exception as e: return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":f"Connector failed: {type(e).__name__}: {e}"}],"isError":True}}
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
