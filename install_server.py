#!/usr/bin/python


#! run script with ROOT Privileges


# intsall & start a backend app via systemD



from os import path, getlogin
from pathlib import Path
import subprocess as sb

# define constants
username = getlogin()
sources = ("fastapi_backend.service",)
BASE = path.dirname(__file__)

backend_service_templated = f"""
[Unit]
Description=A Systemd service runner for app backend
After=network.target

[Service]
User={username}
Group={username}
WorkingDirectory={BASE}/
Environment="PATH={BASE}/.venv/bin"
ExecStart={BASE}/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000



[Install]
WantedBy=multi-user.target # NOTE: this line helps to start-up the service on every boot-action
"""


def main():
    """logic entry"""
    
    for file in sources:
        
        source_path = Path().joinpath(BASE,file)
        
        #* Generate Service
        with open(source_path, "w") as curr_file:
            if source_path.name == sources[0]:
                curr_file.write(backend_service_templated)
                
                    
        if not path.exists(Path().joinpath(BASE,file)):
            print(f"Failed To Generate Requeired Files: {file}")
            return -1
        
        #* Last Generated-file Check
        with open(source_path, "r") as curr_file:
            if source_path.name==sources[0] and "[Install]\n" not in curr_file.readlines():
                print(f"File Empty/Incomplete: {file}")
                return -1
        
        #* install & run service
        if source_path.name==sources[0]: #* Install Fastapi_backend service
            # instruction = ("success_msg", instruction)
            
            # this structure (lists) 
            cp_fastapi_service = (f"\033[92mService Copied:\033[0m {source_path.name}", ("cp", source_path, "/etc/systemd/system/"))
            reload_systemd = (f"\033[92mService Reloaded :\033[0m {source_path.name}", ("systemctl", "daemon-reload"))
            enable_service = (f"\033[92mService Enabled:\033[0m {source_path.name}", ("systemctl", "enable", "--now", source_path.name))
            start_service =(f"\033[92mService Started :\033[0m {source_path.name}", ("systemctl", "start", "--now", source_path.name))
            
            args = (cp_fastapi_service, reload_systemd, enable_service, start_service)
            for arg in args:
                proccess = sb.Popen(arg[1])
                if proccess.returncode != 0: print(arg[0])
                else: print("[red]Failed With Error[/red]:",proccess.stderr)
                    

if __name__ == '__main__':
    main()