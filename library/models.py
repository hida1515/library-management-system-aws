from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_quantity > 0


class Member(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    membership_id = models.CharField(max_length=50, unique=True, verbose_name="Membership ID")
    address = models.TextField(blank=True, null=True)
    joined_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.membership_id})"


class Borrowing(models.Model):
    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowings')
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.title} issued to {self.member.name}"

    @property
    def is_overdue(self):
        if self.status == 'borrowed' and self.due_date < timezone.now().date():
            return True
        return False
