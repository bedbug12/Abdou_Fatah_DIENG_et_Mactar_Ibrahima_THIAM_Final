import tkinter as tk
from tkinter import ttk
import time
# Définition de l'automate
table = {
    # 1: {'a': {1, 2}, 'b': {1}},
    # 2: {'a': {3}, 'b': {3}},
    # 3: {'a': {4}, 'b': {4}},
    # 4: {}
    
# etats_initiaux = {1, 2}
# etats_acceptants = {4}
# 
#     1: {'a': {2, 3}, 'b': {2}},
#     2: {'a': {4}, 'b': {3}},
#     3: {'a': {3}, 'b': {4}},
#     4: {'a': {4}, 'b': {4}}
# 
# etats_initiaux = {1, 2}
# etats_acceptants = {4}

}




def create_automaton():
    for child in transition_frame.winfo_children():
        child.destroy()
    # récupérer les données de l'utilisateur
    alphabet = alphabet_entry.get().split(",")
    n_states = int(states_entry.get())
    
    # créer la table de transition vide
    global table
    table = {}
    for i in range(n_states):
        table[i+1] = {}
        for symbol in alphabet:
            table[i+1][symbol] = None

    # ajouter le Treeview à la fenêtre principale
    tree = ttk.Treeview(transition_frame)
    tree.grid(row=0, column=1, padx=20, pady=20)

    # créer le Treeview pour la table de transition
    tree.configure(columns=[str(i) for i in range(len(alphabet)+1)], show="headings")
    for i in range(len(alphabet)):
        tree.heading(str(i+1), text=str(alphabet[i]))
    for i in range(len(alphabet)+1):
        tree.column(str(i), width=50)

    # ajouter les entrées pour chaque transition
    for i in range(n_states):
        tree.insert("", "end", values=[i+1])

    # définir la fonction de modification de cellule
    def edit_cell(event):
        # récupérer les indices de la cellule sélectionnée
        row_id = tree.selection()[0]
        col_id = tree.identify_column(event.x)

        # ouvrir l'éditeur de cellule
        cell_editing_window = tk.Toplevel(root)
        cell_editing_window.title(f"Edit Cell ({row_id}, {col_id})")

        # ajouter une entrée pour la valeur de la cellule
        cell_value_entry = tk.Entry(cell_editing_window)
        cell_value_entry.pack()

        # ajouter un bouton pour sauvegarder la valeur
        def save_cell_value():
            value = cell_value_entry.get()
            tree.set(row_id, col_id, value)
            cell_editing_window.destroy()

        save_button = tk.Button(cell_editing_window,text="Save", command=save_cell_value)
        save_button.pack()

    # lier la fonction de modification de cellule au clic gauche
    tree.bind("<Double-1>", edit_cell)

    # ajouter un bouton pour récupérer les données depuis le Treeview
    def get_table_data():
         # Récupère la table de transition depuis le Treeview.
        for i in range(n_states):
            for symbol in alphabet:
                cell_values = tree.item(tree.get_children()[i], "values")[alphabet.index(symbol)+1]
                table[i+1][symbol]=[]
                for cell_value in cell_values.split(","):
                    if cell_value.isdigit():
                        table[i+1][symbol].append(int(cell_value))
                    else:
                        if table[i+1][symbol]==[]:
                            table[i+1].pop(symbol)
        # Creation de l'animation
        create_widgets()

    get_data_button = tk.Button(transition_frame, text="Créer Automate", command=get_table_data)
    get_data_button.grid(row=2, column=1, padx=10)


# Fonction pour simuler l'automate
def simuler_automate(table, etat, chaine):
    global tab_etat,bande,n_success
    tab_etat=[states[etat-1]]
    bande=[]
    n_success=[0]
    if etat in [int(state) for state in final_states_entry.get().split(",")]:
        return True
    elif chaine == '':
        return False
    else:
        transitions = table[etat].get(chaine[0], set())
        for i in transitions:
            if simuler_automate(table, i, chaine[1:]):
                #recupérer la lettre et l'etat de transition pour la simulation
                tab_etat.append(states[etat-1])
                bande.append([chaine[0],i])
                n_success.append(n_success[-1]+1)
                #Si on trouve un etat acceptant on arrête
                return True
            #recupérer la lettre et l'etat de transition pour la simulation
            tab_etat.append(states[etat-1])
            bande.append([chaine[0],i])
        return False
           

