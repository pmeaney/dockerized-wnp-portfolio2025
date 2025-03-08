from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django import forms
from .models import Tag
from django.urls import reverse

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['value', 'category']

class TagModalView(View):
    """View for handling tag creation in a modal"""
    
    def get(self, request):
        """Return the form HTML for the modal"""
        form = TagForm()
        
        return JsonResponse({
            'html': render(request, 'portfolio/tag_modal.html', {
                'form': form,
            }).content.decode('utf-8'),
            'step': 'open',
        })
    
    def post(self, request):
        """Handle the form submission and return JSON"""
        form = TagForm(request.POST)
        
        if form.is_valid():
            tag = form.save()
            
            return JsonResponse({
                'step': 'success',
                'tag_id': tag.id,
                'tag_name': str(tag),
            })
        else:
            return JsonResponse({
                'html': render(request, 'portfolio/tag_modal.html', {
                    'form': form,
                }).content.decode('utf-8'),
                'step': 'error',
            })