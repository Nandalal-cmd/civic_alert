from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Roads', 'Roads'),
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Traffic', 'Traffic'),
        ('Pollution', 'Pollution'),
        ('Others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    id = models.AutoField(primary_key=True, db_column='complaint_id')
    citizen = models.ForeignKey(User, related_name='complaints', on_delete=models.CASCADE, db_column='reporter_id')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/', blank=True, null=True, db_column='image_url')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    admin_comment = models.TextField(blank=True, null=True, db_column='admin_notes')
    upvoters = models.ManyToManyField(User, related_name='upvoted_complaints', blank=True, db_table='complaint_upvotes')
    
    # Location coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    upvotes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'complaint'

    def __str__(self):
        return f"{self.category} - {self.citizen.username}"

class Notification(models.Model):
    id = models.AutoField(primary_key=True, db_column='notification_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='target_citizen_id')
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, db_column='linked_complaint_id')
    message = models.TextField(db_column='message_text')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'

    def __str__(self):
        return f"Notification for {self.user.username}"