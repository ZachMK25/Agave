from flask import Flask, jsonify

import scrape_description

app = Flask(__name__)
    

@app.route('/<video_id>', methods=['GET'])
def get_item(video_id):
    print(video_id)
    out = scrape_description(video_id)
    if out:
        return jsonify(out)
    else:
        return jsonify({"error": "Error Processing video"}), 404


if __name__ == '__main__':
    app.run(debug=True)