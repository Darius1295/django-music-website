from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Album, Song
from .forms import UserForm
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        users_songs = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_name__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            users_songs = users_songs.filter(
                Q(song_title__icontains=query) |
                Q(album__artist__icontains=query)
            ).distinct()
            return render(request, 'music/results.html', {
                'albums': albums,
                'song_list': users_songs,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def songs(request, filter_by='track_number'):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def detail(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=pk)
    return render(request, 'music/detail.html', {'album': album, 'user': user})


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_name', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_name', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'song_title', 'track_number']
    success_url = reverse_lazy('music:add-song')


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('music:songs')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/registration_form.html', context)