# Fonction pour afficher le résultat de la simulation
def afficher_resultat(resultat):
    if resultat:
        message["text"] = "La chaîne est acceptée"
        message["fg"] = "green"
    else:
        message["text"] = "La chaîne n'est pas acceptée"
        message["fg"] = "red"



# Fonction pour simuler le mot
def lecture_afn():
    global bandes,tab_etats,n_success
    mot = entry_mot.get()
    etats_initials= [int(etat_initial) for etat_initial in initial_state_entry.get().split(",") ]
    
    resultats=[]
    bandes=[]
    tab_etats=[]

    # Cette boucle parcourt les états initiaux, en exécutant pour chaque état initial la fonction 
    for etat_initial in etats_initials:
        resultat= simuler_automate(table ,etat_initial , mot)
        if resultat:
            # Si resultat est True, la liste tab_etat est inversée et ajoutée à la liste tab_etats.
            tab_etat.reverse()
            tab_etats.append(tab_etat)

        bande.reverse()
        reste=list(mot)
        #Si resultat est True, une boucle est exécutée pour ajouter les lettres de reste à la liste bande à partir de l'indice n_success[-1].
        if resultat:
            for i in range(n_success[-1],len(reste)):
                l,c=bande[-1]
                bande.append([reste[i],c])
        bandes.append(bande)
        resultats.append(resultat)

    if True in resultats:
        afficher_resultat(True)
    else:
        afficher_resultat(False)
    




def create_widgets():
    global states

    # Effacer le canvas
    canvas.delete("all")
    
    # Recuperer le nombre d'Etat et les etats initiaux
    etats=int(states_entry.get())
    etat_final = [int(state) for state in final_states_entry.get().split(",")]
    etat_initial=[int(etat_initial) for etat_initial in initial_state_entry.get().split(",") ]
    
    # Donner à chaque etat une position sur le canvas
    positions={}
    inc=0
    for i in range(1,etats+1):
        if i%2==0:
            positions[i]=(75+inc, 250)
        else:
            positions[i]=(75+inc, 100)
        inc+=150

    # Ajouter des états
    states=[]
    for i in range(1,etats+1):
        x, y = positions[i]
        if i in etat_final:
            canvas.create_oval(x-25-10, y-25-10, x+25+10, y+25+10, outline="black")
        if i in etat_initial:
            states.append(canvas.create_oval(x-25, y-25, x+25, y+25, fill="white",tags="final" if i in etat_final else "", outline='#28AAFF',width=2))
        else:
            states.append(canvas.create_oval(x-25, y-25, x+25, y+25, fill="white",tags="final" if i in etat_final else ""))
        canvas.create_text(x, y, text=str(i))

        

    # Ajouter des transitions
    transitions = []
    for orig, trans in table.items():
        if orig!=None:
            x1, y1 = positions[orig]
        for lettre, dest in trans.items():
            if dest!=None:
                for i in dest:
                    x2, y2 = positions[i]
                    if i==orig and  orig!=None and i!=None:
                        # Dessin d'un cercle semi-fermé our les boucles
                        x = 50  # Coordonnée x du centre du cercle
                        rayon = 12  # Rayon du cercle
                        angle_debut = 60  # Angle de départ du cercle en degrés
                        angle_fin = 350  # Angle d'arrivée du cercle en degrés
                        #pour eviter la superposition d'élements on regarde s'il n'y a pas de d'element sur cette zone
                        elements = canvas.find_overlapping(x1 - rayon, y1 - x - rayon, x1 + rayon, y1 - x + rayon)
                        if elements:
                            x2=x1+30
                            y2=y1+10
                            canvas.create_arc(x2 - rayon, y2 - x - rayon, x2 + rayon, y2 - x + rayon, start=angle_debut, extent=angle_fin - angle_debut, style=tk.ARC)
                            canvas.create_text(x2, y2-x, text=lettre)
                        else:
                            canvas.create_arc(x1 - rayon, y1 - x - rayon, x1 + rayon, y1 - x + rayon, start=angle_debut, extent=angle_fin - angle_debut, style=tk.ARC)
                            canvas.create_text(x1, y1-x, text=lettre)
                    else:
                        if x1>x2:
                            transitions.append(canvas.create_line(x1-30, y1, x2+30, y2, arrow="last",width=1))
                            canvas.create_text((x1+x2)/2-20, (y1+y2)/2-10, text=lettre)
                        else: 
                            transitions.append(canvas.create_line(x1+30, y1, x2-30, y2, arrow="last",width=1))
                            canvas.create_text((x1+x2)/2+20, (y1+y2)/2+10, text=lettre)




