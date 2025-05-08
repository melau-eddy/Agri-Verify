from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from transformers import pipeline
from .models import ChatMessage
import json
from django.db.models import Q
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
    return render(request, 'home.html', {
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

def details(request):
    return render(request, 'details.html')


from django.http import JsonResponse
from .models import EducationalVideo, VerifiedProduct, GovernmentApproval


def home_page(request):
    # Get approved videos (prefetch related approval to reduce queries)
    approved_videos = EducationalVideo.objects.select_related('related_approval').filter(
        Q(related_approval__status='approved') | Q(related_approval__isnull=True),
        video_file__isnull=False
    ).order_by('-created_at')
    
    # Get featured video (first approved video or most recent if none specified)
    featured_video = approved_videos.first()
    
    # Get related videos (excluding featured, limited to 3)
    related_videos = approved_videos.exclude(
        id=featured_video.id if featured_video else None
    )[:3]
    
    # Get verified products with their approval (prefetch to reduce queries)
    verified_products = VerifiedProduct.objects.select_related('approval').filter(
        approval__status='approved',
        image__isnull=False
    ).order_by('-date_added')[:3]
    
    context = {
        'featured_video': featured_video,
        'related_videos': related_videos,
        'verified_products': verified_products,
    }
    return render(request, 'home.html', context)



@csrf_exempt
def verify_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '').strip()
            
            product = VerifiedProduct.objects.get(
                approval__approval_id=code
            )
            
            approval = product.approval
            
            return JsonResponse({
                'status': 'success',
                'product': {
                    'name': product.name,
                    'type': product.get_product_type_display(),
                    'manufacturer': product.manufacturer,
                    'image_url': product.image.url if product.image else None,
                    'description': product.description,
                    'traits': product.gmo_traits,
                },
                'approval': {
                    'id': approval.approval_id,
                    'status': approval.get_status_display(),
                    'body': approval.approving_body,
                    'date': approval.approval_date.strftime('%Y-%m-%d') if approval.approval_date else None,
                    'expiry': approval.expiry_date.strftime('%Y-%m-%d') if approval.expiry_date else None,
                    'risk': approval.risk_level,
                    'conditions': approval.conditions
                },
                'is_approved': approval.status == 'approved',
            })
            
        except VerifiedProduct.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'No product found with this approval ID'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)