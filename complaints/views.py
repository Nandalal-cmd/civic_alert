import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Complaint, Notification
from .forms import CitizenRegistrationForm
from .utils import haversine

# 1. Public Home Page
def home(request):
    return render(request, 'complaints/home.html')

# 2. Registration Logic
def register_view(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'complaints/register.html', {'form': form})

# 3. Login Logic
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'complaints/login.html', {'form': form})

# 4. Logout Logic
def logout_view(request):
    logout(request)
    return redirect('home')

# 5. Citizen Dashboard
@login_required
def dashboard(request):
    duplicate_complaint = None
    duplicate_distance = None
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if category and description and latitude and longitude:
            # Duplicate Detection
            existing_complaints = Complaint.objects.filter(
                category=category, 
                status__in=['Pending', 'In Progress']
            )
            for existing in existing_complaints:
                if existing.latitude and existing.longitude:
                    dist = haversine(latitude, longitude, existing.latitude, existing.longitude)
                    if dist < 50: # 50 meters radius
                        duplicate_complaint = existing
                        duplicate_distance = round(dist, 1) # Store rounded distance
                        break
            
            if not duplicate_complaint:
                Complaint.objects.create(
                    citizen=request.user,
                    category=category,
                    description=description,
                    image=image if image else None,
                    latitude=latitude if latitude else None,
                    longitude=longitude if longitude else None
                )
                messages.success(request, "Complaint submitted successfully!")
                return redirect('dashboard')
            else:
                messages.warning(request, f"A similar issue has already been reported nearby ({duplicate_distance}m away)!")
        else:
            messages.error(request, "Please fill in all fields and pick a location on the map.")
    
    from django.db.models import Q
    user_complaints = Complaint.objects.filter(
        Q(citizen=request.user) | Q(upvoters=request.user)
    ).distinct().order_by('-created_at')
    
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications.update(is_read=True)

    return render(request, 'complaints/dashboard.html', {
        'complaints': user_complaints,
        'notifications': notifications,
        'duplicate_complaint': duplicate_complaint,
        'duplicate_distance': duplicate_distance
    })

@login_required
def upvote_complaint(request, complaint_id):
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        if request.user not in complaint.upvoters.all():
            complaint.upvoters.add(request.user)
            complaint.upvotes += 1
            complaint.save()
            messages.success(request, "Thank you for upvoting! This helps prioritize the issue.")
        else:
            messages.info(request, "You have already upvoted this complaint.")
    except Complaint.DoesNotExist:
        messages.error(request, "Complaint not found.")
    
    return redirect('dashboard')

# 6. Admin Panel
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                next_url = request.GET.get('next', 'admin_dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Access Denied: Regular users cannot use the staff portal.")
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'complaints/admin_login.html', {'form': form})

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Stats
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='Pending').count(),
        'in_progress': complaints.filter(status='In Progress').count(),
        'resolved': complaints.filter(status='Resolved').count(),
    }
    
    # Locations for the global map (Only show active issues)
    locations = []
    for c in complaints:
        if c.latitude and c.longitude and c.status != 'Resolved':
            locations.append({
                'id': c.id,
                'lat': float(c.latitude),
                'lng': float(c.longitude),
                'category': c.category,
                'status': c.status,
                'image_url': c.image.url if c.image else None,
                'priority': c.priority
            })

    return render(request, 'complaints/admin_dashboard.html', {
        'complaints': complaints,
        'stats': stats,
        'locations': json.dumps(locations)
    })

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_update_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        admin_comment = request.POST.get('admin_comment')
        
        if status:
            complaint.status = status
        if priority:
            complaint.priority = priority
        if admin_comment:
            complaint.admin_comment = admin_comment
            
        complaint.save()
        
        # Notify user
        Notification.objects.create(
            user=complaint.citizen,
            complaint=complaint,
            message=f"Update: Your {complaint.category} report has been updated to '{status}'."
        )
        
        messages.success(request, f"Complaint #{complaint_id} updated successfully.")
    
    return redirect('admin_dashboard')