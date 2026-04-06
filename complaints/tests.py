from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Complaint, Notification
from .forms import CitizenRegistrationForm


class CitizenRegistrationFormTests(TestCase):
    """Test email validation in registration form."""
    
    def test_unique_email_enforcement(self):
        """Ensure two users cannot register with the same email."""
        User.objects.create_user(username='user1', email='test@example.com', password='pass123')
        
        form = CitizenRegistrationForm(data={
            'username': 'user2',
            'email': 'test@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('This email is already in use', str(form.errors))
    
    def test_valid_registration(self):
        """Ensure valid registration data passes validation."""
        form = CitizenRegistrationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        self.assertTrue(form.is_valid())


class ComplaintModelTests(TestCase):
    """Test Complaint model creation and fields."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123')
    
    def test_complaint_creation(self):
        """Ensure complaint is created with correct fields."""
        complaint = Complaint.objects.create(
            citizen=self.user,
            category='Roads',
            description='Pothole on Main Street',
            status='Pending'
        )
        self.assertEqual(complaint.category, 'Roads')
        self.assertEqual(complaint.status, 'Pending')
        self.assertEqual(complaint.citizen, self.user)
    
    def test_complaint_status_choices(self):
        """Ensure complaint respects status choices."""
        valid_statuses = [choice[0] for choice in Complaint.STATUS_CHOICES]
        self.assertIn('Pending', valid_statuses)
        self.assertIn('In Progress', valid_statuses)
        self.assertIn('Resolved', valid_statuses)


class DashboardViewTests(TestCase):
    """Test dashboard view authentication and functionality."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123')
    
    def test_dashboard_requires_login(self):
        """Ensure dashboard redirects unauthenticated users."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)
    
    def test_dashboard_complaint_submission(self):
        """Ensure POST request creates a complaint."""
        self.client.login(username='testuser', password='pass123')
        response = self.client.post('/dashboard/', {
            'category': 'Water',
            'description': 'Broken water pipe',
            'latitude': '27.7172',
            'longitude': '85.3240',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        complaint = Complaint.objects.filter(citizen=self.user).first()
        self.assertIsNotNone(complaint)
        self.assertEqual(complaint.category, 'Water')
        self.assertEqual(complaint.description, 'Broken water pipe')
    
    def test_dashboard_marks_notifications_as_read(self):
        """Ensure notifications are marked as read when dashboard is viewed."""
        self.client.login(username='testuser', password='pass123')
        
        complaint = Complaint.objects.create(citizen=self.user, category='Roads', description='Test')
        notification = Notification.objects.create(
            user=self.user,
            complaint=complaint,
            message='Test notification',
            is_read=False
        )
        
        self.client.get('/dashboard/')
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
