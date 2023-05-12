import tkinter as tk
import subprocess

# Création de la fenêtre principale
root = tk.Tk()

# Définition de la fonction pour lancer le premier programme
def program_1():
    subprocess.Popen(["python", "simulateur_AFD.py"])

# Définition de la fonction pour lancer le deuxième programme
def program_2():
    subprocess.Popen(["python", "simulateur_AFN.py"])

# Création des deux boutons
button_1 = tk.Button(root, text="simulateur_AFD", command=program_1)
button_2 = tk.Button(root, text="simulateur_AFN", command=program_2)
message_1 = tk.Label(root, height=3, font=12, text="Si vous voulez simuler un automate fini déterministe \nCliquez ici:")
message_2 = tk.Label(root, height=3, font=12, text="Si vous voulez simuler un automate fini non déterministe \nCliquez ici:")
message_3 = tk.Label(root, height=3, text="Vous pouvez aussi simuler un automate fini déterministe ici sur SIMULATEUR_AFN,\ncependant ce simulateur peut ne pas être très performant pour certains AFD")

# Placement des boutons dans la fenêtre
message_1.pack()
button_1.pack()
message_2.pack()
button_2.pack()
message_3.pack()

# Affichage de la fenêtre
root.mainloop()
