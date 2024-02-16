from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile 
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles
def loginUser(request):
    page ='login'

    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
             user = User.objects.get(username=username)
        except User.DoesNotExist:
             messages.error(request, 'Username does not exist')
       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')


    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST' :
        form = CustomUserCreationForm (request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.success(request, 'error during registration')
    
    context = {'page': page, 'form': form}
    return render (request, 'users/login_register.html', context)

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles': profiles, 'search_query': search_query}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # Corrected line: Exclude skills where description is empty
    topSkills = profile.skill_set.exclude(description_exact="")
    # Include only skills where description is empty
    otherSkills = profile.skill_set.filter(description="")

    # Note: Changed 'topSkill' to 'topSkills' in the context for consistency
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    # Corrected line: Exclude skills where description is empty
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    

    context = {'profile':profile, 'skills':skills}
    return render(request, 'users/account.html', context)



@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile  # Corrected from user-profile to user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Corrected request. FILES to request.FILES
        if form.is_valid():
            form.save()  # Corrected form. save to form.save()
            
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile  # Fixed the '-' to '.'
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)  # Corrected 'request. POST' to 'request.POST'
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('account')
    context = {'form': form}  # Corrected the syntax for dictionary creation
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile  # Fixed the '-' to '.'
    skill = profile.skill_set.get(id=pk)  # Corrected '-getid=pk)' to '.get(id=pk)'
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)  # Corrected spacing
        if form.is_valid():
            form.save()  # Corrected 'form. save)' to 'form.save()'
            messages.success(request,'Skill was updated successfully!')
            return redirect('account')
    context = {'form': form}  # Adjusted spacing for readability
    return render(request, 'users/skill_form.html', context)



def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)  # Corrected '-get' to '.get'
    if request.method == 'POST':
        skill.delete()  # Added '()' to execute the delete method
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)
