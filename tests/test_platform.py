import sys,unittest,json
from unittest.mock import patch
sys.path.insert(0,"src")
from mcp_server import handle
from discovery import discover_connectors
from oauth_manager import OAuth2Manager,OAuthError
class PlatformTests(unittest.TestCase):
 def test_resources_list(self): self.assertEqual(len(handle({"id":1,"method":"resources/list"})["result"]["resources"]),2)
 def test_catalog_resource(self):
  r=handle({"id":2,"method":"resources/read","params":{"uri":"connectors://catalog"}})
  self.assertEqual(len(json.loads(r["result"]["contents"][0]["text"])),10)
 def test_prompts(self):
  self.assertEqual(len(handle({"id":3,"method":"prompts/list"})["result"]["prompts"]),2)
  r=handle({"id":4,"method":"prompts/get","params":{"name":"plan_connector","arguments":{"service":"Example","use_case":"search"}}})
  self.assertIn("Example",r["result"]["messages"][0]["content"]["text"])
 def test_discovery(self): self.assertEqual(len(discover_connectors()),10)
 def test_oauth_https(self):
  with self.assertRaisesRegex(OAuthError,"HTTPS"): OAuth2Manager("http://bad","id","secret")
 def test_oauth_cache(self):
  m=OAuth2Manager("https://issuer.example/token","id","secret")
  def issue(fields):
   m._token="mock-token"; m._expires_at=9999999999
   return "mock-token"
  with patch.object(m,"_post",side_effect=issue) as post:
   self.assertEqual(m.access_token(),"mock-token"); self.assertEqual(m.access_token(),"mock-token"); post.assert_called_once()
if __name__=="__main__": unittest.main()
