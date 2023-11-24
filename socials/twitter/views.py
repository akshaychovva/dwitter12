from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Dweet
from .forms import DweetForm

def home(request):
    form = DweetForm(request.POST or None)
    if request.method == 'POST':
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect('/') # return to '' in url
         
    dweet_list = []
    user_follows = request.user.profile.follows.all()
    for user_profile in user_follows:
        dweet_list += user_profile.user.dweets.all()

    dweet_list.sort(key=lambda x: x.edited_at, reverse=True)
    context = {'dweet_list': dweet_list, 'form': form}
    return render(request, 'base.html', context)

def profile_list(request):
    profile_list = Profile.objects.exclude(user=request.user)
    context = {'profile_list': profile_list}
    return render(request, 'profiles.html', context)

def profile(request, pk):
    '''if there is no profile for existing user'''
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    try:
        user_profile = Profile.objects.get(pk=pk)
        current_user = request.user
    except Exception:
        return redirect('profile_list')
    if request.method == 'POST':
        value = request.POST['follow']
        if value == 'follow':
            current_user.profile.follows.add(user_profile)
        elif value == 'unfollow':
            current_user.profile.follows.remove(user_profile)
        else:
            return HttpResponse('Page not found')
        current_user.profile.save()
    user_id = user_profile.id
    following = user_profile.follows.exclude(pk=user_id)
    followed_by = user_profile.folowed_by.exclude(pk=user_id)
    context = {'profile': user_profile, 'following': following, 'followed_by': followed_by}
    return render(request, 'profile.html', context)


def Update_dweet(request, pk):
    dweet = Dweet.objects.get(id=pk)
    form = DweetForm(instance=dweet)
    if request.method == 'POST':
        form = DweetForm(request.POST, instance=dweet)
        if form.is_valid():
            form.save(commit=False)
            dweet.num_of_edit = 1
            dweet.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'base.html', context)
    
def delete_dweet(request, pk):
    dweet = Dweet.objects.get(id=pk)
    dweet.delete()
    return  redirect('/')
    