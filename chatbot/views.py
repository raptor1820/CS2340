from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def askAI(message):
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=message
    )
    return response.text

def chatbot(request):
    
    if request.method == 'POST':
        message = request.POST.get("message")
        response = askAI(message)
        return JsonResponse({"message": message, "response": response})
    
    return render(request, "chatbot/chatbot.html")

