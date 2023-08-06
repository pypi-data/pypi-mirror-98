from django.shortcuts import get_object_or_404
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Case, When
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect

from souschef.note.models import Note, NoteFilter
from souschef.note.forms import NoteForm
from souschef.member.models import Client


# Create your views here.

class NoteList(
        LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    # Display the list of notes
    context_object_name = 'notes'
    model = Note
    paginate_by = 20
    permission_required = 'sous_chef.read'
    template_name = 'notes_list.html'

    def get_queryset(self):
        uf = NoteFilter(self.request.GET)
        return uf.qs.select_related(
            'client__member'
        )

        # The queryset must be client

    def get_context_data(self, **kwargs):
        uf = NoteFilter(self.request.GET, queryset=self.get_queryset())

        context = super(NoteList, self).get_context_data(**kwargs)

        # Here you add some variable of context to display on template
        context['filter'] = uf
        text = ''
        count = 0
        for getVariable in self.request.GET:
            if getVariable == "page":
                continue
            for getValue in self.request.GET.getlist(getVariable):
                if count == 0:
                    text += "?" + getVariable + "=" + getValue
                else:
                    text += "&" + getVariable + "=" + getValue
                count += 1

        text = text + "?" if count == 0 else text + "&"
        context['get'] = text

        return context


class ClientNoteList(
        LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    # Display detail of one client
    context_object_name = 'notes'
    model = Note
    permission_required = 'sous_chef.read'
    template_name = 'notes_client_list.html'

    def get_queryset(self):
        queryset = NoteFilter(
            self.request.GET,
            queryset=Note.objects.filter(
                client__id=self.kwargs['pk'])).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientNoteList, self).get_context_data(**kwargs)
        context['active_tab'] = 'notes'
        context['client_status'] = Client.CLIENT_STATUS
        context['client'] = get_object_or_404(Client, id=self.kwargs['pk'])
        context['filter'] = NoteFilter(
            self.request.GET, queryset=Note.objects.filter(
                client__id=self.kwargs['pk']))

        return context


class NoteAdd(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    form_class = NoteForm
    model = Note
    permission_required = 'sous_chef.edit'
    template_name = 'notes_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(NoteAdd, self).form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            _("The note has been created.")
        )
        return response

    def get_success_url(self):
        return reverse('note:note_list')


class ClientNoteListAdd(NoteAdd):
    """
    Reuses things from note.
    """
    def get_context_data(self, **kwargs):
        context = super(ClientNoteListAdd, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('member:client_notes', kwargs={'pk': self.kwargs['pk']})


@login_required
def mark_as_read(request, id):
    note = get_object_or_404(Note, pk=id)
    note.mark_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def mark_as_unread(request, id):
    note = get_object_or_404(Note, pk=id)
    note.mark_as_unread()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NoteBatchToggle(
        LoginRequiredMixin, PermissionRequiredMixin, View
):
    permission_required = 'sous_chef.read'

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('note')
        count = Note.objects.filter(id__in=ids).update(is_read=Case(
            When(is_read=True, then=False),
            When(is_read=False, then=True)
        ))
        messages.add_message(
            self.request, messages.SUCCESS,
            _("%(count)s note(s) have been updated.") % {'count': count}
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
