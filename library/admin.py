from django.contrib import admin
from .models import Book, Member, Borrowing


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available_quantity', 'publication_year')
    search_fields = ('title', 'author', 'isbn', 'category', 'publisher')
    list_filter = ('category', 'publication_year')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'name', 'email', 'phone', 'joined_date')
    search_fields = ('name', 'email', 'membership_id', 'phone')
    list_filter = ('joined_date',)


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'return_date', 'status')
    search_fields = ('book__title', 'member__name', 'member__membership_id')
    list_filter = ('status', 'issue_date', 'due_date')
