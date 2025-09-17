from django.db import models


# Book Catalog
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True)  # allow blanks
    isbn = models.CharField(max_length=20, unique=True)
    published_date = models.DateField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Library Members
class Member(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)  # allow blanks
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Member"


# Circulation (book loans)
class Circulation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        from django.utils import timezone
        return self.return_date is None and self.due_date < timezone.now().date()

    def __str__(self):
        return f"{self.book.title} → {self.member.name if self.member.name else 'Member'}"
