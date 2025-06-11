import json
import time
import random
from collections import defaultdict

class QuizGame:
    def __init__(self):
        self.questions = self.load_questions()
        self.score = 0
        self.current_question = 0
        self.answers = []
        self.categories = self.get_categories()
        self.selected_category = None
        self.username = ""
    
    def load_questions(self):
        """Load questions from a JSON file"""
        try:
            with open('questions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Sample questions if file doesn't exist
            sample_questions = [
                {
                    "question": "What is the capital of France?",
                    "options": ["London", "Paris", "Berlin", "Madrid"],
                    "answer": 1,
                    "category": "Geography"
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                    "answer": 1,
                    "category": "Science"
                },
                {
                    "question": "What is 2 + 2?",
                    "options": ["3", "4", "5", "6"],
                    "answer": 1,
                    "category": "Math"
                }
            ]
            with open('questions.json', 'w') as f:
                json.dump(sample_questions, f, indent=4)
            return sample_questions
    
    def get_categories(self):
        """Get all available categories from questions"""
        categories = set()
        for question in self.questions:
            categories.add(question["category"])
        return sorted(categories)
    
    def display_welcome(self):
        """Display welcome message and get user's name"""
        print("""
        ******************************
        *       WELCOME TO QUIZ      *
        *            GAME            *
        ******************************
        """)
        self.username = input("Enter your name: ").strip()
        print(f"\nHello, {self.username}! Let's get started.\n")
    
    def select_category(self):
        """Let user select a quiz category"""
        print("Available Categories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        while True:
            try:
                choice = int(input("\nSelect a category (number): "))
                if 1 <= choice <= len(self.categories):
                    self.selected_category = self.categories[choice-1]
                    print(f"\nYou've selected: {self.selected_category}\n")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def filter_questions(self):
        """Filter questions by selected category"""
        if self.selected_category:
            return [q for q in self.questions if q["category"] == self.selected_category]
        return self.questions
    
    def ask_question(self, question):
        """Display a question and get user's answer"""
        print(f"Question {self.current_question + 1}: {question['question']}")
        for i, option in enumerate(question["options"], 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                answer = int(input("\nYour answer (number): "))
                if 1 <= answer <= len(question["options"]):
                    return answer - 1  # Convert to 0-based index
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def check_answer(self, question, user_answer):
        """Check if the answer is correct and update score"""
        is_correct = user_answer == question["answer"]
        if is_correct:
            self.score += 1
            print("\nCorrect! 🎉")
        else:
            correct_option = question["options"][question["answer"]]
            print(f"\nWrong! The correct answer was: {correct_option}")
        
        # Store the answer for review
        self.answers.append({
            "question": question["question"],
            "user_answer": question["options"][user_answer],
            "correct_answer": question["options"][question["answer"]],
            "is_correct": is_correct
        })
        
        self.current_question += 1
        time.sleep(1)  # Pause for a moment
    
    def show_progress(self):
        """Show current progress in the quiz"""
        total = len(self.filter_questions())
        print(f"\nProgress: {self.current_question}/{total} | Score: {self.score}\n")
    
    def show_results(self):
        """Display final results and answer review"""
        total_questions = len(self.answers)
        percentage = (self.score / total_questions) * 100
        
        print("\n" + "="*50)
        print(" QUIZ RESULTS ".center(50, "="))
        print("="*50)
        print(f"\nPlayer: {self.username}")
        print(f"Category: {self.selected_category or 'All Categories'}")
        print(f"Score: {self.score}/{total_questions} ({percentage:.1f}%)")
        
        if percentage >= 70:
            print("\nExcellent! You're a quiz master! 🏆")
        elif percentage >= 50:
            print("\nGood job! You know your stuff! 👍")
        else:
            print("\nKeep practicing! You'll get better! 💪")
        
        # Answer review
        print("\n" + " ANSWER REVIEW ".center(50, "-"))
        for i, answer in enumerate(self.answers, 1):
            print(f"\nQ{i}: {answer['question']}")
            print(f"Your answer: {answer['user_answer']}", 
                  "✅" if answer['is_correct'] else "❌")
            if not answer['is_correct']:
                print(f"Correct answer: {answer['correct_answer']}")
    
    def play_again(self):
        """Ask if user wants to play again"""
        while True:
            choice = input("\nWould you like to play again? (yes/no): ").lower()
            if choice in ['yes', 'y']:
                self.score = 0
                self.current_question = 0
                self.answers = []
                self.selected_category = None
                return True
            elif choice in ['no', 'n']:
                print("\nThanks for playing! Goodbye!")
                return False
            else:
                print("Please enter 'yes' or 'no'.")
    
    def run(self):
        """Main game loop"""
        self.display_welcome()
        
        while True:
            self.select_category()
            filtered_questions = self.filter_questions()
            
            if not filtered_questions:
                print("No questions available in this category. Please select another.")
                continue
                
            # Shuffle questions for variety
            random.shuffle(filtered_questions)
            
            for question in filtered_questions:
                self.show_progress()
                user_answer = self.ask_question(question)
                self.check_answer(question, user_answer)
            
            self.show_results()
            
            if not self.play_again():
                break

if __name__ == "__main__":
    game = QuizGame()
    game.run()
