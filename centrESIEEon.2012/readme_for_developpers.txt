TRUNK?
C'est le r�pertoire principal, celui dans lequel on va travailler pour faire �voluer le projet.
TAGS?
Dans ce r�pertoire on va placer les versions fig�es du projet, des snapshots de version stable. Par exemple la version 1.0, puis 1.1,� Il faut consid�rer ce r�pertoire comme �tant en lecture seule. Une sorte d'historique des diff�rents versions.
BRANCHES?
On va retrouver ici, une zone de travail diff�rente du TRUNK, qui permettra de faire �voluer des versions en parall�les du TRUNK. Par exemple, lorsque l'on doit effectuer une correction sur la version 0.6, alors que l'on travaille d�j� sur la version 0.7, on pourra placer une copie de TAGS/0.6 dans BRANCHES/0.6.x; une fois le travail termin� on pourra cr�er un TAGS/0.6.1 bas� sur BRANCHES/0.6.x.


Source : http://blog.geturl.net/post/2009/04/20/%5Bsvn%5D-Trunk-Tags-Branches-!