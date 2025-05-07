from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from transformers import pipeline
from .models import ChatMessage
import json

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