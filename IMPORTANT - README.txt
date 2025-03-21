=============================
======= WOKE INVADERS =======
=============================


============= !!! NEW !!! =============
woke_invaders.exe fonctionnel !!

- Réalisé avec auto-py-to-exe (https://pypi.org/project/auto-py-to-exe/)
- Le code a été modifié pour le packaging; le code présent dans main.py est non-modifié et les dépendances nécéssaires présentées plus bas sont toujours nécéssaires pour sa bonne execution
- Le code modifié dans main for exe.py a été fait suivant les recommandation présentes sur https://github.com/TomSchimansky/CustomTkinter/discussions/939

- Votre antivirus n'aimera pas ce .exe, il faudra lui accorder une exception // De même pour windows
- Promis c'est pas un virus

=======================================


Pour execution du code depuis VSCode:

Dépendances nécessaires à la bonne exécution: 
Si vous ne les avez pas installés, exécutez les commandes suivantes (cmd ou PowerShell)

Python (évidemment)
	pip install python3
	
Pillow
	pip install Pillow

Playsound:
	pip install --upgrade setuptools Wheel
	pip install playsound
	

En cas d'erreur de compilation:
	pip install playsound==1.2.2   

Veuiller à ce que le chemin d'accès du programme ne comporte pas de caractère spécial ou d'accents.
Bien modifier la variable path au début du fichier en indiquant le chemin du dossier sous la forme suivante:

"C:/Chemin/vers/le/dossier/"

/!\ Remplacer les anti-slash windows (\) par des slashs (/) /!\



