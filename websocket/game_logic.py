def define_winner(game_choices: list):
    print(game_choices)
    player_one = game_choices[0]
    player_two = game_choices[1]

    if player_one['choice'] == player_two['choice']:
        return 'draw'

    win_cases = [{'stone': 'scissors'}, {'scissors': 'paper'}, {'paper': 'stone'}]
    lose_cases = [{'stone': 'paper'}, {'scissors': 'stone'}, {'paper': 'scissors'}]
    for case in win_cases:

        if {player_one['choice']:player_two['choice']} == case:
            for winner in [player_one, player_two]:
                if [key for key in case.keys()][0] == winner['choice']:
                    game_choices.remove(winner)
                    looser = game_choices[0]
                    return {'winner_id': winner['user_id'], 'winner_choice': winner['choice'], 'looser_choice': looser['choice']}

    for case in lose_cases:

       if {player_one['choice']:player_two['choice']} == case:
            for player in [player_one, player_two]:
               if [key for key in case.keys()][0] == player['choice']:
                    game_choices.remove(player)
                    winner = game_choices[0]
                    looser_choice = player['choice']
                    return {'winner_id': winner['user_id'], 'winner_choice': winner['choice'], 'looser_choice': looser_choice}

