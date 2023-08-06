import sys
sys.path.append("../")
from datetime import datetime

from chessdotcom.client import *
from chessdotcom import ChessDotComResponse

def test_endpoints(print_ = False, break_ = False):

    Client.config['headers']['user-agent'] = 'chess.com wrapper testing scripts. Contact me at saradzhyanartur@gmail.com'

    data = get_player_profile("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_titled_players("GM")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_stats("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = is_player_online("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_current_games("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_current_games_to_move("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_game_archives("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data =get_player_games_by_month(username = "fabianocaruana", year='2020', month='05')
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_games_by_month_pgn(username = "fabianocaruana", year='2020', month='05')
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_clubs("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_team_matches("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_player_tournaments("fabianocaruana")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_club_details("chess-com-developer-community")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_club_members("chess-com-developer-community")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_club_matches("chess-com-developer-community")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_tournament_details("-33rd-chesscom-quick-knockouts-1401-1600")
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_tournament_round("-33rd-chesscom-quick-knockouts-1401-1600", 1)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_tournament_round_group_details("-33rd-chesscom-quick-knockouts-1401-1600", 1, 1)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_team_match(12803)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_team_match_board(12803, 1)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()
    
    data = get_team_match_live(5833)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()
    
    data = get_team_match_live_board(5833, 1)
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()
    
    data = get_country_details('XE')
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_country_players('XE')
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_country_clubs('XE')
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()
  
    data = get_current_daily_puzzle()
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_random_daily_puzzle()
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_streamers()
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()

    data = get_leaderboards()
    assert(isinstance(data, ChessDotComResponse))
    print(data.__dict__.keys())
    assert(len(data.__dict__.keys()) == 3)
    if print_:
        print(data)
    if break_:
        input()
    

if __name__ == "__main__":
    start = datetime.now()
    test_endpoints()
    end = datetime.now()
    print(end - start)