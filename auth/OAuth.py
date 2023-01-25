import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# package need to install
# google-api-python-client
# google-auth-oauthlib

class GoogleOAuth(object):
    
    home = os.getenv('HOME')
    scopes = ["https://www.googleapis.com/auth/userinfo.profile"]
    # credencial = {"installed":{"client_id":"YOUR-CLIENT_ID.apps.googleusercontent.com","project_id":"YOUR-PROJECT-ID","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"YOUR_CLIENT_SECRET","redirect_uris":["http://localhost"]}}
    credencial = {"installed":{"client_id":"834833311214-q58q01f1kas0299ak1u9voc6h4ldntsv.apps.googleusercontent.com","project_id":"qqda-372912","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
    
    def __init__(self, dotfile):
        self.config = "".join([self.home, '/.', dotfile])
        self.credential_file = "".join([self.config, '/credential.json'])
        self.token_file = "".join([self.config, '/token.json']) 
        self.tmp = "".join([self.config, '/.tmp'])
        if os.path.isdir(self.config) == False:
            os.system("mkdir %s"%(self.config))
    

    def write_file(self, file, data):
        with  open(file, 'w') as f:
            f.write(data)

    def get_info(self, creds):
        user_info_service = build(
            serviceName='oauth2', version='v2',
            credentials=creds)
        return  user_info_service.userinfo().get().execute()


    def is_login(self):        
            
        if os.path.isfile(self.token_file) == False:
            return False

        creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not creds or not creds.valid:
            return False 

        return self.get_info(creds)

    def login(self):
        creds = None
        if os.path.isfile(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(self.credencial, self.scopes)
                creds = flow.run_local_server(port=0)

        self.write_file(self.token_file, creds.to_json())

        return self.get_info(creds)

    def logout(self):
        os.system('rm %s'%(self.token_file))