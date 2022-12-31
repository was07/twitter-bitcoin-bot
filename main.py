import schedule
import time
import datetime
import bot


if __name__ == "__main__":
    bot = bot.Bot()
    # Calculate the times in a day when the bot will tweet
    TIMES = [
        f"{hour}:30:00" for hour in range(21)
    ]

    # print(TIMES)

    def job():
        cur_time = datetime.datetime.now().strftime("%H:%M:%S")
        for runTime in TIMES:
            if cur_time == str(runTime):
                print(f"\n[+] Current time matched a tweet time. cur_time = \x1b[45m{cur_time}\x1b[0m")
                bot.tweet()

    schedule.every(0.01).minutes.do(job)
    
    # Main Loop
    while True:
        schedule.run_pending()
        time.sleep(1)