def step():
    global current_state,cpt,t_bandes,tab_etat
    
    current_state = tab_etat[cpt]
    if cpt!=len(tab_etat):
        cpt+=1
    
    # Mettre à jour la couleur de l'état actuel
    for tab_etat in  tab_etats:
        for state in tab_etat:
            if state == current_state and current_state==False :
                canvas.itemconfig(tab_etat[-2], fill="red")
            elif state == current_state and canvas.itemcget(state, "tags")!="final" and cpt==len(tab_etat) :
                canvas.itemconfig(state, fill="red")
            elif state == current_state and canvas.itemcget(state, "tags")=="final" and cpt==len(tab_etat) :
                canvas.itemconfig(state, fill="#33FF00")
            elif state == current_state:
                canvas.itemconfig(state, fill="white")
                canvas.update()
                time.sleep(1/50)
                canvas.itemconfig(state, fill="orange")
            else:
                canvas.itemconfig(state, fill="white")
    

    x, y= 100, 330
    etat_initial=[int(etat_initial) for etat_initial in initial_state_entry.get().split(",") ]
    for bande in bandes:
        t_bandes.append(canvas.create_rectangle(x,y,x+50,y+50, fill='#28AAFF', outline="white"))
        t_bandes.append(canvas.create_text((x+x+50)/2, (y+y+50)/2, text=str(etat_initial[bandes.index(bande)]), font=('Arial', 24), fill="white"))
        x+=50
        for lettre,etat in bande:
            t_bandes.append(canvas.create_rectangle(x,y,x+50,y+50, fill='orange', outline="white"))
            # Ajouter la lettre
            t_bandes.append(canvas.create_text((x+x+50)/2, (y+y+50)/2, text=str(lettre), font=('Arial', 24)))
            t_bandes.append(canvas.create_text((x+x+50)/2, (y+y+50)/2+50, text=str(etat), font=('Arial', 24)))
            x+=50



def reset():
    global current_state,cpt,t_bandes
    # Réinitialiser l'état actuel
    current_state = states[0]
    cpt=0
    # Réinitialiser la couleur de tous les états
    for state in states:
        canvas.itemconfig(state, fill="white")
    
    for bande in t_bandes:
        canvas.delete(bande)





# Créer la fenêtre principale
root = tk.Tk()
root.title("Simulateur d'automate finis non déterministe")
root.wm_minsize(width=500,height=500)

canvas_frame = ttk.LabelFrame(root, text="Simulation de la lecture par l\'automate")
canvas_frame.grid(row=0, column=1,padx=10, pady=2)
canvas_frame.place(x=300,y=0)

# Créer le canevas
canvas = tk.Canvas(canvas_frame,scrollregion=(0, 0, 2000, 600))
canvas.config(width=900, height=500,bg="#FFFDE7")
canvas.grid(row=0, column=1, columnspan=2)

scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.grid(row=0, column=0)

scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.grid(row=0, column=0)

canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)


# Ajouter du champ de saisie
entry_mot = tk.Entry(canvas_frame,font=8)
entry_mot.grid(row=1, column=2)


