from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):  # Corrected 'ProjectFrom' to 'ProjectForm'
    class Meta:
        model = Project 
        fields =  ['title','featured_image', 'description', 'demo_link', 'source_link', 'tags']
       
