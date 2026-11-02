"""Optional LangChain adapter. Install langchain-core to use."""
def get_langchain_tools():
    try: from langchain_core.tools import StructuredTool
    except ImportError as exc: raise RuntimeError("Install optional dependency: pip install langchain-core") from exc
    from connectors import TOOLS,call_tool
    result=[]
    for spec in TOOLS:
        name=spec["name"]
        def invoke(_name=name,**kwargs): return call_tool(_name,kwargs)
        result.append(StructuredTool.from_function(func=invoke,name=name,description=spec["description"]))
    return result
