# test_code.py or added to main.py

import mainoperations

# Helper function to find a member's current book count
def _get_borrowed_count(member_id):
    """Returns the number of books a member currently has, or 0 if not found."""
    member = mainoperations._get_member(member_id)
    return len(member['borrowed_books']) if member else 0

def run_constraint_tests():
    """Runs a series of tests to validate all constraints and core logic."""
    print("\n" + "="*50)
    print("         RUNNING CONSTRAINT VALIDATION TESTS")
    print("="*50)

    # Reset data structures for clean testing environment
    mainoperations.books = {}
    mainoperations.members = []
    
    # --- SETUP: Add valid records for testing ---
    mainoperations.add_book("978-A", "The Test Book", "Test Author", "Fiction", 2)
    mainoperations.add_book("978-B", "Sci-Fi Trial", "Trial Author", "Sci-Fi", 1)
    mainoperations.add_book("978-C", "Limit Test 1", "L Author", "Mystery", 1)
    mainoperations.add_book("978-D", "Limit Test 2", "L Author", "Mystery", 1)
    mainoperations.add_book("978-E", "Limit Test 3", "L Author", "Mystery", 1)
    mainoperations.add_member("M001", "Alice Test", "alice@test.com")
    mainoperations.add_member("M002", "Bob Test", "bob@test.com")
    print("\nSETUP COMPLETE: Books 978-A to 978-E and Members M001, M002 created.")
    print("-" * 50)


    # ==========================================================
    # 1. ADD/UPDATE CONSTRAINTS (T01)
    # ==========================================================
    print("TEST 1: Add/Update Constraints")
    
    # T01a: Test invalid genre (add_book)
    result_a = mainoperations.add_book("978-FAIL-A", "Bad Genre", "A", "Horror", 1)
    print(f"  T01a (Invalid Genre 'Horror'): Expected False, Got {result_a}")
    
    # T01b: Test unique ISBN constraint (add_book)
    result_b = mainoperations.add_book("978-A", "Duplicate Book", "Test Author", "Fiction", 1)
    print(f"  T01b (Duplicate ISBN '978-A'): Expected False, Got {result_b}")
    
    # T01c: Test valid genre check on update
    result_c = mainoperations.update_book("978-A", genre="INVALID")
    print(f"  T01c (Update to Invalid Genre): Expected False, Got {result_c}")
    
    print("-" * 50)

    # ==========================================================
    # 2. BORROW/AVAILABILITY CONSTRAINTS (T02, T03)
    # ==========================================================
    print("TEST 2: Borrowing Limits and Availability")

    # T02: Test book availability (0 copies available)
    # Borrow the only copy of 978-B
    mainoperations.borrow_book("978-B", "M001")
    # Attempt to borrow the now unavailable book
    result_d = mainoperations.borrow_book("978-B", "M002")
    print(f"  T02 (Book 978-B, now 0 copies): Expected False, Got {result_d}")
    
    # T03: Test member borrowing limit (max 3)
    mainoperations.borrow_book("978-C", "M002") # 1st book
    mainoperations.borrow_book("978-D", "M002") # 2nd book
    mainoperations.borrow_book("978-E", "M002") # 3rd book
    # Attempt to borrow the 4th book
    result_e = mainoperations.borrow_book("978-A", "M002")
    count_e = _get_borrowed_count("M002")
    print(f"  T03 (Member M002, trying 4th book): Expected False, Got {result_e} (Count: {count_e})")
    
    print("-" * 50)


    # ==========================================================
    # 3. RETURN CONSTRAINTS (T04)
    # ==========================================================
    print("TEST 3: Return Integrity")

    # T04: Test returning a book that wasn't borrowed
    # M001 borrowed 978-B. Try to return 978-C (not borrowed by M001).
    result_f = mainoperations.return_book("978-C", "M001")
    print(f"  T04 (M001 returns unborrowed 978-C): Expected False, Got {result_f}")
    
    print("-" * 50)


    # ==========================================================
    # 4. DELETION CONSTRAINTS (T05, T06)
    # ==========================================================
    print("TEST 4: Deletion Safety and Update Integrity")

    # T05a: Test delete_book constraint (copies outstanding)
    # 978-B has 1 copy borrowed by M001.
    result_g = mainoperations.delete_book("978-B")
    print(f"  T05a (Delete 978-B, 1 copy out): Expected False, Got {result_g}")
    
    # T05b: Test delete_member constraint (books outstanding)
    # M002 has 3 books borrowed.
    result_h = mainoperations.delete_member("M002")
    print(f"  T05b (Delete M002, 3 books out): Expected False, Got {result_h}")

    # T06: Test update_book to violate loan count
    # Book 978-A has 2 total copies, 0 borrowed (0 is less than 2)
    # Let M001 borrow one more book (978-A)
    mainoperations.borrow_book("978-A", "M001")
    # Now, 978-A has 1 copy available, 1 copy borrowed (original was 2).
    # Try to reduce total copies to 0 (which is < 1 borrowed copy)
    result_i = mainoperations.update_book("978-A", total_copies=0)
    print(f"  T06 (Update 978-A total to 0, 1 borrowed): Expected False, Got {result_i}")

    # --- CLEANUP AND FINAL SUCCESS TEST ---
    print("\n--- Final Cleanup & Success Test ---")
    
    # Allow deletion by returning M002's books
    mainoperations.return_book("978-C", "M002")
    mainoperations.return_book("978-D", "M002")
    mainoperations.return_book("978-E", "M002")
    
    # T05b SUCCESS: Delete M002 after returns
    result_j = mainoperations.delete_member("M002")
    print(f"  T05b Success (Delete M002 cleared): Expected True, Got {result_j}")

    print("\n" + "="*50)
    print("         TEST SUITE COMPLETE")
    print("="*50)

# Call this function to run all tests
# run_constraint_tests()