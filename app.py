from flask import Flask, send_from_directory, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/judge", methods=["POST"])
def judge():
    data = request.get_json()
    idea = data.get("idea", "")

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=f"""
Evaluate this business idea carefully.

Score it from 0 to 100 based on:
- problem importance
- target customer clarity
- competition
- willingness to pay
- uniqueness
- ease of building
- growth potential

Return exactly:

Score: X/100
Target customer: ...
Strength: ...
Weakness: ...
Biggest risk: ...
Recommendation: ...

Do not use markdown or bullet symbols.

Business idea:
{idea}
"""
    )

    return jsonify({
        "message": "AI judgment",
        "idea": response.output_text
    })

if __name__ == "__main__":
    app.run()