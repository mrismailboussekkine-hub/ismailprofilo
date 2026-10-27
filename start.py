"""Serveur local uniquement ; ne pas utiliser pour exposer le site sur Internet."""
import os, subprocess, sys, threading, webbrowser
from pathlib import Path
root=Path(__file__).resolve().parent
python=root/'.venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
if not python.exists():raise SystemExit('Exécutez d’abord python setup.py ou INSTALLER.bat.')
print('Portfolio : http://127.0.0.1:8000\nAdministration : http://127.0.0.1:8000/admin/\nCtrl+C pour arrêter.')
threading.Timer(2,lambda:webbrowser.open('http://127.0.0.1:8000')).start()
try: subprocess.run([str(python),'manage.py','runserver','127.0.0.1:8000'],cwd=root/'backend',check=True)
except KeyboardInterrupt:pass
except subprocess.CalledProcessError as exc:sys.exit(exc.returncode)
