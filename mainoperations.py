# 1. Global Data Structures

# Books Dictionary:
books = {}

# Members List: List of Member Dictionaries
members = []

# Genres Tuple: Fixed categories for validation
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography", "Fantasy")


# Functions

def _get_member(member_id):
    """Internal helper to find a member dictionary by ID."""
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None


def _is_valid_genre(genre):
    """Internal helper to check if a genre is in the global GENRES tuple."""
    return genre in GENRES


#  (CRUD Operations)

#  we Create

def add_book(isbn, title, author, genre, total_copies):
    """Add a new book if ISBN is unique and genre is valid."""
    if isbn in books:
        print(f"Error: Book with ISBN {isbn} already exists.")
        return False
    if not _is_valid_genre(genre):
        print(f"Error: Invalid genre '{genre}'. Must be one of {list(GENRES)}.")
        return False
    if not isinstance(total_copies, int) or total_copies < 0:
        print("Error: Total copies must be a non-negative integer.")
        return False

    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        # Storing original_copies for delete constraint validation
        "original_copies": total_copies
    }
    return True


def add_member(member_id, name, email):
    """Add a new member if member_id is unique."""
    if _get_member(member_id):
        print(f"Error: Member with ID {member_id} already exists.")
        return False

    new_member = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []  # Initialize as an empty list of ISBNs
    }
    members.append(new_member)
    return True


## Read

def search_books(query, by="title"):
    """Search books by title or author (case-insensitive, partial matches)."""

    # Ensure search type is valid, default to 'title'
    if by not in ["title", "author"]:
        by = "title"

        # Normalize the query for case-insensitive matching
    normalized_query = query.lower()

    matching_books = []
    # Iterate through the values (book dictionaries) in the books global dictionary
    for isbn, book_details in books.items():
        # Check the specified field (title or author)
        if normalized_query in book_details[by].lower():
            # Create a copy including the ISBN for the result list
            result_book = {"isbn": isbn}
            result_book.update(book_details)
            matching_books.append(result_book)

    return matching_books


# Update

def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """Update specified fields of a book if it exists and genre is valid."""
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]

    if title is not None:
        book["title"] = title
    if author is not None:
        book["author"] = author
    if genre is not None:
        if not _is_valid_genre(genre):
            print(f"Error: Invalid genre '{genre}'. Update failed.")
            return False
        book["genre"] = genre

    if total_copies is not None:
        if not isinstance(total_copies, int) or total_copies < 0:
            print("Error: Total copies must be a non-negative integer. Update failed.")
            return False

        # Calculate difference to update the original_copies count as well.
        # This keeps the 'delete_book' constraint relevant.
        borrowed_count = book["original_copies"] - book["total_copies"]

        # Ensure the new total_copies is not less than the currently borrowed count
        if total_copies < borrowed_count:
            print(f"Error: Cannot set total copies to {total_copies}. {borrowed_count} copies are currently borrowed.")
            return False

        book["total_copies"] = total_copies
        book["original_copies"] = total_copies  # Reset original_copies to the new total

    return True


def update_member(member_id, name=None, email=None):
    """Update specified fields of a member if they exist."""
    member = _get_member(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    if name is not None:
        member["name"] = name
    if email is not None:
        member["email"] = email

    return True


# Delete

def delete_book(isbn):
    """Remove a book if it exists and all copies are available."""
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    book = books[isbn]

    # This means total_copies must equal the original number of copies.
    if book["total_copies"] != book["original_copies"]:
        print(f"Error: Cannot delete book {isbn}. Some copies are currently borrowed.")
        return False

    del books[isbn]
    return True


def delete_member(member_id):
    """Remove a member if they exist and have no borrowed books."""
    member = _get_member(member_id)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    # Constraint: Must have no borrowed books.
    if member["borrowed_books"]:
        print(f"Error: Cannot delete member {member_id}. They have borrowed books: {member['borrowed_books']}.")
        return False

    members.remove(member)
    return True


# Borrow/Return

def borrow_book(isbn, member_id):
    """Borrows a book if available and member has room."""
    book = books.get(isbn)
    member = _get_member(member_id)

    if not book:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    if book["total_copies"] <= 0:
        print(f"Error: No copies of book {isbn} are currently available.")
        return False

    # Max borrowed books constraint
    if len(member["borrowed_books"]) >= 3:
        print(f"Error: Member {member_id} has reached the borrowing limit (3 books).")
        return False

    # Prevent borrowing the same book twice
    if isbn in member["borrowed_books"]:
        print(f"Error: Member {member_id} has already borrowed a copy of book {isbn}.")
        return False

    # Execute borrow transaction
    book["total_copies"] -= 1
    member["borrowed_books"].append(isbn)
    return True


def return_book(isbn, member_id):
    """Returns a book if it was actually borrowed by the member."""
    book = books.get(isbn)
    member = _get_member(member_id)

    if not book:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False

    if isbn not in member["borrowed_books"]:
        print(f"Error: Book {isbn} was not borrowed by member {member_id}.")
        return False

    # Execute return transaction
    book["total_copies"] += 1
    member["borrowed_books"].remove(isbn)
    return True