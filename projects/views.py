from django.shortcuts import render 


projectsList = [
    {
        'id': '1',
        'title': "Ecommerce Website",
        'description': 'Fully functional ecommerce website'
    },
    {
        'id': '2',
        'title': "Portfolio Website",
        'description': 'This was a project where I built out my portfolio'
    },
    {
        'id': '3',
        'title': "Social Network",
        'description': 'Awesome open source project I am still working on'
    }
]




def projects(request):
    page = 'projects'
    number = 10
    context = {'page':page,'number':number, 'projects': projectsList}
    return render(request,'projects/projects.html',context)


def project(request,pk):
    projectobj = None
    for i in projectsList:
        if i ['id'] == pk:
            projectobj = i
    return render(request,'projects/single-project.html',{'project':projectobj})