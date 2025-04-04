
players = {}
round_scores = {}
def update_scores(round_data):
    """
    Esta funcion actualiza las puntuaciones de los jugadores basándose en los datos de la ronda.

    Args:
        round_data (dict): Un diccionario donde las claves son los nombres de los jugadores y los valores son diccionarios que contienen estadísticas de la ronda. 

    Returns:
        list: Una lista de tuplas que contienen el nombre del jugador y sus estadísticas acumuladas, ordenada por puntos en orden descendente.
    
    """
    for player, stats in round_data.items(): 
        kills, assists, death = stats['kills'], stats['assists'], stats['deaths']
        points = kills * 3 + assists * 1 - (1 if death else 0)  
        
        if player not in players: 
            players[player] = {'kills': 0, 'assists': 0, 'deaths': 0, 'points': 0, 'mvps': 0}
        
        players[player]['kills'] += kills 
        players[player]['assists'] += assists  
        players[player]['deaths'] += 1 if death else 0
        players[player]['points'] += points
        round_scores[player] = points
    
    mvp = max(round_scores, key=round_scores.get) 
    players[mvp]['mvps'] += 1 
    
    return sorted(players.items(), key=lambda x: x[1]['points'], reverse=True) 



def print_ranking(ranking, round_number): 
    """
    Esta funcion Imprime el ranking de jugadores para una ronda específica."
    Args:
        ranking (lista de tuplas): cada tupla contiene el nombre del jugador  y un diccionario con sus estadísticas.
        
        round_number (int): Número de la ronda actual.
    Returns:
       none: Esta función imprime el ranking directamente en la consola.
    """
    print(f"Ranking ronda {round_number}:")
    print("Jugador    Kills  Asistencias  Muertes  MVPs  Puntos")
    print("-" * 50)
    for player, stats in ranking: 
        print(f"{player:<10} {stats['kills']:<6} {stats['assists']:<11} {stats['deaths']:<7} {stats['mvps']:<4} {stats['points']:<6}") 
    print("-" * 50, "\n")

