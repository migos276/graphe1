"""
Analyseur de Graphes - Module Principal
Université de Yaoundé I - Département d'Informatique
Licence 2 - Supervisé par Dr Manga MAXWELL

Membres:
- DIZE TCHEMOU MIGUEL CAREY
- SAGUEN KAMDEM CHERYL RONALD  
- SIGNE FONGANG WILFRIED BRANDON
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from graph_core import GraphAnalyzer
from report_generator import ReportGenerator

class GraphAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Graphes - Université de Yaoundé I")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.analyzer = GraphAnalyzer()
        self.report_gen = ReportGenerator()
        self.current_graph = None
        
        self.setup_ui()
        self.show_guide()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = ttk.Label(main_frame, text="Analyseur de Graphes", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de saisie
        input_frame = ttk.LabelFrame(main_frame, text="Saisie du Graphe", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Type de représentation
        ttk.Label(input_frame, text="Type de représentation:").grid(row=0, column=0, sticky=tk.W)
        self.graph_type = tk.StringVar(value="matrice")
        ttk.Radiobutton(input_frame, text="Matrice d'adjacence", variable=self.graph_type, 
                       value="matrice").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Liste d'adjacence", variable=self.graph_type, 
                       value="liste").grid(row=0, column=2, sticky=tk.W)
        
        # Zone de saisie
        ttk.Label(input_frame, text="Données du graphe:").grid(row=1, column=0, sticky=tk.NW, pady=(10, 0))
        self.input_text = scrolledtext.ScrolledText(input_frame, width=60, height=8)
        self.input_text.grid(row=1, column=1, columnspan=2, pady=(10, 0), padx=(10, 0))
        
        # Boutons d'action
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Charger Fichier", command=self.load_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Analyser", command=self.analyze_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guide", command=self.show_guide).pack(side=tk.LEFT, padx=5)
        
        # Frame des résultats
        results_frame = ttk.LabelFrame(main_frame, text="Résultats de l'Analyse", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=70, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de visualisation
        viz_frame = ttk.LabelFrame(main_frame, text="Visualisation", padding="10")
        viz_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=(10, 0))
        
        # Canvas pour matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bouton de rapport
        report_frame = ttk.Frame(main_frame)
        report_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(report_frame, text="Générer Rapport HTML", command=self.generate_report).pack()
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def show_guide(self):
        """Affiche le guide d'utilisation"""
        guide_text = """
GUIDE D'UTILISATION - ANALYSEUR DE GRAPHES

1. MATRICE D'ADJACENCE:
   Format: Une matrice carrée où chaque ligne représente un sommet
   Exemple pour un graphe à 4 sommets:
   0 1 1 0
   1 0 0 1
   1 0 0 1
   0 1 1 0

2. LISTE D'ADJACENCE:
   Format: Chaque ligne commence par le sommet suivi de ses voisins
   Exemple:
   0: 1 2
   1: 0 3
   2: 0 3
   3: 1 2

3. CHARGEMENT DE FICHIER:
   - Fichiers .txt supportés
   - Même format que la saisie manuelle

4. FONCTIONNALITÉS:
   - Calcul des degrés (min, max, moyen)
   - Détection des boucles
   - Visualisation du graphe
   - Génération de rapport académique

5. TYPES DE GRAPHES SUPPORTÉS:
   - Graphes orientés et non-orientés
   - Graphes avec boucles
   - Graphes connexes et non-connexes
        """
        
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Guide d'Utilisation")
        guide_window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, guide_text)
        text_widget.config(state=tk.DISABLED)
    
    def load_file(self):
        """Charge un fichier contenant le graphe"""
        filename = filedialog.askopenfilename(
            title="Charger un fichier de graphe",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(1.0, content)
                messagebox.showinfo("Succès", "Fichier chargé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def clear_input(self):
        """Efface la zone de saisie"""
        self.input_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()
    
    def analyze_graph(self):
        """Analyse le graphe saisi"""
        try:
            input_data = self.input_text.get(1.0, tk.END).strip()
            if not input_data:
                messagebox.showwarning("Attention", "Veuillez saisir les données du graphe!")
                return
            
            graph_type = self.graph_type.get()
            
            # Analyser le graphe
            if graph_type == "matrice":
                self.current_graph = self.analyzer.from_adjacency_matrix(input_data)
            else:
                self.current_graph = self.analyzer.from_adjacency_list(input_data)
            
            # Obtenir les résultats
            results = self.analyzer.analyze_graph()
            
            # Afficher les résultats
            self.display_results(results)
            
            # Visualiser le graphe
            self.visualize_graph()
            
            messagebox.showinfo("Succès", "Analyse terminée avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse: {str(e)}")
    
    def display_results(self, results):
        """Affiche les résultats de l'analyse"""
        self.results_text.delete(1.0, tk.END)
        
        output = f"""
═══════════════════════════════════════════════════════════
                    ANALYSE DU GRAPHE
═══════════════════════════════════════════════════════════

INFORMATIONS GÉNÉRALES:
• Nombre de sommets: {results['nb_vertices']}
• Nombre d'arêtes: {results['nb_edges']}
• Type: {'Orienté' if results['is_directed'] else 'Non-orienté'}
• Contient des boucles: {'Oui' if results['has_loops'] else 'Non'}

ANALYSE DES DEGRÉS:
• Degré minimum: {results['min_degree']}
• Degré maximum: {results['max_degree']}
• Degré moyen: {results['avg_degree']:.2f}

DÉTAILS DES DEGRÉS PAR SOMMET:
"""
        
        for vertex, degree in results['degrees'].items():
            output += f"• Sommet {vertex}: degré {degree}\n"
        
        if results['loops']:
            output += f"\nBOUCLES DÉTECTÉES:\n"
            for loop in results['loops']:
                output += f"• Boucle sur le sommet {loop}\n"
        
        output += f"""
PROPRIÉTÉS TOPOLOGIQUES:
• Graphe connexe: {'Oui' if results['is_connected'] else 'Non'}
• Nombre de composantes connexes: {results['nb_components']}
        """
        
        self.results_text.insert(tk.END, output)
    
    def visualize_graph(self):
        """Visualise le graphe"""
        self.ax.clear()
        
        if self.current_graph is None:
            return
        
        # Créer le graphe NetworkX
        G = nx.Graph() if not self.analyzer.is_directed else nx.DiGraph()
        
        # Ajouter les nœuds et arêtes
        for node in self.current_graph:
            G.add_node(node)
        
        for node in self.current_graph:
            for neighbor in self.current_graph[node]:
                G.add_edge(node, neighbor)
        
        # Calculer la disposition
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Dessiner le graphe
        nx.draw(G, pos, ax=self.ax, with_labels=True, 
                node_color='lightblue', node_size=500, 
                font_size=10, font_weight='bold',
                edge_color='gray', arrows=self.analyzer.is_directed)
        
        # Dessiner les boucles séparément
        loops = [(n, n) for n in G.nodes() if G.has_edge(n, n)]
        if loops:
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(n, n): '↻' for n, n in loops})
        
        self.ax.set_title("Visualisation du Graphe", fontsize=12, fontweight='bold')
        self.canvas.draw()
    
    def generate_report(self):
        """Génère le rapport HTML"""
        if self.current_graph is None:
            messagebox.showwarning("Attention", "Veuillez d'abord analyser un graphe!")
            return
        
        try:
            results = self.analyzer.analyze_graph()
            filename = filedialog.asksaveasfilename(
                title="Enregistrer le rapport",
                defaultextension=".html",
                filetypes=[("Fichiers HTML", "*.html")]
            )
            
            if filename:
                self.report_gen.generate_report(results, self.analyzer, filename)
                messagebox.showinfo("Succès", f"Rapport généré: {filename}")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération: {str(e)}")

def main():
    root = tk.Tk()
    app = GraphAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
