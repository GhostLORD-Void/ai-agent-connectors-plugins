import os,sys,unittest
from unittest.mock import patch
sys.path.insert(0,"src")
import connectors
from mcp_server import handle
class Tests(unittest.TestCase):
 def test_tool_registry(self):
  self.assertEqual(len(connectors.TOOLS),11)
  self.assertEqual(set(connectors.DISPATCH),{x["name"] for x in connectors.TOOLS})
 def test_missing_token(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaisesRegex(connectors.ConnectorError,"GITHUB_TOKEN"): connectors.github_list_repos()
 def test_github_auth(self):
  with patch.dict(os.environ,{"GITHUB_TOKEN":"dummy"}),patch.object(connectors,"request_json",return_value=[]) as req:
   self.assertEqual(connectors.github_list_repos(5),[])
   self.assertEqual(req.call_args.kwargs["headers"]["Authorization"],"Bearer dummy")
 def test_discord_url_validation(self):
  with self.assertRaisesRegex(connectors.ConnectorError,"Discord HTTPS"): connectors.discord_send_webhook("https://example.com/x","hi")
 def test_mcp_initialize(self):
  self.assertEqual(handle({"id":1,"method":"initialize"})["result"]["serverInfo"]["name"],"ai-agent-connectors-plugins")
 def test_mcp_list(self):
  self.assertEqual(len(handle({"id":2,"method":"tools/list"})["result"]["tools"]),11)
 def test_unknown_tool(self):
  self.assertTrue(handle({"id":3,"method":"tools/call","params":{"name":"missing","arguments":{}}})["result"]["isError"])
if __name__=="__main__": unittest.main()
