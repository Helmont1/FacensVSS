import sys
import csv

from Controllers.MatchParameters import MatchParameters
from Strategies.MainStrategy import Strategy

from bridge import (Actuator, Replacer, Vision, Referee)



if __name__ == "__main__":

    try:
        team = sys.argv[1]

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

    filename = "dataYellowTeam.csv"
    
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['pos_x_1', 'pos_y_1', 'pos_x_2', 'pos_y_2', 'pos_x_3', 'pos_y_3', 'action_1', 'action_2', 'action_3'])
        
    actions = []
    
    while True:
        referee.update()
        ref_data = referee.get_data()
        vision.update()

        teamsParameters = MatchParameters(vision.get_field_data())

        # ref_data["game_on"] = True

        if ref_data["game_on"]:
            objectives = Strategy(teamsParameters, "default").main_strategy()
            actions = teamsParameters.controller(teamsParameters.yellowRobotValues
                                                         if teamsParameters.isYellowTeam
                                                         else teamsParameters.blueRobotValues,
                                                         objectives)
            
            actuator.send_all(actions)

            writer.writerow([teamsParameters.yellowRobotValues[0][0], teamsParameters.yellowRobotValues[0][1],
                             teamsParameters.yellowRobotValues[1][0], teamsParameters.yellowRobotValues[1][1],
                             teamsParameters.yellowRobotValues[2][0], teamsParameters.yellowRobotValues[2][1],
                             actions[0][0], actions[1][0], actions[2][0]])

        elif ref_data["foul"] != 7:
            # foul behaviour
            actuator.stop()

        else:
            # halt behavior
            actuator.stop()
