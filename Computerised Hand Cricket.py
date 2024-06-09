import random
from math import floor
print('''Welcome to Hand Cricket.
You have to write the playing XI for both the teams and the computer will play the game.
When you are writing the name of an all-rounder or bowler, write "(b)" AFTER their name.
When you are writing the name of the captain, write "(c)" AFTER their name.
When you are writing the name of the wicketkeeper, write "(wk)" AFTER their name.
The 3 specifications can be written in any order.
''')

class Player():
  def __init__(self, name):
    self.name = name
    self.bat_runs = self.bat_balls = self.bowl_runs = self.bowl_balls = 0
    self.wickets = 0
    self.did_bat = False
    self.dismissal = "not out"

#creating CricketTeam to store all info related to the team
class CricketTeam():
  def __init__(self, name):
    self.name = name
    self.playing_xi = []
    self.bowlers = []
    self.wickets_lost = self.score = self.balls_played = 0
  
  def initialiseTeam(self):
    for _ in range(11):
      player = Player(input(f"Enter a player's name for {self.name}: ").strip(" "))

      if "(c)" in player.name or "(c)" in player.name:
        player.name = player.name.replace("(c)", "")
        player.name = player.name.replace("(C)", "")
        self.captain = player
      
      if "(WK)" in player.name or "(wk)" in player.name:
        player.name = player.name.replace("(WK)", "")
        player.name = player.name.replace("(wk)", "")
        self.wk = player
      
      if "(b)" in player.name or "(B)" in player.name:
        player.name = player.name.replace("(b)", "")
        player.name = player.name.replace("(B)", "")
        self.bowlers.append(player)
      
      self.playing_xi.append(player)

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
  for _ in bat_partners:
    _.did_bat = True

  available_batters = batting_side.playing_xi[2: ]

  bowling_order = createBowlingOrder(bowling_side.bowlers)

  while batting_side.balls_played < 60:
    #playing an over
    for _ in range(6):
      batter_on_strike = bat_partners[0]
      bowler = bowling_order[0]

      bat_number = random.choice(numbers)
      bowl_number = random.choice(numbers)
      batter_on_strike.bat_balls += 1 #incrementing the ball already
      bowler.bowl_balls += 1
      batting_side.balls_played += 1

      if bat_number == bowl_number: #wicket
        batting_side.wickets_lost += 1
        dismissal = common_dismissal_types[floor(random.triangular(0, 2, 0))]
        bowler.wickets += 1
        bat_partners.remove(batter_on_strike)

        if dismissal == 'c X b Y':
          catcher = random.choice(bowling_side.playing_xi)
          if catcher == bowler:
            dismissal = f'c & b {bowler.name}'

          else:
            dismissal = f'c {catcher.name}  b {bowler.name}'

        elif dismissal == 'b':
          dismissal = f'b {bowler.name}'

        elif dismissal == 'lbw':
          dismissal = f'lbw {bowler.name}'
          
        batter_on_strike.dismissal = dismissal

      else: #not a wicket
        runs_scored = scoreCounting(bat_number, bowl_number)
        batter_on_strike.bat_runs += runs_scored
        batting_side.score += runs_scored
        bowler.bowl_runs += runs_scored

        if runs_scored % 2 == 1:
          bat_partners.reverse()
      
      if chasing:
        if batting_side.score >= target: #chased the target
          result = f"{batting_side.name} beat {bowling_side.name} by {10 - batting_side.wickets_lost} wickets."
          return result

      if batting_side.wickets_lost == 10: #all out
        if not chasing: #first batting
          return batting_side.score + 1   #target
        
        elif chasing: #couldn't chase the target and got all out
          if batting_side.score < target - 1: #lesser runs than opponent
            result = f"{bowling_side.name} beat {batting_side.name} by {target - 1 - batting_side.score} runs."
          
          elif batting_side.score == target - 1: #same runs as the opponent
            result = "Match drawn."

          return result

        break

      if len(bat_partners) == 1:
        new_batter = available_batters.pop(0)
        bat_partners.insert(0, new_batter)
        new_batter.did_bat = True

    bat_partners.reverse() #the over concluded so the strike switches
    bowling_order.pop(0) #next bowler will be upfront

  else: #didn't get all out
    if not chasing:
      return batting_side.score + 1 #target
    
    elif chasing: #couldn't chase and didn't get all out
      if batting_side.score < target - 1:
        result = f"{bowling_side.name} beat {batting_side.name} by {target - 1 - batting_side.score} runs."

      elif batting_side.score == target - 1:
        result = "Match drawn."

      return result

defending_team = toss_dict['bat']
chasing_team = toss_dict['bowl']
target = batting(defending_team, chasing_team, False)
result = batting(chasing_team, defending_team, True, target)

def createScorecard(batting_side: CricketTeam, bowling_side: CricketTeam):
  scorecard = f"{batting_side.name} - {batting_side.score}/{batting_side.wickets_lost} ({batting_side.balls_played//6}.{batting_side.balls_played%6} overs):"
  for batter in batting_side.playing_xi:
    if batter.did_bat:
      name = batter.name
      batter_score = f"{batter.bat_runs}({batter.bat_balls})"
      if batter.dismissal == "not out":
        name += '* '
    
      if batter == batting_side.captain:
        name += "(c)"

      if batter == batting_side.wk:
        name += "(wk)"

      scorecard += f'\n{name:<25}{batter.dismissal:<50}{batter_score:>5}'

  scorecard += f'\n\n{bowling_side.name} bowling:'
  for bowler in bowling_side.bowlers:
    name = bowler.name
    overs = f'{bowler.bowl_balls // 6}.{bowler.bowl_balls % 6} overs'
    figures = f'{bowler.wickets}-{bowler.bowl_runs}'
    if bowler == bowling_side.captain:
      name += '(c)'

    if bowler.bowl_balls != 0:
      scorecard += f'\n{name:<25}{figures} ({overs})'

  print(scorecard, '\n\n')

print('\n\n')
print(toss_statement)
print("Result:", result, '\n')
createScorecard(defending_team, chasing_team)
createScorecard(chasing_team, defending_team)
