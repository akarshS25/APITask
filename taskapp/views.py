from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
import json

# Signup view
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)

# Login view
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# Assign Task view (only admin can assign tasks)
@login_required
def assign_task(request):
    if request.method == "POST" and request.user.is_staff:
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description")
        assigned_to_id = data.get("assigned_to_id")

        if not title or not description:
            return JsonResponse({"error": "Title and description required"}, status=400)

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        task = Task.objects.create(title=title, description=description, assigned_to=assigned_to)
        return JsonResponse({"message": "Task assigned", "task_id": task.id})

    return JsonResponse({"error": "Forbidden or invalid request"}, status=403)
