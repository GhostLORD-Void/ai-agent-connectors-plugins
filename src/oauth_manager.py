"""Generic OAuth 2.0 client-credentials and refresh-token helper; memory-only token cache."""
import json, os, time, urllib.parse, urllib.request, urllib.error
from threading import RLock
class OAuthError(RuntimeError): pass
class OAuth2Manager:
    def __init__(self,token_url,client_id,client_secret,*,scope=None,audience=None,timeout=20):
        if not token_url.startswith("https://"): raise OAuthError("OAuth token endpoint must use HTTPS")
        self.token_url=token_url; self.client_id=client_id; self.client_secret=client_secret
        self.scope=scope; self.audience=audience; self.timeout=timeout
        self._token=None; self._expires_at=0; self._refresh_token=None; self._lock=RLock()
    @classmethod
    def from_env(cls,prefix):
        def get(s,required=True):
            v=os.getenv(prefix+"_"+s)
            if required and not v: raise OAuthError("Missing environment variable: "+prefix+"_"+s)
            return v
        return cls(get("TOKEN_URL"),get("CLIENT_ID"),get("CLIENT_SECRET"),scope=get("SCOPE",False),audience=get("AUDIENCE",False))
    def _post(self,fields):
        req=urllib.request.Request(self.token_url,data=urllib.parse.urlencode(fields).encode(),
            headers={"Accept":"application/json","Content-Type":"application/x-www-form-urlencoded"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as r: result=json.loads(r.read().decode())
        except urllib.error.HTTPError as e: raise OAuthError("OAuth token endpoint returned HTTP "+str(e.code)) from None
        except (urllib.error.URLError,TimeoutError) as e: raise OAuthError("OAuth token request failed: "+str(e)) from None
        token=result.get("access_token")
        if not token: raise OAuthError("OAuth response did not include access_token")
        self._token=token; self._expires_at=time.time()+max(0,int(result.get("expires_in",3600))-60)
        self._refresh_token=result.get("refresh_token",self._refresh_token)
        return token
    def access_token(self):
        with self._lock:
            if self._token and time.time()<self._expires_at: return self._token
            fields={"client_id":self.client_id,"client_secret":self.client_secret}
            if self._refresh_token: fields.update(grant_type="refresh_token",refresh_token=self._refresh_token)
            else:
                fields["grant_type"]="client_credentials"
                if self.scope: fields["scope"]=self.scope
                if self.audience: fields["audience"]=self.audience
            return self._post(fields)
    def clear(self):
        with self._lock: self._token=None; self._expires_at=0; self._refresh_token=None
