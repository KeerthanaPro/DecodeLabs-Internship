from flask import Flask, render_template, request, jsonify
import datetime
import re

app = Flask(__name__)

# Knowledge Base - Dictionary based rules
responses = {
    # Module 1: Greetings
    "hello": "Hello! Welcome to RMK Chatbot. How can I help you?",
    "hi": "Hi there! 👋 How can I assist you today?",
    "hey": "Hey! What can I do for you?",
    "good morning": "Good Morning! 🌞 Hope you have a great day!",
    
    # Module 2: College Information
    "what is rmk": "RMK Engineering College is a prestigious institution located in Kavaraipettai, Tamil Nadu.",
    "where is rmk": "RMK Engineering College is located in Kavaraipettai, near Chennai, Tamil Nadu.",
    "rmk college": "RMK Engineering College offers various engineering programs and is known for academic excellence.",
    "about rmk": "RMK Engineering College was established in 1995 and is affiliated with Anna University.",
    
    # Module 3: Internship Queries
    "internship": "This internship focuses on AI-based projects using Python and Flask. You'll build rule-based chatbots!",
    "project": "You'll work on real-world AI projects including chatbots, recommendation systems, and more.",
    "training": "The training program covers Python, Flask, JavaScript, and AI fundamentals.",
    "what is internship": "It's a hands-on training program where you build AI applications from scratch.",
    
    # Module 4: Time Query
    "time": "",  # Dynamic response will be added
    "current time": "",  # Dynamic response
    "what time": "",  # Dynamic response
    
    # Module 5: Exit
    "bye": "Thank you for using RMK Chatbot! Have a great day! 👋",
    "exit": "Goodbye! See you next time. 👋",
    "quit": "Session ended. Take care! ✨",
    
    # Additional fallback responses
    "help": "I can help with: \n- Greetings (hello, hi)\n- College info (about RMK)\n- Internship details\n- Current time\n- Exit (bye, exit)",
    "who are you": "I'm RMK Chatbot, your AI assistant built using rule-based logic! 🤖",
    "what can you do": "I can answer questions about RMK College, internships, tell time, and more!"
}

# Statistics
stats = {
    "total_questions": 0,
    "known_queries": 0,
    "unknown_queries": 0,
    "unknown_list": []
}

def sanitize_input(text):
    """Clean user input: lowercase, remove extra spaces, strip"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = ' '.join(text.split())  # Remove extra spaces
    return text

def get_response(user_input):
    """Main rule engine - finds matching response"""
    global stats
    
    stats["total_questions"] += 1
    
    # Clean input
    cleaned = sanitize_input(user_input)
    
    # Check for exact match first
    if cleaned in responses:
        response = responses[cleaned]
        
        # Handle dynamic responses
        if "time" in cleaned or "current time" in cleaned:
            now = datetime.datetime.now()
            response = f"Current time is {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}"
        
        stats["known_queries"] += 1
        return response
    
    # Check for partial matches (contains keywords)
    keyword_matches = {
        "rmk": "RMK Engineering College is located in Kavaraipettai, Tamil Nadu.",
        "internship": "This internship focuses on AI projects using Python and Flask.",
        "project": "You'll work on AI-based projects including chatbots and recommendation systems.",
        "training": "Training covers Python, Flask, JavaScript, and AI fundamentals."
    }
    
    for keyword, response in keyword_matches.items():
        if keyword in cleaned:
            stats["known_queries"] += 1
            return response
    
    # Unknown query
    stats["unknown_queries"] += 1
    if cleaned not in stats["unknown_list"]:
        stats["unknown_list"].append(cleaned)
    
    return "I don't understand that query. Please rephrase or ask about: RMK College, Internship, Training, or say 'help' for options."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/architecture')
def architecture():
    return render_template('architecture.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json.get('message', '')
    response = get_response(user_input)
    
    return jsonify({
        'response': response,
        'stats': stats
    })
    
@app.route('/stats')
def get_stats():
    return jsonify(stats)

@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    global stats
    stats = {
        "total_questions": 0,
        "known_queries": 0,
        "unknown_queries": 0,
        "unknown_list": []
    }
    return jsonify({'message': 'Stats reset successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
