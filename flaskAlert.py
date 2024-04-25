import telegram
import json
import logging
import pytz
from dateutil import parser
from flask import Flask, request
from flask_basicauth import BasicAuth
import time

app = Flask(__name__)
app.secret_key = 'lAlAlA123'
basic_auth = BasicAuth(app)

# Danh sách các cặp bot_token và chat_id tương ứng
bot_configs = [
    {"bot_token": "botToken", "chat_id": "xchatIDx"},
#    {"bot_token": "1828768750:AAGwespDaekiXQgP-ji-vZ2AjzCy08IHKdjE", "chat_id": "-599148s695"},
    # Thêm các cặp bot_token và chat_id cho các kênh chat khác nếu cần
]

# Authentication conf, change it!
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

# Khởi tạo danh sách đối tượng bot từ bot_configs
bots = {config["bot_token"]: telegram.Bot(token=config["bot_token"]) for config in bot_configs}

@app.route('/alert', methods=['POST'])
def postAlertmanager():
    try:
        content = json.loads(request.get_data())
        print(content)
        for alert in content['alerts']:
            print(alert)
            message = "**" + "Status: " + "**" + (alert['status']).upper() + "\n"
            message += "**" + "Alertname: " + "**" + alert['labels']['alertname'] + "\n"

            if 'info' in alert['annotations']:
                message += "**" + "Info: " + "**" + "`" + alert['annotations']['info'] + "`" + "\n"
            if 'summary' in alert['annotations']:
                message += "**" + "Summary: " + "**" + "`" + alert['annotations']['summary'] + "`" + "\n"
            if 'description' in alert['annotations']:
                message += "**" + "Description: " + "**" + "`" + alert['annotations']['description'] + "`" + "\n"

            # Chuyển đổi thời gian sang múi giờ +7 trước khi thêm vào thông báo
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).astimezone(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M:%S')
                message += "**" + "Resolved: " + "**" + "`" + str(correctDate) + "`"
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).astimezone(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M:%S')
                message += "**" + "Started: " + "**" + "`" + str(correctDate) + "`"

            # Gửi cảnh báo đến các kênh chat tương ứng cho từng bot
            for config in bot_configs:
                bot_token = config["bot_token"]
                chat_id = config["chat_id"]
                bot = bots.get(bot_token)
                if bot:
                    bot.sendMessage(chat_id=chat_id, text=message, parse_mode='Markdown')

        return "Alert OK", 200
    except Exception as error:
#        for config in bot_configs:
#            bot_token = config["bot_token"]
#            chat_id = config["chat_id"]
#            bot = bots.get(bot_token)
#            if bot:
#                bot.sendMessage(chat_id=chat_id, text="Error: " + str(error))
        app.logger.info("\t%s", error)
        return "Alert fail", 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9119, debug=True)