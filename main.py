from flask import Flask, jsonify

import scrape_description
from dotenv import dotenv_values
import json
import requests
from bs4 import BeautifulSoup

config = dotenv_values(".env")
    
app = Flask(__name__)

@app.route('/<video_id>', methods=['GET'])
def get_item(video_id):
    print(video_id)
    out = scrape_description(video_id, printing=False)
    if out:
        return jsonify(out)
    else:
        return jsonify({"error": "Error Processing video"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    
# @app.route('/ai/<video_id>', methods=["GET"])
# def ai_get_item(video_id):
#     print("AI approach",video_id)
#     soup = BeautifulSoup(requests.get(youtube_url).content, features="html.parser")

#     html_pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')

#     description = html_pattern.findall(str(soup))[0].replace('\\n','\n')

#     print(description)
    
#     url = config["OLLAMA_URL"]
#     headers = {
#         "Content-Type": "application/json"
#     }
    
#     data = {
#         "model":config["MODEL"],
#         "prompt": config["PROMPT"] + description,
#         "stream": False
#     }
    
#     response = requests.post(url, headers=headers, data=json.dumps(data))
    
#     if response.status_code == 200:
#         response_text = response.text
#         data = json.loads(response_text)
#         actual_response = data["response"]
#         return jsonify(actual_response)
#     else:
#         print(response)
#         return jsonify({"error": "Error Processing video"}), 404