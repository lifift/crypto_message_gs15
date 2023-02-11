# crypto_message_gs15

Petit projet de cryptographie qui se base de concepts de l'application de messagerie Signal:
- X3DH
- RC4
- Feistel
- Sha3 ?
- Double ratchet

La partie applicative n'est pas incroyable et tout fonctionne en local ( pas de socket / pas de script "serveur" ...) mais la philosophie et le flow de fonctionnement de Signal sont plutot bien reproduit.




Utilisation :
- 0 # Il faut créer un dossier nommé "personnal_data" à la racine du programme.
- 1 # Executer client.py pour obtenir un ou deux CLI.
- 2 # Entrer deux nom différents dans chaque CLI, le programme va initialiser toute les clés cryptographiques dans des fichiers locaux.
- 3 # Communiquer entre les deux pesonnages créés, il faut penser à raffraichir pour recevoir les messages.
- 4 # Si une erreur survient il faut vider le contenue des fichiers "serveur" et supprimer les fichiers "utilisateur" pour pouvoirs reprendre les tests.
