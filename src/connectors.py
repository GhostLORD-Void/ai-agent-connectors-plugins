"""Ten practical API connectors. Python standard library only."""
import json, os, urllib.error, urllib.parse, urllib.request, base64
TIMEOUT=30
class ConnectorError(RuntimeError): pass
def request_json(method,url,*,headers=None,body=None):
    data=None if body is None else json.dumps(body).encode()
    h={"Accept":"application/json","User-Agent":"ai-agent-connectors-plugins/0.1"}
    if data is not None: h["Content-Type"]="application/json"
    h.update(headers or {})
    try:
        with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=h,method=method),timeout=TIMEOUT) as r:
            raw=r.read()
            return json.loads(raw.decode()) if raw else {}
    except urllib.error.HTTPError as e:
        detail=e.read(2048).decode("utf-8","replace")
        raise ConnectorError(f"HTTP {e.code} from {urllib.parse.urlsplit(url).netloc}: {detail}") from None
    except (urllib.error.URLError,TimeoutError) as e: raise ConnectorError(f"Network error: {e}") from None
def need(k):
    v=os.environ.get(k)
    if not v: raise ConnectorError(f"Missing required environment variable: {k}")
    return v
def github_list_repos(per_page=20):
    return request_json("GET","https://api.github.com/user/repos?"+urllib.parse.urlencode({"per_page":min(max(int(per_page),1),100),"sort":"updated"}),headers={"Authorization":"Bearer "+need("GITHUB_TOKEN"),"X-GitHub-Api-Version":"2022-11-28"})
def github_create_issue(owner,repo,title,body=""):
    return request_json("POST",f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/issues",headers={"Authorization":"Bearer "+need("GITHUB_TOKEN"),"X-GitHub-Api-Version":"2022-11-28"},body={"title":title,"body":body})
def gitlab_list_projects(per_page=20):
    return request_json("GET","https://gitlab.com/api/v4/projects?"+urllib.parse.urlencode({"membership":"true","per_page":min(max(int(per_page),1),100),"order_by":"last_activity_at"}),headers={"PRIVATE-TOKEN":need("GITLAB_TOKEN")})
def slack_send_message(channel,text):
    return request_json("POST","https://slack.com/api/chat.postMessage",headers={"Authorization":"Bearer "+need("SLACK_BOT_TOKEN")},body={"channel":channel,"text":text})
def discord_send_webhook(webhook_url,content):
    if not webhook_url.startswith("https://discord.com/api/webhooks/"): raise ConnectorError("Only Discord HTTPS webhook URLs are accepted")
    return request_json("POST",webhook_url,body={"content":content})
def notion_search(query,page_size=20):
    return request_json("POST","https://api.notion.com/v1/search",headers={"Authorization":"Bearer "+need("NOTION_TOKEN"),"Notion-Version":"2022-06-28"},body={"query":query,"page_size":min(max(int(page_size),1),100)})
def jira_create_issue(project_key,summary,description,issue_type="Task"):
    site=need("JIRA_BASE_URL").rstrip("/")
    auth=base64.b64encode((need("JIRA_EMAIL")+":"+need("JIRA_API_TOKEN")).encode()).decode()
    desc={"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":description}]}]}
    return request_json("POST",site+"/rest/api/3/issue",headers={"Authorization":"Basic "+auth},body={"fields":{"project":{"key":project_key},"summary":summary,"description":desc,"issuetype":{"name":issue_type}}})
def linear_create_issue(team_id,title,description=""):
    q="mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier url title } } }"
    return request_json("POST","https://api.linear.app/graphql",headers={"Authorization":need("LINEAR_API_KEY")},body={"query":q,"variables":{"input":{"teamId":team_id,"title":title,"description":description}}})
def openai_chat(prompt,model="gpt-4o-mini"):
    return request_json("POST","https://api.openai.com/v1/chat/completions",headers={"Authorization":"Bearer "+need("OPENAI_API_KEY")},body={"model":model,"messages":[{"role":"user","content":prompt}]})
def gemini_generate(prompt,model="gemini-2.0-flash"):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model)}:generateContent?key={urllib.parse.quote(need('GEMINI_API_KEY'))}"
    return request_json("POST",url,body={"contents":[{"parts":[{"text":prompt}]}]})
def tavily_search(query,max_results=5):
    return request_json("POST","https://api.tavily.com/search",body={"api_key":need("TAVILY_API_KEY"),"query":query,"max_results":min(max(int(max_results),1),20)})
def schema(name,desc,props,required=()):
    return {"name":name,"description":desc,"inputSchema":{"type":"object","properties":props,"required":list(required)}}
S={"type":"string"}; I={"type":"integer","minimum":1}
TOOLS=[
schema("github_list_repos","List repositories accessible to the configured GitHub token.",{"per_page":I}),
schema("github_create_issue","Create an issue in a GitHub repository; external write.",{"owner":S,"repo":S,"title":S,"body":S},("owner","repo","title")),
schema("gitlab_list_projects","List projects accessible to the configured GitLab token.",{"per_page":I}),
schema("slack_send_message","Send a message to a Slack channel; external write.",{"channel":S,"text":S},("channel","text")),
schema("discord_send_webhook","Send a Discord webhook message; external write.",{"webhook_url":S,"content":S},("webhook_url","content")),
schema("notion_search","Search Notion content shared with this integration.",{"query":S,"page_size":I},("query",)),
schema("jira_create_issue","Create a Jira Cloud issue; external write.",{"project_key":S,"summary":S,"description":S,"issue_type":S},("project_key","summary","description")),
schema("linear_create_issue","Create a Linear issue; external write.",{"team_id":S,"title":S,"description":S},("team_id","title")),
schema("openai_chat","Generate a response with OpenAI Chat Completions.",{"prompt":S,"model":S},("prompt",)),
schema("gemini_generate","Generate content with Google Gemini.",{"prompt":S,"model":S},("prompt",)),
schema("tavily_search","Search the web using Tavily.",{"query":S,"max_results":I},("query",))]
DISPATCH={f.__name__:f for f in [github_list_repos,github_create_issue,gitlab_list_projects,slack_send_message,discord_send_webhook,notion_search,jira_create_issue,linear_create_issue,openai_chat,gemini_generate,tavily_search]}
def call_tool(name,args):
    if name not in DISPATCH: raise ConnectorError("Unknown tool: "+str(name))
    if not isinstance(args,dict): raise ConnectorError("Tool arguments must be an object")
    return DISPATCH[name](**args)
