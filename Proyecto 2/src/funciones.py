
players = {}
def update_scores(round_data):
    round_scores = {}  
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


#funcion de armado de tabla
def print_ranking(ranking, round_number): 
    print(f"Ranking ronda {round_number}:")
    print("Jugador    Kills  Asistencias  Muertes  MVPs  Puntos")
    print("-" * 50)
    for player, stats in ranking: 
        print(f"{player:<10} {stats['kills']:<6} {stats['assists']:<11} {stats['deaths']:<7} {stats['mvps']:<4} {stats['points']:<6}") 
    print("-" * 50, "\n")
