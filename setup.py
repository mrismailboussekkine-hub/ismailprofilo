"""Installation locale : python setup.py (Python 3.10 ou plus)."""
import os
import subprocess
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
backend=root/'backend'
env=root/'.venv'
python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
def run(args,cwd=backend): subprocess.run([str(x) for x in args],cwd=cwd,check=True)
def main():
    if sys.version_info<(3,10):raise SystemExit('Python 3.10 minimum est nécessaire.')
    print('1/4 — Création de l’environnement Python')
    if not python.exists():run([sys.executable,'-m','venv',env],root)
    print('2/4 — Installation des dépendances (connexion Internet nécessaire)')
    run([python,'-m','pip','install','-r','requirements.txt'])
    print('3/4 — Préparation de la base et du contenu')
    run([python,'manage.py','migrate'])
    run([python,'manage.py','seed_portfolio'])
    run([python,'manage.py','check'])
    print('4/4 — Création de votre administrateur (aucun compte prédéfini)')
    answer=input('Créer un administrateur maintenant ? [O/n] : ').strip().lower()
    if answer not in ('n','non'):run([python,'manage.py','createsuperuser'])
    print('\nPrêt ! Lancez DEMARRER.bat sous Windows ou python start.py.')
if __name__=='__main__':
    try:main()
    except subprocess.CalledProcessError as exc:
        print('\nInstallation interrompue. Corrigez l’erreur affichée, puis relancez setup.py. Vos données existantes sont conservées.')
        sys.exit(exc.returncode)
