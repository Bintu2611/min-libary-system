import mainoperations


# --- 1. Menu Function ---
def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "=" * 40)
    print("      Mini Library Management System")
    print("=" * 40)
    print("1. Book Operations (Add, Update, Search, Delete)")
    print("2. Member Operations (Add, Update, Delete)")
    print("3. Borrow/Return Book")
    print("4. View Current Status (All Books/Members)")
    print("0. Exit")
    print("=" * 40)


# --- 2. Input Handlers (Example: Adding a Book) ---
def handle_add_book():
    """Collects input for adding a new book and calls the operations function."""
    print("\n--- Add New Book ---")
    isbn = input("Enter ISBN (e.g., 978-343455): ").strip()

    # Input validation (This is part of your custom design!)
    if mainoperations.books.get(isbn):
        print(f"Operation Failed: Book with ISBN {isbn} already exists.")
        return

    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    genre = input(f"Enter Genre ({', '.join(mainoperations.GENRES)}): ").strip()

    try:
        copies = int(input("Enter Total Copies: ").strip())
    except ValueError:
        print("Operation Failed: Total Copies must be a number.")
        return

    # Call the core function and display result
    if mainoperations.add_book(isbn, title, author, genre, copies):
        print("\n Book added successfully!")
    else:
        # operations.py already prints the specific error (e.g., invalid genre)
        print("\n Failed to add book. Check details.")


# --- 3. Main Loop ---
def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            # You would create a sub-menu here for Book CRUD operations
            print("\nBook Operations selected. (You'll implement a submenu here)")

        elif choice == '2':
            # You would create a sub-menu here for Member CRUD operations
            print("\nMember Operations selected. (You'll implement a submenu here)")

        elif choice == '3':
            # Handle Borrow/Return (You will create a function like handle_borrow_return)
            print("\nBorrow/Return selected. (You'll implement the functionality here)")

        elif choice == '4':
            # Example of 'Read' functionality: printing the global data
            print("\n--- Current Books ---")
            for isbn, book in mainoperations.books.items():
                print(f"ISBN: {isbn} | Title: {book['title']} | Copies Available: {book['total_copies']}")

            print("\n--- Current Members ---")
            for member in mainoperations.members:
                print(f"ID: {member['member_id']} | Name: {member['name']} | Borrowed: {len(member['borrowed_books'])}")

        elif choice == '0':
            print("Exiting Library Management System. Goodbye! ")
            break

        # Call the example handler for demonstration
        elif choice == 'test_add':  # Hidden option for quick testing
            handle_add_book()

        else:
            print("Invalid choice. Please enter a number from the menu.")


if "_name_" == "_main_":
    # Optional: Preload some data for easier testing
    mainoperations.add_book("9781234567890", "Python Fun", "A. Programmer", "Sci-Fi", 3)
    mainoperations.add_member("M100", "Charlie Brown", "charlie@peanuts.com")

    main()


# --- 2. Input Handlers (Continued from main.py) ---
# ... (after handle_add_book) ...

def handle_search_books():
    """Collects input for searching books and displays matching results."""
    print("\n--- Search Books ---")

    # 1. Get search criteria
    print("Search by:")
    print("  1. Title")
    print("  2. Author")

    search_choice = input("Enter search field (1 or 2): ").strip()

    if search_choice == '1':
        by_field = "title"
    elif search_choice == '2':
        by_field = "author"
    else:
        print(" Invalid choice. Defaulting search to Title.")
        by_field = "title"  # Defaulting as per assignment requirement

    # 2. Get search query
    query = input(f"Enter search term (partial match, case-insensitive) for {by_field}: ").strip()

    if not query:
        print(" Search query cannot be empty.")
        return

    # 3. Call the core operation function
    matching_books = mainoperations.search_books(query, by=by_field)

    # 4. Display results
    print("\n--- Search Results ---")
    if matching_books:
        print(f"Found {len(matching_books)} book(s) matching '{query}' by {by_field}:")
        print("-" * 50)

        for book in matching_books:
            # Note: We include the 'isbn' since the search_books function adds it to the dictionary
            # The 'book' dictionary here is a merged dict of {"isbn": "...", "title": "..."}
            print(f"  ISBN: {book['isbn']}")
            print(f"  Title: {book['title']}")
            print(f"  Author: {book['author']}")
            print(f"  Genre: {book['genre']}")
            print(f"  Available Copies: {book['total_copies']}")
            print("-" * 50)
    else:
        print(f" No books found matching '{query}' by {by_field}.")


# --- Integration into main() ---
# In your main() function, you would integrate this into a 'Book Operations' submenu.

def book_operations_menu():
    while True:
        print("\n--- Book Operations ---")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Update Book")
        print("4. Delete Book")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            handle_add_book()
        elif choice == '2':
            handle_search_books()  # <-- Call the new search function here
        elif choice == '3':
            print("--- (Implement handle_update_book here) ---")
        elif choice == '4':
            print("--- (Implement handle_delete_book here) ---")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


# Update the main function to call the submenu
def main_updated():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            book_operations_menu()  # <-- New integration point
        # ... (other choices) ...
        # ...
        elif choice == '0':
            print("Exiting Library Management System. Goodbye! ")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


def handle_update_book():
    """Prompts for book details to update and calls the operations function."""
    print("\n--- Update Existing Book ---")
    isbn_to_update = input("Enter the ISBN of the book to update: ").strip()

    # Pre-check if the book exists
    if isbn_to_update not in mainoperations.books:
        print(f" Error: Book with ISBN {isbn_to_update} not found.")
        return

    book = mainoperations.books[isbn_to_update]

    print(f"\nCurrently updating: {book['title']} by {book['author']}")
    print("Which field would you like to update? (Press Enter to skip a field)")

    # Collect new values (None indicates no change)
    new_title = input(f"New Title (Current: {book['title']}): ").strip() or None
    new_author = input(f"New Author (Current: {book['author']}): ").strip() or None

    # Genre validation guidance
    genre_prompt = f"New Genre (Current: {book['genre']}). Valid options: {list(mainoperations.GENRES)}: "
    new_genre = input(genre_prompt).strip() or None

    # Handle total_copies separately as it must be an integer
    new_copies_str = input(f"New Total Copies (Current: {book['total_copies']}): ").strip()
    new_copies = None
    if new_copies_str:
        try:
            new_copies = int(new_copies_str)
        except ValueError:
            print(" Update Failed: Total copies must be an integer.")
            return

    # Call the core update function
    if mainoperations.update_book(
            isbn=isbn_to_update,
            title=new_title,
            author=new_author,
            genre=new_genre,
            total_copies=new_copies
    ):
        print("\n Book updated successfully!")
    else:
        # operations.py already handles and prints specific error messages (e.g., genre invalid)
        print("\n Failed to update book. Please review the constraints and input.")