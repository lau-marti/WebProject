from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import PlaylistForm, SongForm
from .models import Playlist, Song
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name ='form.html'
class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'form.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assignem l'usuari actual a la llista de reproducció
        return super(PlaylistCreate, self).form_valid(form)

class PlaylistDetail(DetailView):
    model = Playlist
    template_name='playlist_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PlaylistDetail, self).get_context_data(**kwargs)
        return context

class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    template_name = 'form.html'
    form_class = SongForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.playlist = Playlist.objects.get(id=self.kwargs['pk'])
        return super(SongCreate, self).form_valid(form)