message = tk.Label(canvas_frame, width=80, height=3, font=12,)
message.grid(row=2, column=2)

# Ajouter des boutons
button_step = tk.Button(canvas_frame, text="Etapes de Transition", command=step)
button_step.grid(row=3, column=1)

button_submit = tk.Button(canvas_frame, text="Soumettre Mot", command=lecture_afn)
button_submit.grid(row=3, column=2)

button_reset = tk.Button(canvas_frame, text="Effacer Transition", command=reset)
button_reset.grid(row=3, column=3)

# Initialisaton des globals

states = []
cpt = 0
t_bandes = []
tab_etat=[]
bande=[]
bandes=[]
tab_etats=[]
n_success=[]

input_frame = ttk.LabelFrame(root, text="Paramètres d'entrée")
input_frame.grid(row=0, column=0)
input_frame.place(x=0,y=0)

transition_frame = ttk.LabelFrame(root, text="Table de transition")
transition_frame.grid(row=1, column=0, pady=10)
transition_frame.place(x=0,y=270)

# ajouter les champs de saisie pour l'utilisateur
alphabet_label = tk.Label(input_frame, text='Alphabet (séparé par virgule ","):')
alphabet_label.grid(row=0, column=1,padx=5, pady=5)
alphabet_entry = tk.Entry(input_frame)
alphabet_entry.grid(row=1, column=1)

states_label = tk.Label(input_frame, text="Nombre d'Etats:")
states_label.grid(row=2, column=1,padx=5, pady=5)
states_entry = tk.Entry(input_frame)
states_entry.grid(row=3, column=1)

initial_state_label = tk.Label(input_frame, text='Etats Initial (séparé par virgule ","):')
initial_state_label.grid(row=4, column=1,padx=5, pady=5)
initial_state_entry = tk.Entry(input_frame)
initial_state_entry.grid(row=5, column=1)

final_states_label = tk.Label(input_frame, text='Etats Finaux (séparé par virgule ","):')
final_states_label.grid(row=6, column=1,padx=5, pady=5)
final_states_entry = tk.Entry(input_frame)
final_states_entry.grid(row=7, column=1)

# ajouter un bouton pour créer l'automate
create_button = tk.Button(input_frame, text="Table de transition", command=create_automaton)
create_button.grid(row=8, column=1,padx=5, pady=5)

# Démarrer la boucle d'événements tkinter
root.mainloop()



# Le programme utilise le module tkinter pour créer une interface utilisateur graphique (GUI) avec des 
# widgets tels que Entry, Button et Treeview. 
# Le widget Treeview affiche la table des transitions de l'automate, permettant à l'utilisateur d'éditer 
# les transitions en double-cliquant sur une cellule. Le programme lit alors la table éditée et effectue la 
# simulation.

# La fonction de simulation est une fonction récursive qui prend l'état actuel, la chaîne d'entrée et la 
# table de transition comme entrées. Il vérifie si l'état actuel est un état d'acceptation, si c'est le cas, il 
# renvoie True. Si la chaîne d'entrée est vide, elle renvoie False. Sinon, il obtient l'ensemble des 
# transitions pour le premier symbole de la chaîne d'entrée à partir de la table de transition et 
# s'appelle de manière récursive sur chaque transition avec la chaîne d'entrée restante. Si l'un des 
# appels récursifs renvoie True, la fonction renvoie True. Si aucun des appels récursifs ne renvoie True, 
# la fonction renvoie False.

# La fonction de simulation enregistre également le chemin suivi par l'automate sur la chaîne d'entrée 
# en ajoutant l'état actuel et le symbole qu'il a lu à deux listes globales, tab_etat et bande, 
# respectivement. Le programme affiche ensuite le chemin à l'aide du module canvas. La liste 
# n_success enregistre le nombre de transitions réussies consécutives effectuées par l'automate. Ces 
# informations sont utilisées pour colorer les bords du chemin.

# Dans l'ensemble, le programme est un outil simple mais utile pour apprendre et expérimenter avec 
# des automates.

