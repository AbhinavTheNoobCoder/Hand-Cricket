import random
print('''Welcome to Hand Cricket.
You have to write the playing XI for both the teams and the computer will play the game.
When you are writing the name of an all-rounder or bowler, please write "(b)" AFTER their name.
However, when you are writing the captain name, DO NOT write "(b)"!!
''')

class CricketTeam():
  def __init__(self, name):
    self.name = name.strip(" ")
    self.roster = list()
    self.captain = self.wicketkeeper = None
    self.bowling_options = []
  
  def initialiseTeam(self):
    for _ in range(11):
      member = input(f"Enter a player name for {self.name}: ").strip(" ")
      
      if "(b)" in member or "(B)" in member:
        member = member[0: -3].strip(" ")
        self.bowling_options.append(member)

      self.roster.append(member)

    cap = input(f"Enter captain name for {self.name}: ").strip(" ")
    keeper = input(f"Enter wicketkeeper name for {self.name}: ").strip(" ")
    self.captain, self.wicketkeeper = cap, keeper


player_team = CricketTeam(input("Enter first team's name: "))
player_team.initialiseTeam()
print("\n")
computer_team = CricketTeam(input("Enter second team's name: "))
computer_team.initialiseTeam()
print("\n")

numbers = (0, 1, 2, 3, 4, 6)
number_dict = {0: "Dot ball.", 1: "1 run.", 2: "2 runs.", 3: "3 runs.", 4: "FOUR!", 6: "The ball clears the fence for a SIX!"}
def scoreCounting(n1, n2):
  if n1 == 0:
    return n2
  
  elif n2 == 0:
    return n1
  
  elif abs(n1-n2) == 1:
    return 0
  
  elif abs(n1-n2) == 2:
    if set([n1, n2]) == {4, 6}:
      return 0
    else:
      return n1
  
  else:
    return n1

def toss():
  toss_options = ["Heads", "Tails"]
  elect_options = ["bat", "bowl"]

  team1_call = random.choice(toss_options)
  toss_options.remove(team1_call)
  team2_call = toss_options[0]
  toss_options.append(team1_call)

  coin_land = random.choice(toss_options)
  if team1_call == coin_land:
    toss_winner = player_team
    toss_loser = computer_team

  else:
    toss_winner = computer_team
    toss_loser = player_team

  elect = random.choice(elect_options)
  elect_options.remove(elect)

  elect_dict = {elect : toss_winner, elect_options[0] : toss_loser}
  toss_statement = f"{toss_winner.name} won the toss and elected to {elect} first."

  return elect_dict, toss_statement

result_of_toss, toss_statement = toss()

