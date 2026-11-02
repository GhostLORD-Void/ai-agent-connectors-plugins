"""Connector discovery metadata for agent frameworks and admin UIs."""
from connectors import TOOLS
SERVICES={
"github":{"category":"developer","auth_env":["GITHUB_TOKEN"],"tools":["github_list_repos","github_create_issue"]},
"gitlab":{"category":"developer","auth_env":["GITLAB_TOKEN"],"tools":["gitlab_list_projects"]},
"slack":{"category":"communication","auth_env":["SLACK_BOT_TOKEN"],"tools":["slack_send_message"]},
"discord":{"category":"communication","auth_env":["webhook_url"],"tools":["discord_send_webhook"]},
"notion":{"category":"knowledge","auth_env":["NOTION_TOKEN"],"tools":["notion_search"]},
"jira":{"category":"project-management","auth_env":["JIRA_BASE_URL","JIRA_EMAIL","JIRA_API_TOKEN"],"tools":["jira_create_issue"]},
"linear":{"category":"project-management","auth_env":["LINEAR_API_KEY"],"tools":["linear_create_issue"]},
"openai":{"category":"models","auth_env":["OPENAI_API_KEY"],"tools":["openai_chat"]},
"gemini":{"category":"models","auth_env":["GEMINI_API_KEY"],"tools":["gemini_generate"]},
"tavily":{"category":"search","auth_env":["TAVILY_API_KEY"],"tools":["tavily_search"]}}
def discover_connectors():
    by_name={x["name"]:x for x in TOOLS}
    return [{"id":n,"category":m["category"],"authentication":m["auth_env"],
             "tools":[by_name[t] for t in m["tools"]],"status":"experimental"} for n,m in SERVICES.items()]
