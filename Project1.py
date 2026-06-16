print("Bot: Hello! I am DecodeBot.")
responses = {
    "hi": "Hello!",
    "hello": "Hi there!",
    "good morning": "Good morning!",
    "good evening": "Good evening!",
    "how are you": "I am doing great!",
    "who created you": "I was created by a DecodeLabs intern.",
    "what is python": "Python is a programming language.",
    "thank you": "You're welcome!"
}
while True:
    ui=input("You: ")
    ci=ui.lower().strip()
    if ci=="bye":
        print("Bot: Goodbye!")
        break
 
    reply=responses.get(ci,"Sorry, I don't understand.")
    print(reply)
    