def handCricket():
  team1 = result_of_toss["bat"]
  team2 = result_of_toss["bowl"]

  team1_score = team2_score = 0
  
  team1_available_batsmen = team1.roster.copy()
  team2_available_batsmen = team2.roster.copy()

  team1_available_bowlers = team1.bowling_options.copy()
  team2_available_bowlers = team2.bowling_options.copy()

  team1_nextover = team1_available_bowlers.copy()
  team2_nextover = team2_available_bowlers.copy()

  team1_wickets = team2_wickets = 0

  team1_individual_runs = {}
  team1_individual_balls = {}

  team2_individual_runs = {}
  team2_individual_balls = {}

  team1_individual_wickets = {}.fromkeys(team1_available_bowlers, 0)
  team1_individual_overs = {}.fromkeys(team1_available_bowlers, 0)

  team2_individual_wickets = {}.fromkeys(team2_available_bowlers, 0)
  team2_individual_overs = {}.fromkeys(team2_available_bowlers, 0)

  team1_bowler_runs = {}.fromkeys(team1_available_bowlers, 0)
  team2_bowler_runs = {}.fromkeys(team2_available_bowlers, 0)

  team1_currentbat = []
  team2_currentbat = []

  team1_balls = team2_balls = 0
  
  while team1_wickets < 10 and team1_balls != 60: #First batting - 10 overs are not complete and team is not all-out

    bowlers_list = team2_nextover
    bowler = random.choice(bowlers_list)

    for bowling in team2_individual_overs:
      if team2_individual_overs[bowling] == 2: #2 overs bowled by the bowler
        team2_available_bowlers.remove(bowling) if bowling in team2_available_bowlers else "" #bowler may no more bowl
        team2_nextover.remove(bowling) if bowling in team2_nextover else ""

    balls_bowled_in_over = 0 #initiating an over
    while balls_bowled_in_over < 6: #over is initiated

      if len(team1_currentbat) < 2: #2 batsmen are not on the pitch yet
      
        if team1_wickets == 0: #finding openers
          team1_currentbat = team1_available_batsmen[:2] #First two available batsmen are picked up
          team1_individual_runs = {}.fromkeys(team1_currentbat, 0)
          team1_individual_balls = {}.fromkeys(team1_currentbat, 0)
          team1_available_batsmen = team1_available_batsmen[2: ] #from in at 3 till in at 11
        
        else: #at least 1 wicket is gone
          team1_currentbat.insert(0, team1_available_batsmen[0]) if team1_available_batsmen != [] else "" #first available batsman picked
          batsman = team1_available_batsmen.pop(0) #no more available
          team1_individual_runs[batsman] = 0
          team1_individual_balls[batsman] = 0
      

      batsman = team1_currentbat[0] #first person in current batsmen list is on strike

      bat_number = random.choice(numbers)
      bowl_number = random.choice(numbers)
      
      balls_bowled_in_over += 1 #add 1 ball to the over

      if bat_number == bowl_number: #WICKET
        runs_taken = 0
        team1_wickets += 1 #add 1 wicket to the team tally
        team1_currentbat.remove(batsman) #remove batsman from pitch
        team2_individual_wickets[bowler] += 1 #add wicket to bowler's name
        team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
      
      else: #Not a wicket
        runs_taken = scoreCounting(bat_number, bowl_number) #counting runs scored
        team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name


      if runs_taken%2 == 1 and balls_bowled_in_over != 6: #1 run taken and not the last ball of over
        team1_currentbat.reverse() #reverse the batsmen

      elif runs_taken%2 == 0 and balls_bowled_in_over == 6: #2 runs taken and last ball of the over
        team1_currentbat.reverse() #reverse the batsmen again

      team1_balls += 1
      team1_score += runs_taken #increment team score for runs taken in each ball
      

      if team1_wickets == 10: #all out within the over
        team2_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        break

    else: #over successfully completed
      team2_individual_overs[bowler] += 1 #add an over to the bowler's name

    team2_nextover = team2_available_bowlers.copy() #making changes to team2's next over bowlers
    team2_nextover.remove(bowler) if bowler in team2_nextover else "" #bowler cannot bowl 2 consecutive overs

  target = team1_score + 1
  team1_overs = f"{team1_balls//6}.{team1_balls%6}"

  while team2_wickets < 10 and team2_balls != 60:
    
    bowlers_list = team1_nextover
    bowler = random.choice(bowlers_list)

    for bowling in team1_individual_overs:
      if team1_individual_overs[bowling] == 2: #2 overs bowled by the bowler
        team1_available_bowlers.remove(bowling) if bowling in team1_available_bowlers else "" #bowler may no more bowl
        team1_nextover.remove(bowling) if bowling in team1_nextover else ""

    balls_bowled_in_over = 0 #initiating an over
    while balls_bowled_in_over < 6: #over is initiated

      if len(team2_currentbat) < 2: #2 batsmen are not on the pitch yet
      
        if team2_wickets == 0: #finding openers
          team2_currentbat = team2_available_batsmen[:2] #First two available batsmen are picked up 
          team2_individual_runs = {}.fromkeys(team2_currentbat, 0)
          team2_individual_balls = {}.fromkeys(team2_currentbat, 0)
          team2_available_batsmen = team2_available_batsmen[2: ] #from in at 3 till in at 11
        
        else: #at least 1 wicket is gone
          team2_currentbat.insert(0, team2_available_batsmen[0]) if team2_available_batsmen!=[] else "" #first available batsman picked
          batsman = team2_available_batsmen.pop(0) #no more available
          team2_individual_runs[batsman] = 0
          team2_individual_balls[batsman] = 0

      batsman = team2_currentbat[0] #first person in current batsmen list is on strike

      bat_number = random.choice(numbers)
      bowl_number = random.choice(numbers)
      
      balls_bowled_in_over += 1 #add 1 ball to the over

      if bat_number == bowl_number: #WICKET
        runs_taken = 0
        team2_wickets += 1 #add 1 wicket to the team tally
        team2_currentbat.remove(batsman) #remove batsman from pitch
        team1_individual_wickets[bowler] += 1 #add wicket to bowler's name
        team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
      
      else: #Not a wicket
        runs_taken = scoreCounting(bat_number, bowl_number) #counting runs scored
        team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
    

      if runs_taken%2 == 1 and balls_bowled_in_over != 6: #1 run taken and not the last ball of over
        team2_currentbat.reverse() #reverse the batsmen

      elif runs_taken%2 == 0 and balls_bowled_in_over == 6: #2 runs taken and last ball of the over
        team2_currentbat.reverse() #reverse the batsmen again

      team2_balls += 1
      team2_score += runs_taken #increment team score for runs taken in each ball
      

      if team2_score >= target:
        team2_overs = f"{team2_balls//6}.{balls_bowled_in_over}"
        team1_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        gameOver = True
        result = f"{team2.name} beat {team1.name} by {10 - team2_wickets} wickets."
        break

      if team2_wickets == 10: #all out within the over
        team1_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        team2_overs = f"{team2_balls//6}.{balls_bowled_in_over}"
        if team2_score == team1_score:
          gameOver = True
          result = "Game drawn."

        else:
          gameOver = True
          result = f"{team1.name} beat {team2.name} by {team1_score - team2_score} runs."
        
        break
      
      else:
        gameOver = False

    else: #over successfully completed
      team1_individual_overs[bowler] += 1 #add an over to the bowler's name

    team1_nextover = team1_available_bowlers.copy() #making changes to team2's next over bowlers
    team1_nextover.remove(bowler) if bowler in team1_nextover else "" #bowler cannot bowl 2 consecutive overs
    
    if gameOver:
      break
  
  else:
    if team2_score < team1_score:
      team2_overs = 10
      result = f"{team1.name} beat {team2.name} by {team1_score - team2_score} runs."
  
  print("Match report:\n")
  print(f"Toss: {toss_statement}")
  print(f"Result: {result}")
  print(f"{team1.name} - {team1_score}/{team1_wickets} ({team1_overs} overs):")
  for batter in team1_individual_runs:
    display_name = batter
    runs = team1_individual_runs[batter]
    balls = team1_individual_balls[batter]
    if batter == team1.captain:
      display_name += " (c)"
    if batter == team1.wicketkeeper:
      display_name += " (wk)"
    if batter in team1_currentbat:
      display_name += "*"
    spaces = " " * (35 - (len(display_name) + (len(str(runs)) + len(str(balls))) - 2))
    if batter not in team1_available_batsmen:
      print(f"{display_name}{spaces}{runs}({balls})")
    else:
      print(f"{batter} - DNB")
  print("\n")

  print(f"{team2.name} bowling:")
  for bowler in team2_individual_wickets:
    wickets = team2_individual_wickets[bowler]
    runs = team2_bowler_runs[bowler]
    overs = team2_individual_overs[bowler]
    performance = f"{wickets}-{runs} ({overs} overs)"
    if bowler == team2.captain:
      bowler += " (c)"
    spaces = " " * (40 - len(bowler) - len(performance))
    if overs != 0:
      print(f"{bowler}{spaces}{performance}")
  print("\n")
  
  print(f"{team2.name} - {team2_score}/{team2_wickets} ({team2_overs} overs):")
  for batter in team2_individual_runs:
    display_name = batter
    runs = team2_individual_runs[batter]
    balls = team2_individual_balls[batter]
    if batter == team2.captain:
      display_name += " (c)"
    if batter == team2.wicketkeeper:
      display_name += " (wk)"
    if batter in team2_currentbat:
      display_name += "*"
    spaces = " " * (35 - (len(display_name) + (len(str(runs)) + len(str(balls))) - 2))
    if batter not in team2_available_batsmen:
      print(f"{display_name}{spaces}{runs}({balls})")
    else:
      print(f"{batter} - DNB")
  print("\n")

  print(f"{team1.name} bowling:")
  for bowler in team1_individual_wickets:
    wickets = team1_individual_wickets[bowler]
    runs = team1_bowler_runs[bowler]
    overs = team1_individual_overs[bowler]
    performance = f"{wickets}-{runs} ({overs} overs)"
    if bowler == team1.captain:
      bowler += " (c)"
    spaces = " " * (40 - len(bowler) - len(performance))
    if overs != 0:
      print(f"{bowler}{spaces}{performance}")
  print("\n")

handCricket()
