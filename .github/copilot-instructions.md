# Copilot / AI Agent Instructions for CivicAlert

This file contains concise, actionable instructions for AI coding agents working on the CivicAlert Django app. Keep suggestions narrowly targeted to the repository's existing patterns and files.

## Project overview
- Single Django project (`civicalert_project`) with one app: `complaints`.
- Purpose: allow citizens to register, submit complaints with optional images, and receive notifications.
- DB: configured to use MySQL in `civicalert_project/settings.py` (DB: `city_db`, user `root`).
- Media files are saved to `MEDIA_ROOT` (project `media/` folder) and served in `civicalert_project/urls.py` via `static()` (dev only).

## Key files and patterns (examples)
- `civicalert_project/settings.py` — primary runtime configuration: DB credentials, `DEBUG=True`, `MEDIA_ROOT`, `LOGIN_REDIRECT_URL`.
- `complaints/models.py` — `Complaint` and `Notification` models. Look for `CATEGORY_CHOICES` and `STATUS_CHOICES` when adding features that interact with complaint classification.
  - Example: `citizen = models.ForeignKey(User, related_name='complaints', on_delete=models.CASCADE)` (use `.complaints` reverse lookup).
- `complaints/forms.py` — `CitizenRegistrationForm` extends `UserCreationForm` and enforces unique email via `clean_email()`.
- `complaints/views.py` — simple auth flows: `register_view`, `login_view`, `logout_view`, and `dashboard` (dashboard uses `Complaint.objects.filter(citizen=request.user)` and `Notification.objects.filter(user=request.user, is_read=False)`).
- Templates: app-level templates at `complaints/templates/complaints/` (e.g., `dashboard.html` uses Tailwind CDN and reads `complaints` and `notifications` context variables).

## Developer workflows (concrete commands)
- Create a virtual env and install the Django version referenced in the project header: e.g.,
  - python -m venv .venv
  - .\.venv\Scripts\activate
  - pip install django==6.0.1
  - pip install mysqlclient  # or equivalent MySQL DB driver
- Database setup (matches `settings.py`): ensure a MySQL DB named `city_db` exists and credentials match settings, then run:
  - python manage.py migrate
  - python manage.py createsuperuser
  - python manage.py runserver
- Media uploads: ensure `media/` folder exists and is writable. In development the project serves media using the `static()` helper already present in `civicalert_project/urls.py`.
- Tests: run `python manage.py test` (note: `complaints/tests.py` is currently empty).

## Project-specific conventions & gotchas
- Auth and registration: registration uses `CitizenRegistrationForm` (email required + uniqueness enforced). When changing user fields, update `forms.py` and `register_view` accordingly.
- Templates rely on `request` context (configured in settings) and expect `messages` to exist (messages are added in `register_view`), but current templates do not render `messages`—be explicit when adding UI for success/error messages.
- Image uploads use `ImageField(upload_to='complaints/')`; prefer to reference `{{ MEDIA_URL }}` when generating image URLs in templates.
- `dashboard.html` marks but does not update `Notification.is_read`. If adding read notifications behavior, mirror the read/update logic in `dashboard` view or use an AJAX endpoint.
- Settings contain a plaintext SECRET_KEY and `DEBUG=True`—these are acceptable for dev but must be externalized for production (don't hardcode secrets in the repo).
- Views file contains a small duplicate import (two `from .forms import CitizenRegistrationForm` lines); small cleanups like this are safe to submit.

## Where to add changes & tests
- New business logic: add to `complaints/views.py` and cover with unit tests in `complaints/tests.py` (use Django TestCase and the test DB).
- Model changes: add migrations (use `python manage.py makemigrations` then `migrate`), and add tests that verify field choices and behavior.
- UI changes: templates are in `complaints/templates/complaints/`; prefer re-using Tailwind classes as in `dashboard.html`.

## Security & deployment notes
- For deployment, update `ALLOWED_HOSTS` and set `DEBUG=False` and move secrets to env vars or secret management.
- Add `STATIC_ROOT` if adding `collectstatic`/production static serving.

## Examples for quick reference
- Check unique email enforcement: `complaints/forms.py` -> `def clean_email(self): ... User.objects.filter(email=email).exists()`
- Query user complaints: `Complaint.objects.filter(citizen=request.user).order_by('-created_at')` (used in `dashboard` view)

---
If any of these details are unclear or you'd like me to expand a section (DB setup, test examples, or a sample PR checklist), tell me which part to improve and I'll iterate.  

/ End of Copilot instructions
