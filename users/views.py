from django.shortcuts import render
from .models import Profile

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # Corrected line: Exclude skills where description is empty
    topSkills = profile.skill_set.exclude(description="")
    # Include only skills where description is empty
    otherSkills = profile.skill_set.filter(description="")

    # Note: Changed 'topSkill' to 'topSkills' in the context for consistency
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)
