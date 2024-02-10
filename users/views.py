from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


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
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
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
