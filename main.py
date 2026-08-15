import telebot
import requests

TELEGRAM_BOT_TOKEN = "8878697817:AAFLq1vVheuTUHvDG9a9Sletjek9Sp0mmxw"
GEMINI_API_KEY = "AQ.Ab8RN6KBI0mzH1uQxDK_9FTYI17_4VyN_eJYj8L0K-iXieuPNA"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        user_name = message.from_user.first_name
        
        print(f"[{user_name}] মেসেজ পাঠিয়েছে: {user_text}")
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        prompt = (
            "তুমি জেমিনি (Gemini)-এর প্রযুক্তিতে তৈরি একটি এআই বট। "
            "তোমার মালিক বা সৃষ্টিকর্তা হলেন ইয়াকুব আলী (Yeakub Ali)। "
            "কেউ যদি তোমাকে জিজ্ঞেস করে 'তুমি কে?', 'তোমার নাম কি?', 'তুমি কার তৈরি?', "
            "তখন তুমি বলবে: 'আমি ইয়াকুব আলীর তৈরি করা একটি কৃত্রিম বুদ্ধিমত্তা বা এআই সহকারী।' "
            f"ব্যবহারকারীর মেসেজ: {user_text}"
        )
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()
        
        if 'error' in res_json:
            error_msg = res_json['error'].get('message', 'Unknown error')
            bot.reply_to(message, f"API Error: {error_msg}")
            return
            
        reply = res_json['candidates'][0]['content']['parts'][0]['text']
        bot.reply_to(message, reply)
        
    except Exception as e:
        err_str = str(e)
        bot.reply_to(message, f"Error: {err_str}")

print("Bot is running successfully...")
bot.infinity_polling()
