import openai
import os
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from transformers import pipeline

# Load your model
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')
qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad', max_answer_len=100)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
translator_fr_en = pipeline('translation', model='Helsinki-NLP/opus-mt-fr-en')
translator_en_fr = pipeline('translation_en_to_fr', model='Helsinki-NLP/opus-mt-en-fr')


def question_answering(request):
    context = {}
    if request.method == 'POST':
        context['question'] = request.POST.get('question')
        context['paragraph'] = request.POST.get('paragraph')
        
        answer = qa_pipeline({
            'question': context['question'],
            'context': context['paragraph']})
        context['answer'] = answer['answer']
    return render(request, 'chatbot/question_answering.html', context)

@require_http_methods(["GET", "POST"])
def sentiment_analysis(request):
    context = {'result': None}
    if request.method == 'POST':
        text_to_analyze = request.POST.get('text', '')
        if text_to_analyze:
            # Use model to predict
            result = classifier(text_to_analyze)
            context['result'] = result
            print(context)
    return render(request, 'chatbot/sentiment_analysis.html', context)

def summarize_text(request):
    context = {}
    if request.method == 'POST':
        text_to_summarize = request.POST.get('text', '')
        # Generate summary
        summary = summarizer(text_to_summarize, max_length=150, min_length=40, do_sample=False)
        context['summary'] = summary[0]['summary_text']
    return render(request, 'chatbot/summarize.html', context)


def translate_text_fr_en(request):
    context = {}
    if request.method == 'POST':
        text_to_translate = request.POST.get('text', '')
        translation = translator_fr_en(text_to_translate, max_length=512)
        context['translation'] = translation[0]['translation_text']
    return render(request, 'chatbot/translate_fr_en.html', context)


def translate_to_french(request):
    context = {}
    if request.method == 'POST':
        english_text = request.POST.get('text', '')
        # Perform translation
        result = translator_en_fr(english_text, max_length=512)
        context['translation'] = result[0]['translation_text']
    return render(request, 'chatbot/translate_en_fr.html', context)