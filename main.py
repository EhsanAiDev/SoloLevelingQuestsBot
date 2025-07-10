import os 
import random
import telebot
import schedule
import threading
from game import Game 
from db import db,cursor
from sensinfo import API_KEY
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup


bot = telebot.TeleBot(API_KEY)
game = Game()
images = [f"./images/{image}" for image in os.listdir("./images")]
#####################################################
def ProfilePage(user_id):
    image = random.choice(images)
    profile_info = game.Profile(user_id=user_id)
    with open(f"{image}" , 'rb') as photo:
        markup = InlineKeyboardMarkup()
        item1 = InlineKeyboardButton("Submit Task" , callback_data="submit_task")
        item2 = InlineKeyboardButton("Top Players" , callback_data="top_players")
        item3 = InlineKeyboardButton("About Me" , callback_data="about_me")
        item4 = InlineKeyboardButton("Channels" , callback_data="channels")

        markup.row(item1)
        markup.row(item2)
        markup.row(item3 , item4)

        bot.send_photo(chat_id=user_id,
                       caption=profile_info, 
                       photo=photo,
                       parse_mode="Markdown",
                       reply_markup=markup
                       )
        
def StartPage(user_id):
    text = (
        "*⚔️ Welcome to the Solo Leveling Quest Bot! ⚔️*\n\n"
        "Prepare to engage in a rigorous journey of self-improvement and physical challenges. Here’s how the game operates:\n\n"
        
        "*📋 Create Your Profile:* Upon starting, your profile will be established to monitor your progress and achievements.\n\n"
        
        "*🏋️‍♂️ Complete Tasks:* Participate in various physical activities, including:\n"
        "   • Push-Ups\n"
        "   • Squats\n"
        "   • Athletics\n"
        "Each completed task will earn you experience points (XP), which are critical for your overall score.\n\n"
        
        "*📊 Score Ranking System:*\n"
        "   • Your score is determined by the XP you accumulate from completing tasks.\n"
        "   • Compete with other players to ascend the leaderboard. Only the top players will be acknowledged for their accomplishments.\n\n"
        
        "*📅 Daily Evaluations:*\n"
        "   • Your performance will be assessed daily. Failure to complete tasks may result in XP loss.\n"
        "   • Players whose scores drop to zero will be banned from the game. Stay vigilant!\n\n"
        
        "*🔍 Profile Overview:*\n You can review your profile at any time to check your score, completed tasks, and overall progress.\n\n"
        
        "*🤝 Community Engagement:*\n Connect with other players, share your experiences, and motivate each other to achieve your fitness goals.\n\n"
        
        "To commence, click the button below to view your profile and begin your quest for personal growth."
    )
    bot.send_message(chat_id=user_id,
                     text=text,
                     parse_mode="Markdown"
                     )

#####################################################

@bot.message_handler(commands=['start'])
def StartHanedel(message):
    ms_info = message.from_user
    user_id = ms_info.id
    name = f"{ms_info.first_name}{'' if ms_info.last_name == None else ' '+ms_info.last_name}"
    username = ms_info.username
    
    if not game.IsBan(user_id=user_id):
        cursor.execute("SELECT * FROM users WHERE user_id=?" , (user_id,))
        resualt = cursor.fetchall()
        if not resualt:
            cursor.execute("INSERT INTO users (user_id, name, username) VALUES (?, ? ,?)" , (user_id, name, username))
            db.commit()
        StartPage(user_id=user_id)
        ProfilePage(user_id=user_id)
    else:
        bot.send_message(chat_id=user_id , text="you banned from this game")

    
   
#####################################################

