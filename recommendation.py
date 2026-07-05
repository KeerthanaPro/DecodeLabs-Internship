# AI Recommendation System
# DecodeLabs Internship - Project 3

# Recommendation Database
recommendations = {
    "technology": [
        "Python Programming Course",
        "Artificial Intelligence Basics",
        "Web Development Bootcamp",
        "Cloud Computing"
    ],
    "sports": [
        "Football Training",
        "Cricket Coaching",
        "Yoga Classes",
        "Fitness Challenge"
    ],
    "music": [
        "Learn Guitar",
        "Piano Course",
        "Music Production",
        "Singing Workshop"
    ],
    "movies": [
        "Inception",
        "Interstellar",
        "The Dark Knight",
        "Avengers: Endgame"
    ],
    "books": [
        "Atomic Habits",
        "The Alchemist",
        "Rich Dad Poor Dad",
        "Think Like a Monk"
    ],
    "travel": [
        "Ooty",
        "Manali",
        "Goa",
        "Kerala Backwaters"
    ]
}

print("="*50)
print("      AI RECOMMENDATION SYSTEM")
print("="*50)

print("\nAvailable Categories:")
for category in recommendations:
    print("-", category.title())

user_choice = input("\nEnter your interest: ").strip().lower()

print("\nRecommended for You")
print("-"*30)

if user_choice in recommendations:
    for i, item in enumerate(recommendations[user_choice], start=1):
        print(f"{i}. {item}")
else:
    print("Sorry! No recommendations available.")
    print("Try one of these categories:")

    for category in recommendations:
        print("-", category.title())