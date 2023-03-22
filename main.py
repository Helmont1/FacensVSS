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
        writer.writerow(['position_x_1', 'position_y_1', 'position_a_1', 'velocity_x_1', 'velocity_y_1', 'velocity_a_1', 'position_x_2', 'position_y_2', 'position_a_2', 'velocity_x_2', 'velocity_y_2', 'velocity_a_2', 'position_x_3', 'position_y_3', 'position_a_3', 'velocity_x_3', 'velocity_y_3', 'velocity_a_3', 'ball_position_x', 'ball_position_y', 'ball_velocity_x', 'ball_velocity_y', 'position_enemy_x_1', 'position_enemy_y_1', 'position_enemy_a_1', 'velocity_enemy_x_1', 'velocity_enemy_y_1', 'velocity_enemy_a_1', 'position_enemy_x_2', 'position_enemy_y_2', 'position_enemy_a_2', 'velocity_enemy_x_2', 'velocity_enemy_y_2', 'velocity_enemy_a_2', 'position_enemy_x_3', 'position_enemy_y_3', 'position_enemy_a_3', 'velocity_enemy_x_3', 'velocity_enemy_y_3', 'velocity_enemy_a_3', 'objectives_1_x', 'objectives_1_y', 'objectives_2_x', 'objectives_2_y', 'objectives_3_x', 'objectives_3_y','goal', 'enemy_goal'])
        
        actions = []
        blue_score = 0
        yellow_score = 0
        last_foul = None
        
        while True:
            referee.update()
            ref_data = referee.get_data()
            vision.update()
            ball = vision.get_ball()
            half = referee.get_half()
            
            if ref_data["foul"] == 4 and last_foul != 4:
                if ref_data["color"] == 0:
                    yellow_score += 1
                elif ref_data["color"] == 1:
                    blue_score += 1
                last_foul = ref_data["foul"]
            elif ref_data["foul"] != 4:
                last_foul = ref_data["foul"]

            teamsParameters = MatchParameters(vision.get_field_data())

            if ref_data["game_on"]:
                objectives = Strategy(teamsParameters, "default").main_strategy()
                actions = teamsParameters.controller(teamsParameters.yellowRobotValues if teamsParameters.isYellowTeam else teamsParameters.blueRobotValues, objectives)
                
                actuator.send_all(actions)
                if teamsParameters.isYellowTeam:
                    writer.writerow([teamsParameters.yellowRobotValues[0].x, teamsParameters.yellowRobotValues[0].y, teamsParameters.yellowRobotValues[0].a, teamsParameters.yellowRobotValues[0].vx, teamsParameters.yellowRobotValues[0].vy, teamsParameters.yellowRobotValues[0].va, teamsParameters.yellowRobotValues[1].x, teamsParameters.yellowRobotValues[1].y, teamsParameters.yellowRobotValues[1].a, teamsParameters.yellowRobotValues[1].vx, teamsParameters.yellowRobotValues[1].vy, teamsParameters.yellowRobotValues[1].va, teamsParameters.yellowRobotValues[2].x, teamsParameters.yellowRobotValues[2].y, teamsParameters.yellowRobotValues[2].a, teamsParameters.yellowRobotValues[2].vx, teamsParameters.yellowRobotValues[2].vy, teamsParameters.yellowRobotValues[2].va, ball.x, ball.y, ball.vx, ball.vy, teamsParameters.blueRobotValues[0].x, teamsParameters.blueRobotValues[0].y, teamsParameters.blueRobotValues[0].a, teamsParameters.blueRobotValues[0].vx, teamsParameters.blueRobotValues[0].vy, teamsParameters.blueRobotValues[0].va, teamsParameters.blueRobotValues[1].x, teamsParameters.blueRobotValues[1].y, teamsParameters.blueRobotValues[1].a, teamsParameters.blueRobotValues[1].vx, teamsParameters.blueRobotValues[1].vy, teamsParameters.blueRobotValues[1].va, teamsParameters.blueRobotValues[2].x, teamsParameters.blueRobotValues[2].y, teamsParameters.blueRobotValues[2].a, teamsParameters.blueRobotValues[2].vx, teamsParameters.blueRobotValues[2].vy, teamsParameters.blueRobotValues[2].va, objectives[0].x, objectives[0].y, objectives[1].x, objectives[1].y, objectives[2].x, objectives[2].y, yellow_score, blue_score])
                    
                elif not teamsParameters.isYellowTeam:
                    writer.writerow([teamsParameters.blueRobotValues[0].x, teamsParameters.blueRobotValues[0].y, teamsParameters.blueRobotValues[0].a, teamsParameters.blueRobotValues[0].vx, teamsParameters.blueRobotValues[0].vy, teamsParameters.blueRobotValues[0].va, teamsParameters.blueRobotValues[1].x, teamsParameters.blueRobotValues[1].y, teamsParameters.blueRobotValues[1].a, teamsParameters.blueRobotValues[1].vx, teamsParameters.blueRobotValues[1].vy, teamsParameters.blueRobotValues[1].va, teamsParameters.blueRobotValues[2].x, teamsParameters.blueRobotValues[2].y, teamsParameters.blueRobotValues[2].a, teamsParameters.blueRobotValues[2].vx, teamsParameters.blueRobotValues[2].vy, teamsParameters.blueRobotValues[2].va, ball.x, ball.y, ball.vx, ball.vy, teamsParameters.yellowRobotValues[0].x, teamsParameters.yellowRobotValues[0].y, teamsParameters.yellowRobotValues[0].a, teamsParameters.yellowRobotValues[0].vx, teamsParameters.yellowRobotValues[0].vy, teamsParameters.yellowRobotValues[0].va, teamsParameters.yellowRobotValues[1].x, teamsParameters.yellowRobotValues[1].y, teamsParameters.yellowRobotValues[1].a, teamsParameters.yellowRobotValues[1].vx, teamsParameters.yellowRobotValues[1].vy, teamsParameters.yellowRobotValues[1].va, teamsParameters.yellowRobotValues[2].x, teamsParameters.yellowRobotValues[2].y, teamsParameters.yellowRobotValues[2].a, teamsParameters.yellowRobotValues[2].vx, teamsParameters.yellowRobotValues[2].vy, teamsParameters.yellowRobotValues[2].va, objectives[0].x, objectives[0].y, objectives[1].x, objectives[1].y, objectives[2].x, objectives[2].y, blue_score, yellow_score])
                sleep(0.1)
         
            elif ref_data["foul"] != 7:
                # foul behaviour
                actuator.stop()

            else:
                # halt behavior
                actuator.stop()
