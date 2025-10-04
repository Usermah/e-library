from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Member, Circulation
from .forms import BookForm, MemberForm


@login_required
def dashboard(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    books_issued = Circulation.objects.count()
    overdue = Circulation.objects.filter(
        return_date__isnull=True, 
        due_date__lt=timezone.now().date()
    ).count()

    recent_books = Book.objects.order_by("-added_on")[:5]

    return render(request, "dashboard.html", {
        "total_books": total_books,
        "total_members": total_members,
        "books_issued": books_issued,
        "overdue": overdue,
        "recent_books": recent_books,
    })


@login_required
def catalog(request):
    books = Book.objects.all().order_by("-added_on")
    return render(request, "catalog.html", {"books": books})


@login_required
def members(request):
    members = Member.objects.all().order_by("-joined_on")
    return render(request, "members.html", {"members": members})


@login_required
def circulation(request):
    loans = Circulation.objects.select_related("book", "member").all().order_by("-issue_date")
    return render(request, "circulation.html", {"loans": loans})


@login_required
def reports(request):
    return render(request, "reports.html")


@login_required
def settings(request):
    return render(request, "settings.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# Add new book
@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        form = BookForm()
    return render(request, "add_book.html", {"form": form})


#  Add new member
@login_required
def add_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("members")
    else:
        form = MemberForm()
    return render(request, "add_member.html", {"form": form})
