import difflib
import os

class ArabicSpellingChecker:
    def __init__(self):
        # Application settings
        self.dictionary_file = "arabic_words.txt"
        self.history_file = "spelling_history.txt"
        self.user_dictionary = "user_dictionary.txt"
        
        # Create storage files if they don't exist
        self.load_user_dictionary()
        
        # Checking statistics
        self.stats = {
            'total_words': 0,
            'correct_words': 0,
            'incorrect_words': 0
        }
    
    def load_words(self):
        """Load words from main and user dictionaries"""
        words = []
        
        # Load main dictionary
        if os.path.exists(self.dictionary_file):
            try:
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    words.extend([line.strip() for line in f if line.strip()])
            except Exception as e:
                print(f"Error reading dictionary file: {str(e)}")
        
        # Load user dictionary
        if os.path.exists(self.user_dictionary):
            try:
                with open(self.user_dictionary, 'r', encoding='utf-8') as f:
                    words.extend([line.strip() for line in f if line.strip()])
            except Exception as e:
                print(f"Error reading user dictionary: {str(e)}")
        
        return list(set(words))  # Remove duplicates
    
    def check_spelling(self, text):
        """Check spelling of entered text"""
        if not text.strip():
            print("Please enter a word or sentence first")
            return
        
        # Update history
        self.update_history(text)
        
        # Load words from dictionaries
        dictionary_words = self.load_words()
        if not dictionary_words:
            print("No dictionary available for checking!")
            return
        
        # Split text into words
        words = text.split()
        self.stats['total_words'] += len(words)
        correct_count = 0
        incorrect_words = []
        
        # Check each word individually
        for word in words:
            if word in dictionary_words:
                correct_count += 1
            else:
                incorrect_words.append(word)
        
        # Update statistics
        self.stats['correct_words'] += correct_count
        self.stats['incorrect_words'] += len(incorrect_words)
        
        # Display results
        if not incorrect_words:
            print("\n✓ All words are correct")
        else:
            print(f"\n✗ Incorrect words: {', '.join(incorrect_words)}")
            
            # Show suggestions for each incorrect word
            suggestions = []
            for word in incorrect_words:
                word_suggestions = difflib.get_close_matches(word, dictionary_words, n=2, cutoff=0.6)
                if word_suggestions:
                    suggestions.append(f"{word}: {' or '.join(word_suggestions)}")
            
            if suggestions:
                print("\n✎ Suggestions:")
                print("\n".join(suggestions))
            else:
                print("\nNo suggestions available")
        
        # Show statistics
        self.show_stats()
    
    def show_stats(self):
        """Display checking statistics"""
        print("\nStatistics:")
        print(f"- Words checked: {self.stats['total_words']}")
        print(f"- Correct words: {self.stats['correct_words']}")
        print(f"- Errors: {self.stats['incorrect_words']}")
        print("-" * 40)
    
    def add_to_dictionary(self, word):
        """Add word to user dictionary"""
        if not word.strip():
            print("Please enter a word first")
            return
        
        try:
            with open(self.user_dictionary, 'a', encoding='utf-8') as f:
                f.write(f"{word}\n")
            print(f"Word '{word}' added to user dictionary")
        except Exception as e:
            print(f"Failed to add word: {str(e)}")
    
    def update_history(self, text):
        """Update checking history"""
        try:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(f"{text}\n")
        except Exception as e:
            print(f"Error saving history: {str(e)}")
    
    def load_user_dictionary(self):
        """Create user dictionary if it doesn't exist"""
        if not os.path.exists(self.user_dictionary):
            try:
                with open(self.user_dictionary, 'w', encoding='utf-8') as f:
                    f.write("")
            except Exception as e:
                print(f"Failed to create user dictionary: {str(e)}")

def show_menu():
    """Display menu options"""
    print("\n" + "=" * 30)
    print("Arabic Spell Checker")
    print("=" * 30)
    print("1. Check word")
    print("2. Add word to dictionary")
    print("3. Show statistics")
    print("4. Exit")
    print("=" * 30)

def main():
    checker = ArabicSpellingChecker()
    
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ")
        
        if choice == "1":
            text = input("Enter word: ")
            checker.check_spelling(text)
        elif choice == "2":
            word = input("Enter new word to add to dictionary: ")
            checker.add_to_dictionary(word)
        elif choice == "3":
            checker.show_stats()
        elif choice == "4":
            print("Thank you for using the spell checker. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()