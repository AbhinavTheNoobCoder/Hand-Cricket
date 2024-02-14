import random
print('''Welcome to Hand Cricket.
Please read the rules here:
http://tinyurl.com/handcricketrules
A gentle reminder that 5 is an illegal number. 4 and 6 are consecutive numbers.
''')

class GameForfeitError(Exception):
  pass

class CricketTeam():
  def __init__(self, name, roster):
    self.name = name.strip(" ")
    self.roster = list(roster)
    self.captain = self.wicketkeeper = None
  
  def initialiseTeam(self):
    for _ in range(11):
      member = input(f"Enter a player name for {self.name}: ").strip(" ")
      self.roster.append(member)
    
    cap = input(f"Enter captain name for {self.name}: ").strip(" ")
    keeper = input(f"Enter wicketkeeper name for {self.name}: ").strip(" ")
    self.captain, self.wicketkeeper = cap, keeper

player_team = CricketTeam(input("Enter YOUR team's name: "), [])
player_team.initialiseTeam()
print("\n")
computer_team = CricketTeam(input("Enter COMPUTER team's name: "), [])
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
  toss_options = ("H", "T")
  toss_dict = {"H": "Heads", "T": "Tails"}
  elect_dict = {"bat": None, "bowl": None}
  elect_options = ["bat", "bowl"]
  user_toss = input('''It is toss time.
Your call.
H for Heads and T for Tails.
>>> ''').upper().strip(" ")

  coin_landed_on = random.choice(toss_options)
  print(f"The coin landed on {toss_dict[coin_landed_on]}.")

  if user_toss != coin_landed_on:
    elect_choice = random.choice(elect_options)
    elect_dict[elect_choice] = computer_team
    elect_options.remove(elect_choice)
    elect_dict[elect_options[0]] = player_team
    print(f"{computer_team.name} won the toss and elected to {elect_choice} first.\n")
    toss_statement = f"{computer_team.name} won the toss and elected to {elect_choice} first."
  else:
    elect_choice = input(f"Choose what to do first from {elect_options}: ").lower().strip(" ")
    elect_dict[elect_choice] = player_team
    elect_options.remove(elect_choice)
    elect_dict[elect_options[0]] = computer_team
    print(f"{player_team.name} won the toss and elected to {elect_choice} first.\n")
    toss_statement = f"{player_team.name} won the toss and elected to {elect_choice} first."

  return elect_dict, toss_statement

result_of_toss, toss_statement = toss()