@bot.callback_query_handler(func= lambda call:True)
def CallBackHandle(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    if not game.IsBan(user_id=user_id):
        if call.data == "top_players":
            bot.delete_message(chat_id=user_id,message_id=message_id)

            markup = InlineKeyboardMarkup()
            back = InlineKeyboardButton("Back" , callback_data="back")
            markup.row(back)

            bot.send_message(chat_id=user_id, 
                            text=game.TopPlayers(user_id=user_id),
                            reply_markup=markup,
                            parse_mode='Markdown')
        
        if call.data == "submit_task":
            bot.edit_message_reply_markup(chat_id=user_id,
                                          message_id=message_id,
                                          reply_markup=game.AnalysisTasks_button(user_id=user_id))
            
        elif call.data == "PushUps":
            bot.answer_callback_query(call.id,text="Task Submited\nyou earn +10xp" , show_alert=True)
            bot.edit_message_caption(chat_id=user_id,
                                     message_id=message_id,
                                     caption=game.SubmitTask(user_id=user_id , task="PushUps"),
                                     reply_markup=game.AnalysisTasks_button(user_id=user_id),
                                     parse_mode="Markdown")
            
        elif call.data == "Squat":
            bot.answer_callback_query(call.id,text="Task Submited\nyou earn +10xp" , show_alert=True)
            bot.edit_message_caption(chat_id=user_id,
                                     message_id=message_id,
                                     caption=game.SubmitTask(user_id=user_id , task="Squat"),
                                     reply_markup=game.AnalysisTasks_button(user_id=user_id),
                                     parse_mode="Markdown")
            
        elif call.data == "Athletics":
            bot.answer_callback_query(call.id,text="Task Submited\nyou earn +10xp" , show_alert=True)
            bot.edit_message_caption(chat_id=user_id,
                                     message_id=message_id,
                                     caption=game.SubmitTask(user_id=user_id , task="Athletics"),
                                     reply_markup=game.AnalysisTasks_button(user_id=user_id),
                                     parse_mode="Markdown")
            

        elif call.data == "back":
            bot.delete_message(chat_id=user_id,message_id=message_id)
            ProfilePage(user_id=user_id)    

        elif call.data == "about_me":
            text = (
                "Hi there! My name is *Ehsan*.\n"
                "People on the internet know me as *Naku Tenshi*. \n\n"
                "Here are some of my social media links:\n"
                "💬*my personal channel's link*: t.me/nakutenshi 💬\n"
                "📱 *Telegram*: [@EhsanNaderlou](tg://resolve?domain=EhsanNaderlou)📱\n"
                "📸 *Instagram*: [ehsan.aidev](https://www.instagram.com/ehsan.aidev)📸\n"
                "💻 *GitHub*: [EhsanAiDev](https://github.com/EhsanAiDev)💻\n"
            )

            bot.send_message(chat_id=user_id,
                            text=text,
                            parse_mode="Markdown")
            
        elif call.data == "channels":
            bot.send_message(chat_id=user_id,
                            text="channel's link: https://t.me/SoloLevelingQuest")
    else:
        bot.send_message(chat_id=user_id , text="you banned from this game")



def UpdateGame():
    cursor.execute("SELECT user_id,score,did_pushup,did_squat,did_run FROM users;")
    players = cursor.fetchall()
    for player in players:
        x = 0 
        for task in player[2:]:
            if task == 0:
                x += 15
        
        score = player[1] - x
        if score <= 0 : # ban player
            cursor.execute("INSERT INTO block_users (user_id) VALUES (?);",(player[0],)) # add user to block list
            db.commit()
            cursor.execute("DELETE FROM users WHERE user_id = ?",(player[0],)) # delete user from users table
            db.commit()

            bot.send_message(chat_id=player[0] , text="‼️ You Banned from game ‼️\nyou lose all scores ")        
        else:
            cursor.execute("UPDATE users SET score = ?,did_pushup=0,did_squat=0,did_run=0,day=day+1 WHERE user_id = ?;" , (score,player[0]))
            db.commit()

            bot.send_message(chat_id=player[0],text=f"❗ you lose {x}xp ❗") 
            ProfilePage(user_id=player[0])


def run_scheduler():
    schedule.every().day.at("00:00").do(UpdateGame)
    
    while True:
        schedule.run_pending()


scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
if __name__ == '__main__':
    print("[INFO] starting bot...")
    bot.infinity_polling()