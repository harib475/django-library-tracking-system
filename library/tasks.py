from celery import shared_task
from django.utils import timezone

from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


# Implement a Celery task that runs daily to check for overdue book loans and sends email notifications to members.
# 📍 Requirements:
# Update the Loan Model:
# Add a due_date field with a default value set to 14 days from the loan_date.
# Create a Celery Periodic Task:
# Define a task named check_overdue_loans that executes daily.
# The task should:
# Query all loans where is_returned is False and due_date is past.
# Send an email reminder to each member with overdue books.
# Apply Migrations:
# Make and apply the necessary database migrations to accommodate the updated model.
# Verify Task Execution:
# Test the Celery task to ensure it correctly identifies overdue loans and sends notifications.
#
#
# Configure Celery Beat Scheduler (optional):
# Only take on this task if you are familiar with Celery Beat, this task can be time consuming.
# Ensure that the check_overdue_loans task is scheduled to run daily using Celery Beat.
# Update docker-compose.yml:
# Add a celery-beat service to handle the periodic tasks.



@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date=timezone.now().date())
    for loan in overdue_loans:
        send_mail(
            subject='Overdue Book Reminder',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{loan.book.title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[loan.member.user.email],
            fail_silently=False,
        )