"""
Module Core pour l'Analyse de Graphes
Université de Yaoundé I - Département d'Informatique

Ce module contient la logique principale pour l'analyse des graphes,
incluant le calcul des degrés, la détection des boucles et l'analyse topologique.
"""

import numpy as np
from collections import defaultdict, deque

class GraphAnalyzer:
    def __init__(self):
        self.graph = None
        self.is_directed = False
        self.adjacency_matrix = None
        self.vertices = []
    
    def from_adjacency_matrix(self, matrix_str):
        """
        Charge un graphe à partir d'une matrice d'adjacence
        
        Args:
            matrix_str (str): Représentation textuelle de la matrice
            
        Returns:
            dict: Graphe sous forme de liste d'adjacence
        """
        lines = [line.strip() for line in matrix_str.strip().split('\n') if line.strip()]
        
        # Convertir en matrice numpy
        matrix = []
        for line in lines:
            row = [int(x) for x in line.split()]
            matrix.append(row)
        
        self.adjacency_matrix = np.array(matrix)
        n = len(self.adjacency_matrix)
        
        # Vérifier si c'est un graphe orienté
        self.is_directed = not np.array_equal(self.adjacency_matrix, self.adjacency_matrix.T)
        
        # Créer la liste d'adjacence
        self.graph = defaultdict(list)
        self.vertices = list(range(n))
        
        for i in range(n):
            for j in range(n):
                if self.adjacency_matrix[i][j] > 0:
                    # Gérer les arêtes multiples
                    for _ in range(self.adjacency_matrix[i][j]):
                        self.graph[i].append(j)
        
        return self.graph
    
    def from_adjacency_list(self, list_str):
        """
        Charge un graphe à partir d'une liste d'adjacence
        
        Args:
            list_str (str): Représentation textuelle de la liste
            
        Returns:
            dict: Graphe sous forme de liste d'adjacence
        """
        lines = [line.strip() for line in list_str.strip().split('\n') if line.strip()]
        
        self.graph = defaultdict(list)
        vertices_set = set()
        
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                vertex = int(parts[0].strip())
                vertices_set.add(vertex)
                
                if len(parts) > 1 and parts[1].strip():
                    neighbors = [int(x.strip()) for x in parts[1].strip().split()]
                    for neighbor in neighbors:
                        vertices_set.add(neighbor)
                        self.graph[vertex].append(neighbor)
        
        # Déterminer tous les sommets
        self.vertices = sorted(list(vertices_set))
        
        # S'assurer que tous les sommets existent dans le graphe
        for vertex in self.vertices:
            if vertex not in self.graph:
                self.graph[vertex] = []
        
        # Déterminer si le graphe est orienté
        self.is_directed = self._check_if_directed()
        
        return self.graph
    
    def _check_if_directed(self):
        """Vérifie si le graphe est orienté"""
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                if vertex not in self.graph[neighbor]:
                    return True
        return False
    
    def calculate_degrees(self):
        """
        Calcule les degrés de tous les sommets
        
        Returns:
            dict: Dictionnaire des degrés par sommet
        """
        degrees = {}
        
        if self.is_directed:
            # Pour un graphe orienté, calculer degré entrant + sortant
            in_degrees = defaultdict(int)
            out_degrees = defaultdict(int)
            
            for vertex in self.vertices:
                out_degrees[vertex] = len(self.graph[vertex])
            
            for vertex in self.graph:
                for neighbor in self.graph[vertex]:
                    in_degrees[neighbor] += 1
            
            for vertex in self.vertices:
                degrees[vertex] = in_degrees[vertex] + out_degrees[vertex]
        else:
            # Pour un graphe non-orienté
            for vertex in self.vertices:
                degree = len(self.graph[vertex])
                # Compter les boucles deux fois
                degree += sum(1 for neighbor in self.graph[vertex] if neighbor == vertex)
                degrees[vertex] = degree
        
        return degrees
    
    def find_loops(self):
        """
        Trouve toutes les boucles dans le graphe
        
        Returns:
            list: Liste des sommets ayant des boucles
        """
        loops = []
        for vertex in self.graph:
            if vertex in self.graph[vertex]:
                loops.append(vertex)
        return loops
    
    def is_connected(self):
        """
        Vérifie si le graphe est connexe (pour graphe non-orienté)
        ou fortement connexe (pour graphe orienté)
        
        Returns:
            bool: True si connexe, False sinon
        """
        if not self.vertices:
            return True
        
        if self.is_directed:
            return self._is_strongly_connected()
        else:
            return self._is_weakly_connected()
    
    def _is_weakly_connected(self):
        """Vérifie la connexité faible (graphe non-orienté)"""
        visited = set()
        queue = deque([self.vertices[0]])
        visited.add(self.vertices[0])
        
        while queue:
            vertex = queue.popleft()
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.vertices)
    
    def _is_strongly_connected(self):
        """Vérifie la connexité forte (graphe orienté)"""
        # Algorithme simple pour petits graphes
        for start_vertex in self.vertices:
            visited = set()
            queue = deque([start_vertex])
            visited.add(start_vertex)
            
            while queue:
                vertex = queue.popleft()
                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            if len(visited) != len(self.vertices):
                return False
        
        return True
    
    def count_components(self):
        """
        Compte le nombre de composantes connexes
        
        Returns:
            int: Nombre de composantes connexes
        """
        visited = set()
        components = 0
        
        for vertex in self.vertices:
            if vertex not in visited:
                components += 1
                # BFS pour marquer tous les sommets de cette composante
                queue = deque([vertex])
                visited.add(vertex)
                
                while queue:
                    current = queue.popleft()
                    for neighbor in self.graph[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                    
                    # Pour graphe non-orienté, vérifier aussi les arêtes inverses
                    if not self.is_directed:
                        for other_vertex in self.vertices:
                            if current in self.graph[other_vertex] and other_vertex not in visited:
                                visited.add(other_vertex)
                                queue.append(other_vertex)
        
        return components
    
    def analyze_graph(self):
        """
        Effectue une analyse complète du graphe
        
        Returns:
            dict: Résultats de l'analyse
        """
        if self.graph is None:
            raise ValueError("Aucun graphe chargé")
        
        degrees = self.calculate_degrees()
        loops = self.find_loops()
        
        # Calculer les statistiques des degrés
        degree_values = list(degrees.values())
        min_degree = min(degree_values) if degree_values else 0
        max_degree = max(degree_values) if degree_values else 0
        avg_degree = sum(degree_values) / len(degree_values) if degree_values else 0
        
        # Compter les arêtes
        if self.is_directed:
            nb_edges = sum(len(neighbors) for neighbors in self.graph.values())
        else:
            # Pour graphe non-orienté, chaque arête est comptée deux fois
            nb_edges = sum(len(neighbors) for neighbors in self.graph.values()) // 2
            # Ajouter les boucles (comptées une seule fois)
            nb_edges += len(loops)
        
        return {
            'nb_vertices': len(self.vertices),
            'nb_edges': nb_edges,
            'is_directed': self.is_directed,
            'degrees': degrees,
            'min_degree': min_degree,
            'max_degree': max_degree,
            'avg_degree': avg_degree,
            'loops': loops,
            'has_loops': len(loops) > 0,
            'is_connected': self.is_connected(),
            'nb_components': self.count_components()
        }
    
    def get_adjacency_matrix(self):
        """
        Retourne la matrice d'adjacence
        
        Returns:
            numpy.ndarray: Matrice d'adjacence
        """
        if self.adjacency_matrix is not None:
            return self.adjacency_matrix
        
        # Construire la matrice à partir de la liste d'adjacence
        n = len(self.vertices)
        matrix = np.zeros((n, n), dtype=int)
        
        vertex_to_index = {v: i for i, v in enumerate(self.vertices)}
        
        for vertex in self.graph:
            i = vertex_to_index[vertex]
            for neighbor in self.graph[vertex]:
                j = vertex_to_index[neighbor]
                matrix[i][j] += 1
        
        self.adjacency_matrix = matrix
        return matrix
    
    def get_graph_representation(self):
        """
        Retourne les représentations du graphe
        
        Returns:
            tuple: (matrice d'adjacence, liste d'adjacence)
        """
        matrix = self.get_adjacency_matrix()
        adj_list = dict(self.graph)
        
        return matrix, adj_list
