import random
from math import floor
print('''Welcome to Hand Cricket.
You have to write the playing XI for both the teams and the computer will play the game.
When you are writing the name of an all-rounder or bowler, please write "(b)" AFTER their name.
However, when you are writing the captain name, DO NOT write "(b)"!!
''')


#creating CricketTeam to store all info related to the team
class CricketTeam():
  def __init__(self, name):
    self.name = name
    self.playing_xi = []
    self.bowlers = []
    self.captain = None
    self.wk = None
  
  def initialiseTeam(self):
    for _ in range(11):
      player_name = input(f"Enter a player's name for {self.name}: ").strip(" ")

      if "(b)" in player_name or "(B)" in player_name:
        player_name = player_name.removesuffix("(b)")
        player_name = player_name.removesuffix("(B)")
        self.bowlers.append(player_name)
      
      self.playing_xi.append(player_name)
    
    self.captain = input(f"Enter the captain for {self.name}: ")
    self.wk = input(f"Enter the wicketkeeper for {self.name}: ")

#accepting two teams
home_team = CricketTeam(input("Enter the home team: ").strip(" "))
home_team.initialiseTeam()
print()
away_team = CricketTeam(input("Enter the away team: ").strip(" "))
away_team.initialiseTeam()

#toss
toss_options = ('H', 'T')
toss_call = random.choice(toss_options)
coin_land = random.choice(toss_options)
elect_options = ["bat", "bowl"]
elect = random.choice(elect_options)

if toss_call == coin_land:
  toss_winner = away_team
  toss_loser = home_team
  
else:
  toss_winner = home_team
  toss_loser = away_team

toss_statement = f"Toss: {toss_winner.name} won the toss and elected to {elect} first."
toss_dict = {elect: toss_winner}
elect_options.remove(elect)
toss_dict.update({elect_options[0]: toss_loser})

numbers = (0, 1, 2, 3, 4, 6)
#defining scoring_counting
def scoreCounting(bat_number: int, bowl_number: int):
  if bat_number == 0:
    return bowl_number
  
  elif bowl_number == 0:
    return bat_number
  
  elif abs(bat_number - bowl_number) == 1:
    return 0
  
  elif set((bat_number, bowl_number)) == {4, 6}:
    return 0
  
  else:
    return bat_number

#New update - dismissal mode :)
common_dismissal_types = ('c X b Y', 'b', 'lbw')

#defining bowling order - to ensure no bowler bowls more than 2 overs, no consec. overs
def createBowlingOrder(bowler_list: list):
  if len(bowler_list) == 5:
    bowling_order = []
    num_bowlers = len(bowler_list)

    # Calculate total overs
    total_overs = 4 * num_bowlers

    # Initialize two lists to alternate bowlers
    current_bowlers = bowler_list.copy()
    next_bowlers = []

    for _ in range(total_overs):
      # Select bowler from current list
      bowler = current_bowlers.pop(0)
      bowling_order.append(bowler)

      # Add bowler to next bowlers list (won't bowl consecutively)
      next_bowlers.append(bowler)

      # If enough overs bowled, switch bowler lists
      if len(current_bowlers) == 0:
        current_bowlers = next_bowlers.copy()
        next_bowlers = []


  if len(bowler_list) > 5:
    bowling_order = []
    possible_bowlers = bowler_list.copy()
    overs_dict = {i:0 for i in bowler_list}
    next_over = possible_bowlers.copy()

    for _ in range(20):
      bowler = random.choice(next_over)
      bowling_order.append(bowler)
      overs_dict[bowler] += 1

      if overs_dict[bowler] == 4:
        possible_bowlers.remove(bowler)

      next_over = possible_bowlers.copy()
      if bowler in next_over:
        next_over.remove(bowler)

  return bowling_order

