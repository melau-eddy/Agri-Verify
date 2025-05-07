from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from transformers import pipeline
from .models import ChatMessage
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Initialize the AI model (agriculture-focused)
agriculture_qa = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2"
)

AGRICULTURE_KNOWLEDGE = """
Genetically Modified Organisms (GMOs) are organisms whose genetic material has been altered using genetic engineering techniques. 
In agriculture, GMO crops are designed to improve yield, enhance nutritional content, drought tolerance, and resistance to pests and diseases. 
Common GMO crops include corn, soybeans, cotton, and canola. Regulatory agencies like the FDA, EPA, and USDA evaluate GMO safety before approval.
Organic farming prohibits GMO use, while conventional farming may use them. Farmers should check seed certification and local regulations.
"""

@login_required
def chat_view(request):
    """Render the agriculture chat template"""
    # Get last 5 messages for the current user
    recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'agriculture_chat.html', {
        'recent_messages': recent_messages
    })

@csrf_exempt
@login_required
def chat_api(request):
    """Handle AJAX chat requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get AI response
            result = agriculture_qa(
                question=user_message,
                context=AGRICULTURE_KNOWLEDGE,
                max_answer_len=200
            )
            
            # Save to database
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=result['answer']
            )
            
            return JsonResponse({
                'response': result['answer'],
                'suggestions': [
                    "GMO regulations in my area",
                    "How to verify seed authenticity",
                    "Benefits of GMO corn",
                    "Non-GMO alternatives"
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "register.html")

