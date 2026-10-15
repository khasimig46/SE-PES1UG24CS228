"""Library catalog management module."""

import csv
import hashlib
import os
import secrets

FINE_PER_DAY = 2.0

catalog = {
    "B01": {"title": "Clean Code", "copies": 3, "total": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1, "total": 1},
    "B03": {"title": "Design Patterns", "copies": 2, "total": 2},
}


def issue_book(book_id, patron, active_issues=None):
    """Issue one copy of a book. Return True on success, False otherwise."""
    book = catalog.get(book_id)
    if book is None or book["copies"] <= 0:
        return False
    book["copies"] -= 1
    if active_issues is not None:
        active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Accept a returned copy. Reject unknown books and surplus returns."""
    book = catalog.get(book_id)
    if book is None or book["copies"] >= book["total"]:
        return False
    book["copies"] += 1
    return True


def check_availability(book_id):
    """Return True if at least one copy of the book is on the shelf."""
    book = catalog.get(book_id)
    return book is not None and book["copies"] > 0


def calculate_fine(days_overdue, daily_rate=FINE_PER_DAY):
    """Return the fine for a number of overdue days."""
    if days_overdue < 0:
        raise ValueError("days_overdue cannot be negative")
    return days_overdue * daily_rate


def generate_patron_hash(patron_id):
    """Return a SHA-256 hex digest identifying a patron."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Return a cryptographically secure 4-digit PIN."""
    return secrets.randbelow(9000) + 1000


def export_catalog(filename="catalog_export.csv"):
    """Write the catalog to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["book_id", "title", "copies", "total"])
        for book_id, book in catalog.items():
            writer.writerow([book_id, book["title"], book["copies"],
                             book["total"]])
    print("Catalog backup exported to:", filename)


def main():
    """Run a short demonstration of the catalog system."""
    librarian_key = os.environ.get("LIBRARIAN_KEY")
    issue_book("B01", "P101")
    print("Return of never-issued B02 accepted:", return_book("B02"))
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian key configured:", librarian_key is not None)


if __name__ == "__main__":
    main()
