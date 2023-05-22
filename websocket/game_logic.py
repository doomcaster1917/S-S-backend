def define_winner(game_choices: list):
    player_one = game_choices[0]
    player_two = game_choices[1]

    if player_one['choice'] == player_two['choice']:
        return 'Draw'

    win_cases = [{'stone': 'scissors'}, {'scissors': 'paper'}, {'paper': 'stone'}]
    lose_cases = [{'stone': 'paper'}, {'scissors': 'stone'}, {'paper': 'scissors'}]
    for case in win_cases:

        if {player_one['choice']:player_two['choice']} == case:
            for player in [player_one, player_two]:
                if case == player['choice']:
                    print(player['user_id'])

    for case in lose_cases:

       if {player_one['choice']:player_two['choice']} == case:
            for player in [player_one, player_two]:
               if [key for key in case.keys()][0] == player['choice']:
                    game_choices.remove(player)
                    print(game_choices[0]['user_id'])

