"""Aperçu de la version compilée, sans installation de dépendances ni backend."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import threading,webbrowser
root=Path(__file__).resolve().parent/'frontend'/'dist'
if not (root/'index.html').exists():raise SystemExit('Version compilée absente. Exécutez npm run build dans frontend.')
handler=partial(SimpleHTTPRequestHandler,directory=str(root))
print('Aperçu : http://127.0.0.1:8085 — Ctrl+C pour fermer.\nLe formulaire et l’administration nécessitent Django (DEMARRER.bat).')
server=ThreadingHTTPServer(('127.0.0.1',8085),handler)
threading.Timer(1,lambda:webbrowser.open('http://127.0.0.1:8085')).start()
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
