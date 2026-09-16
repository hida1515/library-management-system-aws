from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Book, Member, Borrowing
from .forms import BookForm, MemberForm, BorrowingForm


def dashboard(request):
    total_books = Book.objects.aggregate(total=Sum('quantity'))['total'] or 0
    available_books = Book.objects.aggregate(available=Sum('available_quantity'))['available'] or 0
    borrowed_books = total_books - available_books
    total_members = Member.objects.count()
    recent_activity = Borrowing.objects.select_related('book', 'member').all()[:6]

    context = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': max(0, borrowed_books),
        'total_members': total_members,
        'recent_activity': recent_activity,
    }
    return render(request, 'library/dashboard.html', context)


# ==================== BOOK VIEWS ====================

def book_list(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(publisher__icontains=query)
        )

    if category_filter:
        books = books.filter(category__iexact=category_filter)

    categories = Book.objects.values_list('category', flat=True).distinct().order_by('category')

    context = {
        'books': books,
        'query': query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    borrowings = book.borrowings.select_related('member').all()[:10]
    return render(request, 'library/book_detail.html', {'book': book, 'borrowings': borrowings})


def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' created successfully!")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Add New Book'})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' updated successfully!")
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'title': f"Edit Book: {book.title}", 'book': book})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f"Book '{title}' was deleted successfully.")
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})


# ==================== MEMBER VIEWS ====================

def member_list(request):
    query = request.GET.get('q', '').strip()
    members = Member.objects.all()

    if query:
        members = members.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(membership_id__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, 'library/member_list.html', {'members': members, 'query': query})


def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    active_borrowings = member.borrowings.select_related('book').filter(status='borrowed')
    past_borrowings = member.borrowings.select_related('book').filter(status='returned')[:10]
    return render(request, 'library/member_detail.html', {
        'member': member,
        'active_borrowings': active_borrowings,
        'past_borrowings': past_borrowings
    })


def member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f"Member '{member.name}' added successfully!")
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'library/member_form.html', {'form': form, 'title': 'Register New Member'})


def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            messages.success(request, f"Member '{member.name}' updated successfully!")
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'library/member_form.html', {'form': form, 'title': f"Edit Member: {member.name}", 'member': member})


def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f"Member '{name}' was deleted successfully.")
        return redirect('member_list')
    return render(request, 'library/member_confirm_delete.html', {'member': member})


# ==================== BORROWING VIEWS ====================

def borrowing_list(request):
    status_filter = request.GET.get('status', '').strip()
    borrowings = Borrowing.objects.select_related('book', 'member').all()

    today = timezone.now().date()
    # Update overdue status in query results dynamically
    for record in borrowings:
        if record.status == 'borrowed' and record.due_date < today:
            record.status = 'overdue'

    if status_filter:
        borrowings = [b for b in borrowings if b.status == status_filter]

    context = {
        'borrowings': borrowings,
        'status_filter': status_filter,
        'today': today,
    }
    return render(request, 'library/borrowing_list.html', context)


def borrow_issue(request):
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            borrowing = form.save(commit=False)
            book = borrowing.book
            
            # Check availability logic
            if book.available_quantity <= 0:
                messages.error(request, f"Cannot issue '{book.title}'. No copies available.")
                return redirect('borrow_issue')

            # Decrease available_quantity
            book.available_quantity -= 1
            book.save()

            borrowing.status = 'borrowed'
            borrowing.save()

            messages.success(request, f"Book '{book.title}' successfully issued to {borrowing.member.name}!")
            return redirect('borrowing_list')
    else:
        form = BorrowingForm()

    return render(request, 'library/borrowing_form.html', {'form': form, 'title': 'Issue Book'})


def borrow_return(request, pk):
    borrowing = get_object_or_404(Borrowing, pk=pk)

    if borrowing.status == 'returned':
        messages.warning(request, f"This book was already returned on {borrowing.return_date}.")
        return redirect('borrowing_list')

    book = borrowing.book
    book.available_quantity += 1
    if book.available_quantity > book.quantity:
        book.available_quantity = book.quantity
    book.save()

    borrowing.return_date = timezone.now().date()
    borrowing.status = 'returned'
    borrowing.save()

    messages.success(request, f"Book '{book.title}' returned successfully by {borrowing.member.name}!")
    return redirect('borrowing_list')
