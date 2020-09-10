from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Covid19metadata, SampleMutlist, MutSamplelist

class IndexView(generic.ListView):
    template_name = 'mutapp/index.html'
    context_object_name = 'latest_sequence_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Covid19metadata.objects.order_by('sample_collection_date')[:50]

class DetailViewMeta(generic.DetailView):
    model = Covid19metadata
    #template_name = 'mutapp/covid19metadata_detail.html'

class DetailViewMut(generic.DetailView):
    model = MutSamplelist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta_name_str = self.object.sample
        meta_name_list = meta_name_str.split(';')
        meta_list = []
        for meta_name in meta_name_list:
            try:
                meta_id = Covid19metadata.objects.get(virus_strain_name=meta_name).id
            except (LookupError,Covid19metadata.DoesNotExist):
                meta_id = 1
            meta_list.append({'meta_name':meta_name, 'meta_id':meta_id})
        context['meta_list'] = meta_list
        return context
    #template_name = 'mutapp/mutsamplelist_detail.html'

def query_by_name(request):
    smaple = get_object_or_404(Covid19metadata, virus_strain_name=request.POST['queryname'])
    return HttpResponseRedirect(reverse('mutapp:metadata', args=(smaple.id,)))


def query_by_mutation(request):
    mutation_sample = get_object_or_404(MutSamplelist, start=request.POST['querypos'], ref_var=request.POST['querymut'])
    return HttpResponseRedirect(reverse('mutapp:mutation', args=(mutation_sample.id,)))