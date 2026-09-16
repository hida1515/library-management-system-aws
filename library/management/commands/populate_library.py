from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from library.models import Book, Member, Borrowing


class Command(BaseCommand):
    help = 'Populates the library database with realistic fictional sample data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding sample library data..."))

        # Clear existing sample data if desired
        Borrowing.objects.all().delete()
        Book.objects.all().delete()
        Member.objects.all().delete()

        # Create Books
        books_data = [
            {
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "isbn": "978-0132350884",
                "category": "Computer Science",
                "publisher": "Prentice Hall",
                "publication_year": 2008,
                "quantity": 5,
                "available_quantity": 3
            },
            {
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen, Charles E. Leiserson",
                "isbn": "978-0262033848",
                "category": "Computer Science",
                "publisher": "MIT Press",
                "publication_year": 2009,
                "quantity": 4,
                "available_quantity": 2
            },
            {
                "title": "Database System Concepts",
                "author": "Abraham Silberschatz, Henry F. Korth",
                "isbn": "978-0078022159",
                "category": "Database Engineering",
                "publisher": "McGraw-Hill",
                "publication_year": 2019,
                "quantity": 6,
                "available_quantity": 4
            },
            {
                "title": "Modern Operating Systems",
                "author": "Andrew S. Tanenbaum",
                "isbn": "978-0133591620",
                "category": "Systems & Networking",
                "publisher": "Pearson",
                "publication_year": 2014,
                "quantity": 3,
                "available_quantity": 1
            },
            {
                "title": "Python Crash Course: A Hands-On Project-Based Intro",
                "author": "Eric Matthes",
                "isbn": "978-1593279288",
                "category": "Programming",
                "publisher": "No Starch Press",
                "publication_year": 2019,
                "quantity": 5,
                "available_quantity": 5
            },
            {
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
                "isbn": "978-0201633610",
                "category": "Software Architecture",
                "publisher": "Addison-Wesley",
                "publication_year": 1994,
                "quantity": 4,
                "available_quantity": 2
            }
        ]

        created_books = []
        for b_data in books_data:
            book = Book.objects.create(**b_data)
            created_books.append(book)
            self.stdout.write(self.style.SUCCESS(f"  + Added Book: {book.title}"))

        # Create Members
        members_data = [
            {
                "name": "Alice Vance",
                "email": "alice.vance@university.edu",
                "phone": "+1-555-0142",
                "membership_id": "LIB-2026-001",
                "address": "104 Campus View Drive, Bldg A",
                "joined_date": timezone.now().date() - timedelta(days=120)
            },
            {
                "name": "Bob Martin",
                "email": "bob.martin@university.edu",
                "phone": "+1-555-0188",
                "membership_id": "LIB-2026-002",
                "address": "402 Student Housing West",
                "joined_date": timezone.now().date() - timedelta(days=90)
            },
            {
                "name": "Charlie Davis",
                "email": "charlie.davis@university.edu",
                "phone": "+1-555-0193",
                "membership_id": "LIB-2026-003",
                "address": "12 Science Hall Plaza",
                "joined_date": timezone.now().date() - timedelta(days=60)
            },
            {
                "name": "Diana Prince",
                "email": "diana.prince@university.edu",
                "phone": "+1-555-0155",
                "membership_id": "LIB-2026-004",
                "address": "88 Academic Lane",
                "joined_date": timezone.now().date() - timedelta(days=30)
            }
        ]

        created_members = []
        for m_data in members_data:
            member = Member.objects.create(**m_data)
            created_members.append(member)
            self.stdout.write(self.style.SUCCESS(f"  + Registered Member: {member.name}"))

        # Create Borrowings
        today = timezone.now().date()

        # Active Borrowing 1 (Due in future)
        b1 = Borrowing.objects.create(
            book=created_books[0],
            member=created_members[0],
            issue_date=today - timedelta(days=5),
            due_date=today + timedelta(days=9),
            status='borrowed'
        )

        # Active Borrowing 2 (Overdue)
        b2 = Borrowing.objects.create(
            book=created_books[1],
            member=created_members[1],
            issue_date=today - timedelta(days=20),
            due_date=today - timedelta(days=6),
            status='borrowed'
        )

        # Returned Borrowing
        b3 = Borrowing.objects.create(
            book=created_books[2],
            member=created_members[2],
            issue_date=today - timedelta(days=25),
            due_date=today - timedelta(days=11),
            return_date=today - timedelta(days=12),
            status='returned'
        )

        # Active Borrowing 3
        b4 = Borrowing.objects.create(
            book=created_books[3],
            member=created_members[3],
            issue_date=today - timedelta(days=2),
            due_date=today + timedelta(days=12),
            status='borrowed'
        )

        self.stdout.write(self.style.SUCCESS("Sample data population completed successfully!"))
