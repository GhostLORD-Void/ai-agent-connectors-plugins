"""Optional CrewAI adapter. Install crewai to use."""
def get_crewai_tools():
    try: from crewai.tools import BaseTool
    except ImportError as exc: raise RuntimeError("Install optional dependency: pip install crewai") from exc
    from connectors import TOOLS,call_tool
    result=[]
    for spec in TOOLS:
        tool_name=spec["name"]; tool_desc=spec["description"]
        class ConnectorTool(BaseTool):
            name: str=tool_name
            description: str=tool_desc
            def _run(self,**kwargs): return call_tool(self.name,kwargs)
        result.append(ConnectorTool())
    return result