def handCricket():
  team1 = result_of_toss["bat"]
  team2 = result_of_toss["bowl"]
  team1_score = team2_score = 0
  team1_available_batsmen = team1.roster.copy()
  team2_available_batsmen = team2.roster.copy()

  team1_available_bowlers = team1.roster.copy()
  team1_available_bowlers.remove(team1.wicketkeeper)
  
  team2_available_bowlers = team2.roster.copy()
  team2_available_bowlers.remove(team2.wicketkeeper)

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

    if team2 == player_team: #player's team is bowling first
      print(f"{team2.name} can choose a bowler from {team2_nextover}: ")
      bowler = input("Enter a bowler name: ").strip(" ")
      team2_nextover.remove(bowler)

    else: #computer's team is bowling first
      bowlers_list = team2_nextover
      bowler = random.choice(bowlers_list)

    for bowling in team2_individual_overs:
      if team2_individual_overs[bowling] == 2: #2 overs bowled by the bowler
        team2_available_bowlers.remove(bowling) if bowling in team2_available_bowlers else "" #bowler may no more bowl
        team2_nextover.remove(bowling) if bowling in team2_nextover else ""

    balls_bowled_in_over = 0 #initiating an over
    while balls_bowled_in_over < 6: #over is initiated
      if len(team1_currentbat) < 2: #2 batsmen are not on the pitch yet
      
        if team1 == player_team: #player's team is batting first
          
          print(f"{team1.name}'s current available players are: {team1_available_batsmen}") #show available batsmen
          
          for _ in range(2 - len(team1_currentbat)): #vacancies on pitch
            batsman = input("Send a batsman: ").strip(" ")
            team1_individual_runs[batsman] = 0
            team1_individual_balls[batsman] = 0
            print(f"{batsman} comes out to bat.\n") if team1_wickets != 0 else ""
            team1_currentbat.insert(0, batsman) if team1_wickets != 0 else team1_currentbat.append(batsman) 
            team1_available_batsmen.remove(batsman) #sent batsmen cannot bat again

        else: #Computer's team is batting first
          if team1_wickets == 0: #finding openers
            team1_currentbat = team1_available_batsmen[:2] #First two available batsmen are picked up
            team1_individual_runs = {}.fromkeys(team1_currentbat, 0)
            team1_individual_balls = {}.fromkeys(team1_currentbat, 0)
            print(f"The openers are: {team1_currentbat}\n") 
            team1_available_batsmen = team1_available_batsmen[2: ] #from in at 3 till in at 11
          
          else: #at least 1 wicket is gone
            team1_currentbat.insert(0, team1_available_batsmen[0]) if team1_available_batsmen != [] else "" #first available batsman picked
            batsman = team1_available_batsmen.pop(0) #no more available
            print(f"{batsman} comes out to bat.\n")
            team1_individual_runs[batsman] = 0
            team1_individual_balls[batsman] = 0
      

      batsman = team1_currentbat[0] #first person in current batsmen list is on strike
      print(f"{bowler} bowling to {batsman}.\n")

      if team1 == player_team: #player's team batting first
        bat_number = int(input(f"Enter a number from {numbers}: "))
        bowl_number = random.choice(numbers)
      
      else: #computer's team batting first
        bat_number = random.choice(numbers)
        bowl_number = int(input(f"Enter a number from {numbers}: "))
      
      balls_bowled_in_over += 1 #add 1 ball to the over

      print(f'''\nBatsman put: {bat_number}, Bowler put: {bowl_number}''')
      if bat_number == bowl_number: #WICKET
        runs_taken = 0
        team1_wickets += 1 #add 1 wicket to the team tally
        team1_currentbat.remove(batsman) #remove batsman from pitch
        team2_individual_wickets[bowler] += 1 #add wicket to bowler's name
        team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
        print(f"WICKET! {batsman} {team1_individual_runs[batsman]}({team1_individual_balls[batsman]})\n")
      
      else: #Not a wicket or chance of an illegal delivery
        if (bat_number in numbers) and (bowl_number in numbers): #Both are valid numbers - legal ball
          runs_taken = scoreCounting(bat_number, bowl_number) #counting runs scored

          print(number_dict[runs_taken] + "\n") #print the statement related to those runs

          team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
          team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
          team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
        
        else: #illegal ball
          balls_bowled_in_over = balls_bowled_in_over - 1 #undo the 1 ball addition to the over
          print("\nInvalid number!")

          if bat_number not in numbers: #batsman put illegal number
            bat_number = int(input("Enter either 1 or 2: ")) #1 or 2 punishment
            bowl_number = random.randint(1, 2)
            print(f"\nBatsman chose: {bat_number}. Bowler chose: {bowl_number}")
            
            if bat_number not in (1,2):
              raise GameForfeitError("The game has been forfeited as you have defied the rules.")

            if bat_number == bowl_number: #WICKET
              runs_taken = 0
              team1_wickets += 1
              team1_currentbat.remove(batsman)
              team2_individual_wickets[bowler] += 1
              team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print(f"WICKET! {batsman} {team1_individual_runs[batsman]}({team1_individual_balls[batsman]})")
              
            else: #DOT BALL
              runs_taken = 0
              print("Dot ball.\n")
              team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name

          elif bowl_number not in numbers: #bowler put illegal number - NO BALL!
            print("\nNO BALL! Free hit to follow.")
            team1_score += 1 #add extra run to batting team's score
            team2_bowler_runs[bowler] += 1 #extra run to bowler's quota
            bat_number = random.choice(numbers)
            bowl_number = int(input(f"Enter a number from {numbers}: "))
            
            print(f"\nBatsman chose: {bat_number}. Bowler chose: {bowl_number}")

            if bat_number == bowl_number: #NOT A WICKET, DOT BALL! (Free hit)
              runs_taken = 0
              team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print("Dot ball.\n")

            else: #runs taken = number put by batsman (Free hit)
              runs_taken = bat_number if bat_number != 0 else bowl_number
              team1_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team1_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team2_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print(number_dict[runs_taken] + "\n")

      if runs_taken%2 == 1 and balls_bowled_in_over != 6: #1 run taken and not the last ball of over
        team1_currentbat.reverse() #reverse the batsmen

      elif runs_taken%2 == 0 and balls_bowled_in_over == 6: #2 runs taken and last ball of the over
        team1_currentbat.reverse() #reverse the batsmen again

      team1_balls += 1
      team1_score += runs_taken #increment team score for runs taken in each ball
      
      if balls_bowled_in_over != 6:
        print(f"{team1.name}: {team1_score}/{team1_wickets} ({team1_balls//6}.{balls_bowled_in_over} overs)")
      else:
        print(f"{team1.name}: {team1_score}/{team1_wickets} ({team1_balls//6} overs)")

      if team1_wickets == 10: #all out within the over
        team2_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        break

    else: #over successfully completed
      team2_individual_overs[bowler] += 1 #add an over to the bowler's name

    team2_nextover = team2_available_bowlers.copy() #making changes to team2's next over bowlers
    team2_nextover.remove(bowler) if bowler in team2_nextover else "" #bowler cannot bowl 2 consecutive overs

  target = team1_score + 1
  print(f"{team1.name} scored {team1_score} in {team1_balls//6}.{team1_balls%6} overs.")
  team1_overs = f"{team1_balls//6}.{team1_balls%6}"
  print(f"{team2.name} need {target} runs in 10 overs to win. Required run rate: {target/10}")

  while team2_wickets < 10 and team2_balls != 60:
    if team1 == player_team:
      print(f"{team1.name} can choose a bowler from {team1_nextover}: ")
      bowler = input("Enter a bowler name: ")
      team1_nextover.remove(bowler)

    else:
      bowlers_list = team1_nextover
      bowler = random.choice(bowlers_list)

    for bowling in team1_individual_overs:
      if team1_individual_overs[bowling] == 2: #2 overs bowled by the bowler
        team1_available_bowlers.remove(bowling) if bowling in team1_available_bowlers else "" #bowler may no more bowl
        team1_nextover.remove(bowling) if bowling in team1_nextover else ""

    balls_bowled_in_over = 0 #initiating an over
    while balls_bowled_in_over < 6: #over is initiated
      if len(team2_currentbat) < 2: #2 batsmen are not on the pitch yet
      
        if team2 == player_team: 
          
          print(f"{team2.name}'s current available players are: {team2_available_batsmen}") #show available batsmen
          
          for _ in range(2 - len(team2_currentbat)): #vacancies on pitch
            batsman = input("Send a batsman: ").strip(" ")
            team2_individual_runs[batsman] = 0
            team2_individual_balls[batsman] = 0
            print(f"{batsman} comes out to bat.\n") if team2_wickets != 0 else ""
            team2_currentbat.insert(0, batsman) if team2_wickets != 0 else team2_currentbat.append(batsman)
            team2_available_batsmen.remove(batsman) #sent batsmen cannot bat again

        else:
          if team2_wickets == 0: #finding openers
            team2_currentbat = team2_available_batsmen[:2] #First two available batsmen are picked up 
            team2_individual_runs = {}.fromkeys(team2_currentbat, 0)
            team2_individual_balls = {}.fromkeys(team2_currentbat, 0)
            print(f"The openers are: {team2_currentbat}\n")
            team2_available_batsmen = team2_available_batsmen[2: ] #from in at 3 till in at 11
          
          else: #at least 1 wicket is gone
            team2_currentbat.insert(0, team2_available_batsmen[0]) if team2_available_batsmen!=[] else "" #first available batsman picked
            batsman = team2_available_batsmen.pop(0) #no more available
            print(f"{batsman} comes out to bat.\n")
            team2_individual_runs[batsman] = 0
            team2_individual_balls[batsman] = 0

      batsman = team2_currentbat[0] #first person in current batsmen list is on strike
      print(f"{bowler} bowling to {batsman}.\n")

      if team2 == player_team: 
        bat_number = int(input(f"Enter a number from {numbers}: "))
        bowl_number = random.choice(numbers)
      
      else: 
        bat_number = random.choice(numbers)
        bowl_number = int(input(f"Enter a number from {numbers}: "))
      
      balls_bowled_in_over += 1 #add 1 ball to the over

      print(f'''\nBatsman put: {bat_number}, Bowler put: {bowl_number}''')
      if bat_number == bowl_number: #WICKET
        runs_taken = 0
        team2_wickets += 1 #add 1 wicket to the team tally
        team2_currentbat.remove(batsman) #remove batsman from pitch
        team1_individual_wickets[bowler] += 1 #add wicket to bowler's name
        team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
        team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
        team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
        print(f"WICKET! {batsman} {team2_individual_runs[batsman]}({team2_individual_balls[batsman]})\n")
      
      else: #Not a wicket or chance of an illegal delivery
        if (bat_number in numbers) and (bowl_number in numbers): #Both are valid numbers - legal ball
          runs_taken = scoreCounting(bat_number, bowl_number) #counting runs scored

          print(number_dict[runs_taken] + "\n") #print the statement related to those runs

          team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
          team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
          team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
        
        else: #illegal ball
          balls_bowled_in_over -= 1 #undo the 1 ball addition to the over
          print("\nInvalid number!")

          if bat_number not in numbers: #batsman put illegal number
            bat_number = int(input("Enter either 1 or 2: ")) #1 or 2 punishment
            bowl_number = random.randint(1, 2)
            print(f"\nBatsman chose: {bat_number}. Bowler chose: {bowl_number}")
            
            if bat_number not in (1,2):
              raise GameForfeitError("The game has been forfeited as you have defied the rules.")

            if bat_number == bowl_number: #WICKET
              runs_taken = 0
              team2_wickets += 1
              team2_currentbat.remove(batsman)
              team1_individual_wickets[bowler] += 1
              team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print(f"WICKET! {batsman} {team2_individual_runs[batsman]}({team2_individual_balls[batsman]})")
              
            else: #DOT BALL
              runs_taken = 0
              print("Dot ball.\n")
              team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name

          elif bowl_number not in numbers: #bowler put illegal number - NO BALL!
            print("\nNO BALL! Free hit to follow.")
            team2_score += 1 #add extra run to batting team's score
            team1_bowler_runs[bowler] += 1 #extra run to bowler's quota
            bat_number = random.choice(numbers)
            bowl_number = int(input(f"Enter a number from {numbers}: "))
            
            print(f"\nBatsman chose: {bat_number}. Bowler chose: {bowl_number}")

            if bat_number == bowl_number: #NOT A WICKET, DOT BALL! (Free hit)
              runs_taken = 0
              team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print("Dot ball.\n")

            else: #runs taken = number put by batsman (Free hit)
              runs_taken = bat_number if bat_number != 0 else bowl_number
              team2_individual_balls[batsman] += 1 #add 1 ball to batsman's name
              team2_individual_runs[batsman] += runs_taken #add runs taken to batsman's name
              team1_bowler_runs[bowler] += runs_taken #add runs taken to bowler's name
              print(number_dict[runs_taken] + "\n")

      if runs_taken%2 == 1 and balls_bowled_in_over != 6: #1 run taken and not the last ball of over
        team2_currentbat.reverse() #reverse the batsmen

      elif runs_taken%2 == 0 and balls_bowled_in_over == 6: #2 runs taken and last ball of the over
        team2_currentbat.reverse() #reverse the batsmen again

      team2_balls += 1
      team2_score += runs_taken #increment team score for runs taken in each ball
      
      if balls_bowled_in_over != 6:
        print(f"{team2.name}: {team2_score}/{team2_wickets} ({team2_balls//6}.{balls_bowled_in_over} overs)")
      else:
        print(f"{team2.name}: {team2_score}/{team2_wickets} ({team2_balls//6} overs)")
      
      print(f"Target: {target}\n")

      if team2_score >= target:
        team2_overs = f"{team2_balls//6}.{balls_bowled_in_over}"
        team1_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        gameOver = True
        result = f"{team2.name} beat {team1.name} by {10 - team2_wickets} wickets."
        print(f"{team2.name} beat {team1.name} by {10 - team2_wickets} wickets.")
        break

      if team2_wickets == 10: #all out within the over
        team1_individual_overs[bowler] += float(f"0.{balls_bowled_in_over}") if balls_bowled_in_over != 6 else 1
        team2_overs = f"{team2_balls//6}.{balls_bowled_in_over}"
        if team2_score == team1_score:
          gameOver = True
          result = "Game drawn."
          print("Game drawn.")
        else:
          gameOver = True
          result = f"{team1.name} beat {team2.name} by {team1_score - team2_score} runs."
          print(f"{team1.name} beat {team2.name} by {team1_score - team2_score} runs.")
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
      print(result)
  
  view_match_report = input("View match report (entire scorecard)? Enter Y for yes and N for no: ").upper().strip(" ")
  if view_match_report == "Y":
    print("Match report:\n")
    print(f"Toss: {toss_statement}")
    print(f"Result: {result}")
    print(f"{team1.name} - {team1_score}/{team1_wickets} ({team1_overs} overs):")
    for batter in team1_individual_runs:
      runs = team1_individual_runs[batter]
      balls = team1_individual_balls[batter]
      if batter == team1.captain:
        batter += " (c)"
      if batter == team1.wicketkeeper:
        batter += " (wk)"
      if batter in team1_currentbat:
        batter += "*"
      spaces = " " * (35 - (len(batter) + (len(str(runs)) + len(str(balls))) - 2))
      if batter not in team1_available_batsmen:
        print(f"{batter}{spaces}{runs}({balls})")
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
      runs = team2_individual_runs[batter]
      balls = team2_individual_balls[batter]
      if batter == team2.captain:
        batter += " (c)"
      if batter == team2.wicketkeeper:
        batter += " (wk)"
      if batter in team2_currentbat:
        batter += "*"
      spaces = " " * (35 - (len(batter) + (len(str(runs)) + len(str(balls))) - 2))
      if batter not in team2_available_batsmen:
        print(f"{batter}{spaces}{runs}({balls})")
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
