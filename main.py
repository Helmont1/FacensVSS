import sys
import csv
from time import sleep
from Controllers.MatchParameters import MatchParameters
from Strategies.MainStrategy import Strategy

from bridge import (Actuator, Replacer, Vision, Referee)



if __name__ == "__main__":

    try:
        team = "yellow"        #sys.argv[1]

        if team != "yellow" and team != "blue":
            sys.exit()
    except:
        print("Selecione time corretamente")
        sys.exit()

    if team == "yellow":
        isYellowTeam = True
    else:
        isYellowTeam = False

    # Initialize all clients
    actuator = Actuator(isYellowTeam, "127.0.0.1", 20011)
    replacement = Replacer(isYellowTeam, "224.5.23.2", 10004)
    vision = Vision(isYellowTeam, "224.0.0.1", 10002)
    referee = Referee(isYellowTeam, "224.5.23.2", 10003)

    filename = "data.csv"
    
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['pos_x_1', 'pos_y_1', 'pos_x_2', 'pos_y_2', 'pos_x_3', 'pos_y_3', 'action_x_1', 'action_y_1', 'action_x_2', 'action_y_2', 'action_x_3', 'action_y_3', 'goal', 'enemy_goal'])
        
        actions = []
        blue_score = 0
        yellow_score = 0
        
        while True:
            referee.update()
            ref_data = referee.get_data()
            vision.update()
            ball = vision.get_ball()
            goal_data = referee.goalColor()

            if goal_data == "yellow":
                yellow_score += 1
            elif goal_data == "blue":
                blue_score += 1

            teamsParameters = MatchParameters(vision.get_field_data())

            if ref_data["game_on"]:
                objectives = Strategy(teamsParameters, "default").main_strategy()
                actions = teamsParameters.controller(teamsParameters.yellowRobotValues
                                                            if teamsParameters.isYellowTeam
                                                            else teamsParameters.blueRobotValues,
                                                            objectives)
                
                actuator.send_all(actions)
                
                if teamsParameters.isYellowTeam:
                    writer.writerow([teamsParameters.yellowRobotValues[0].x, teamsParameters.yellowRobotValues[0].y, teamsParameters.yellowRobotValues[1].x, teamsParameters.yellowRobotValues[1].y, teamsParameters.yellowRobotValues[2].x, teamsParameters.yellowRobotValues[2].y, objectives[0].x, objectives[0].y, objectives[1].x, objectives[1].y, objectives[2].x, objectives[2].y, yellow_score, blue_score])
                elif teamsParameters.isBlueTeam:
                    writer.writerow([teamsParameters.blueRobotValues[0].x, teamsParameters.blueRobotValues[0].y, teamsParameters.blueRobotValues[1].x, teamsParameters.blueRobotValues[1].y, teamsParameters.blueRobotValues[2].x, teamsParameters.blueRobotValues[2].y, objectives[0].x, objectives[0].y, objectives[1].x, objectives[1].y, objectives[2].x, objectives[2].y, blue_score, yellow_score])
                    


            elif ref_data["foul"] != 7:
                # foul behaviour
                actuator.stop()

            else:
                # halt behavior
                actuator.stop()