#defining batting
def batting(batting_side: CricketTeam, bowling_side: CricketTeam, chasing: bool, target: int | None = None):
  bat_partners = [batting_side.playing_xi[0], batting_side.playing_xi[1]]
  available_batters = batting_side.playing_xi[2: ]
  batter_runs = {}.fromkeys(bat_partners, 0)
  batter_balls = {}.fromkeys(bat_partners, 0)
  batter_dismissals = {}

  bowling_order = createBowlingOrder(bowling_side.bowlers)
  bowler_wickets = {}.fromkeys(bowling_side.bowlers, 0)
  bowler_runs = {}.fromkeys(bowling_side.bowlers, 0)
  bowler_balls = {}.fromkeys(bowling_side.bowlers, 0)

  balls_played = team_score = wickets_lost = 0

  def createScorecard():
    scorecard = f"{batting_side.name} - {team_score}/{wickets_lost} ({balls_played//6}.{balls_played%6} overs):"
    for batter in batter_runs:
      name = batter
      batter_score = f"{batter_runs[batter]}({batter_balls[batter]})"
      if batter in bat_partners:
        name += '* '
      
      if batter == batting_side.captain:
        name += "(c)"

      if batter == batting_side.wk:
        name += "(wk)"

      if batter in batter_dismissals:
        scorecard += f'\n{name:<25}{batter_dismissals[batter]:<40}{batter_score:>5}'

      else:
        dismissal = 'not out'
        scorecard += f'\n{name:<25}{dismissal:<40}{batter_score:>5}'

    
    scorecard += f'\n\n{bowling_side.name} bowling:'
    for bowler in bowler_wickets:
      name = bowler
      overs = f'{bowler_balls[bowler] // 6}.{bowler_balls[bowler] % 6} overs'
      figures = f'{bowler_wickets[bowler]}-{bowler_runs[bowler]}'
      if bowler == bowling_side.captain:
        name += '(c)'

      if bowler_balls[bowler] != 0:
        scorecard += f'\n{name:<25}{figures} ({overs})'

    return scorecard

  while balls_played < 60:
    #playing an over
    for _ in range(6):
      batter_on_strike = bat_partners[0]
      bowler = bowling_order[0]

      bat_number = random.choice(numbers)
      bowl_number = random.choice(numbers)
      batter_balls[batter_on_strike] += 1 #incrementing the ball already
      bowler_balls[bowler] += 1
      balls_played += 1

      if bat_number == bowl_number: #wicket
        wickets_lost += 1
        dismissal = common_dismissal_types[floor(random.triangular(0, 2, 0))]
        bowler_wickets[bowler] += 1
        bat_partners.remove(batter_on_strike)

        if dismissal == 'c X b Y':
          catcher = random.choice(bowling_side.playing_xi)
          if catcher == bowler:
            dismissal = f'c & b {bowler}'

          else:
            dismissal = f'c {catcher}  b {bowler}'

        elif dismissal == 'b':
          dismissal = f'b {bowler}'

        elif dismissal == 'lbw':
          dismissal = f'lbw {bowler}'
          
        batter_dismissals[batter_on_strike] = dismissal

      else: #not a wicket
        runs_scored = scoreCounting(bat_number, bowl_number)
        batter_runs[batter_on_strike] += runs_scored
        team_score += runs_scored
        bowler_runs[bowler] += runs_scored

        if runs_scored % 2 == 1:
          bat_partners.reverse()
      
      if chasing:
        if team_score >= target: #chased the target
          result = f"{batting_side.name} beat {bowling_side.name} by {10 - wickets_lost} wickets."
          scorecard = createScorecard()
          return result, scorecard

      if wickets_lost == 10: #all out
        if not chasing: #first batting
          scorecard = createScorecard()
          return team_score + 1, scorecard   #target
        
        elif chasing: #couldn't chase the target and got all out
          if team_score < target - 1:
            scorecard = createScorecard()     
            result = f"{bowling_side.name} beat {batting_side.name} by {target - 1 - team_score} runs."
          
          elif team_score == target - 1:
            scorecard = createScorecard()
            result = "Match drawn."

          return result, scorecard

        break

      if len(bat_partners) == 1:
        new_batter = available_batters[0]
        available_batters.pop(0)
        bat_partners.insert(0, new_batter)
        batter_runs[new_batter] = batter_balls[new_batter] = 0

    bat_partners.reverse() #the over concluded so the strike switches
    bowling_order.pop(0) #next bowler will be upfront

  else: #didn't get all out
    if not chasing:
      scorecard = createScorecard()
      return team_score + 1, scorecard
    
    elif chasing: #couldn't chase and didn't get all out
      if team_score < target - 1:
        result = f"{bowling_side.name} beat {batting_side.name} by {target - 1 - team_score} runs."
        scorecard = createScorecard()
      
      elif team_score == target - 1:
        result = "Match drawn."
        scorecard = createScorecard()
        
      return result, scorecard

defending_team = toss_dict['bat']
chasing_team = toss_dict['bowl']
target, first_scorecard = batting(defending_team, chasing_team, False)
result, second_scorecard = batting(chasing_team, defending_team, True, target)

print('\n\n')
print(toss_statement)
print("Result:", result, '\n')
print(first_scorecard, '\n\n')
print(second_scorecard)
