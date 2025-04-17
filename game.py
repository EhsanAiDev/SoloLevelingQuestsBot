import mysql.connector as mysql 
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup,ForceReply
from sensinfo import * 
import time
from db import db,cursor


class Game:
    def __init__(self):
        pass
    
    def AnalysisTasks(self,info):
        tasks = ["PushUps","Squat","Athletics"]
        lenght = ["100" , "100" , "1Km"]
        x = []

        for l,task,status in zip(lenght,tasks,info):
            if status == 0:                
                x.append(f"{l} {task}: it's not done ❌")
            elif status == 1:
                x.append(f"{l} {task}: it's done ✅")
        return "\n".join(x) 
     
    def AnalysisTasks_button(self,user_id):
        task_markup = InlineKeyboardMarkup()

        tasks = ["PushUps","Squat","Athletics"]
        cursor.execute("SELECT did_pushup,did_squat,did_run FROM users WHERE user_id = %s",(user_id,))
        db_tasks = cursor.fetchall()[0]


        for t,dt in zip(tasks,db_tasks):
            if dt == 0 and not dt:                
                task = InlineKeyboardButton(f"Submit {t}" , callback_data=t)
                task_markup.row(task)
        back = InlineKeyboardButton("Back" , callback_data="back")
        task_markup.row(back)
        return task_markup   

    def TopPlayers(self,user_id):
        cursor.execute("SELECT * FROM users ORDER BY score DESC")
        tp = cursor.fetchall()[:10]  # Get the top 10 players
        x = []
        
        for rank, player_info in enumerate(tp, start=1):
            if player_info[1] == user_id:
                x.append(f"*{rank}*. *{player_info[2]}*: *{player_info[5]}*XP *(you)*")  # Format: Rank. PlayerName: Score XP
            else:
                x.append(f"*{rank}*. *{player_info[2]}*: *{player_info[5]}*XP")  # Format: Rank. PlayerName: Score XP

        players = '\n'.join(x)  # Join the player list into a single string
        text = (
            "*🏆 Top Players of This Game:*\n"
            f"{players}\n\n"
        )
        return text

    def Profile(self, user_id):
        cursor.execute('SELECT * FROM users WHERE user_id=%s', (user_id,))
        user = cursor.fetchone()  # Use fetchone() since we expect a single user

        name = user[2]
        username = user[3]
        day = user[4]
        score = user[5]
        info = user[-3:]

        text = (
            "*📋 Player Profile:*\n"
            f"*Name:* {name}\n"
            f"*Score:* {score} XP\n"
            f"*Play Time:* {day} days\n"
            "\n"
            "*Your Tasks:*\n"
            f"{self.AnalysisTasks(info)}"
        )
        return text
    
    def SubmitTask(self, user_id , task):
        if task == 'PushUps':
            cursor.execute("UPDATE users SET did_pushup = 1 WHERE user_id = %s",(user_id,))
            db.commit()
            cursor.execute("UPDATE users SET score = score +10 WHERE user_id = %s;",(user_id,))
            db.commit()
        
            return self.Profile(user_id=user_id)
        elif task == "Squat":
            cursor.execute("UPDATE users SET did_squat = 1 WHERE user_id = %s",(user_id,))
            db.commit()
            cursor.execute("UPDATE users SET score = score +10 WHERE user_id = %s;",(user_id,))
            db.commit()

            return self.Profile(user_id=user_id)
        elif task == "Athletics":
            cursor.execute("UPDATE users SET did_run = 1 WHERE user_id = %s",(user_id,))
            db.commit()
            cursor.execute("UPDATE users SET score = score + 10 WHERE user_id = %s;",(user_id,))
            db.commit()
    
            return self.Profile(user_id=user_id)

    def IsBan(self,user_id):
        cursor.execute("SELECT * FROM block_users WHERE user_id = %s",(user_id,))
        return True if cursor.fetchall() else False
    


    