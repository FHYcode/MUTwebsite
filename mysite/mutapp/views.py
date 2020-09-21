from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Covid19metadata, SampleMutlist, MutSamplelist

class IndexView(generic.ListView):
    template_name = 'mutapp/index.html'
    context_object_name = 'latest_sequence_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Covid19metadata.objects.order_by('-sample_collection_date')[:30]

class DetailViewMeta(generic.DetailView):
    model = Covid19metadata
    #template_name = 'mutapp/covid19metadata_detail.html'


# query single mutation, version 1.0
# class DetailViewMut(generic.DetailView):
#     model = MutSamplelist
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         meta_name_str = self.object.sample
#         meta_name_list = meta_name_str.split(';')
#         meta_list = []
#
#         for meta_name in meta_name_list:
#             try:
#                 meta_id = Covid19metadata.objects.get(virus_strain_name=meta_name).id
#             except (LookupError,Covid19metadata.DoesNotExist):
#                 meta_id = 1
#             meta_list.append({'meta_name':meta_name, 'meta_id':meta_id})
#
#         context['meta_list'] = meta_list
#         return context
#     #template_name = 'mutapp/mutsamplelist_detail.html'

# query single mutation, version 2.0
class DetailViewMut(generic.DetailView):
    model = MutSamplelist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta_name_str = self.object.sample
        meta_name_list = meta_name_str.split(';')
        meta_list = []

        meta_id_srt = self.object.meta_id
        meta_id_list = meta_id_srt.split(';')
        meta_name_id_tlist = zip(meta_name_list,meta_id_list)

        for i in meta_name_id_tlist:
            meta_list.append({'meta_name':i[0], 'meta_id':i[1]})

        context['meta_list'] = meta_list
        return context
    #template_name = 'mutapp/mutsamplelist_detail.html'

def query_by_name(request):
    smaple = get_object_or_404(Covid19metadata, virus_strain_name=request.POST['queryname'])
    return HttpResponseRedirect(reverse('mutapp:metadata', args=(smaple.id,)))

def query_by_mutation(request):
    mutation_sample = get_object_or_404(MutSamplelist,
                                        start=request.POST['querypos'], ref_var=request.POST['querymut'])
    return HttpResponseRedirect(reverse('mutapp:mutation', args=(mutation_sample.id,)))


# query multiple mutations, version 1.0
# def query_by_multi_mutation(request):
#     #- get query_set
#     textarea = request.POST['multimut']
#     start_mut = []
#     list_temp = textarea.split()
#     for i in list_temp:
#         start_mut.append(tuple(i.split(';')))
#     my_queryset = []
#     for i in start_mut:
#         try:
#             mut_sample = MutSamplelist.objects.get(start=i[0], ref_var=i[1])
#         except (LookupError, MutSamplelist.DoesNotExist):
#             print('LookupError: '+i[0]+';'+i[1])
#         else:
#             my_queryset.append(mut_sample)
#     vname_list = []
#     for i in my_queryset:
#         vname_set = set(i.sample.upper().split(';'))#-----------------------------------
#         vname_list.append(tuple(vname_set))
#
#     #- build new table
#     smut_qset_vname = [start_mut, my_queryset, vname_list]
#     smut_qset_vname_transpose = list(map(list, zip(*smut_qset_vname)))
#
#     #- count the number of hits
#     vname_all_tuple = ()
#     for i in vname_list:
#         vname_all_tuple = vname_all_tuple + i
#     vname_count_dic = {}
#     for k in vname_all_tuple:
#         vname_count_dic[k] = vname_count_dic.get(k, 0) + 1
#     vname_count_mut_list = []
#     for k,v in vname_count_dic.items():
#         mut_tep = ()
#         for i in smut_qset_vname_transpose:
#             if k in i[2]:
#                 mut_tep = mut_tep + i[0]
#         vname_count_mut_list.append([k,v,mut_tep])
#     vname_count_mut_list.sort(key=lambda x:x[1], reverse=True)
#
#     #- truncated
#     truncated = 30
#     if len(vname_count_mut_list)>truncated:
#         vname_count_mut_list_trunc = vname_count_mut_list[0:truncated]
#     else:
#         vname_count_mut_list_trunc = vname_count_mut_list
#
#     #- get object
#     vname_count_mut_list_trunc_obj = vname_count_mut_list_trunc
#     i = 0
#     while i<len(vname_count_mut_list_trunc_obj):
#         try:
#             metaobj = Covid19metadata.objects.get(virus_strain_name=vname_count_mut_list_trunc[i][0])
#         except (LookupError, Covid19metadata.DoesNotExist):
#             print('LookupError:',vname_count_mut_list_trunc[i])
#             vname_count_mut_list_trunc_obj[i].append(Covid19metadata.objects.get(pk=1))
#         else:
#             vname_count_mut_list_trunc_obj[i].append(metaobj)
#         i = i + 1
#
#     #return HttpResponse(vname_count_mut_list_trunc_obj)
#     context = {'hits_list': vname_count_mut_list_trunc_obj}
#     return render(request, 'mutapp/multimut_hits.html', context)

# query multiple mutations, version 2.0
def query_by_multi_mutation(request):
    #- get query_set
    textarea = request.POST['multimut']
    start_mut = []
    list_temp = textarea.split()
    for i in list_temp:
        start_mut.append(tuple(i.split(';')))
    my_queryset = []
    for i in start_mut:
        try:
            mut_sample = MutSamplelist.objects.get(start=i[0], ref_var=i[1])
        except (LookupError, MutSamplelist.DoesNotExist):
            print('LookupError: '+i[0]+';'+i[1])
        else:
            my_queryset.append(mut_sample)

    vname_tlist =[]
    metaid_tlist = []
    for i in my_queryset:
        vname_tuple = tuple(i.sample.split(';'))
        metaid_tuple = tuple(i.meta_id.split(';'))
        vname_tlist.append(vname_tuple)
        metaid_tlist.append(metaid_tuple)

    #- build new table
    smut_qset_metaid = [start_mut, my_queryset, metaid_tlist]
    smut_qset_metaid_transpose = list(map(list, zip(*smut_qset_metaid)))

    #- count the number of hits
    metaid_all_tuple = ()
    for i in metaid_tlist:
        metaid_all_tuple = metaid_all_tuple + i
    metaid_count_dic = {}
    for k in metaid_all_tuple:
        metaid_count_dic[k] = metaid_count_dic.get(k, 0) + 1
    metaid_count_mut_list = []
    for k,v in metaid_count_dic.items():
        mut_tep = ()
        for i in smut_qset_metaid_transpose:
            if k in i[2]:
                mut_tep = mut_tep + i[0]
        metaid_count_mut_list.append([k,v,mut_tep])
    metaid_count_mut_list.sort(key=lambda x:x[1], reverse=True)

    # #- truncated
    # truncated = 5000
    # if len(metaid_count_mut_list)>truncated:
    #     metaid_count_mut_list_trunc = metaid_count_mut_list[0:truncated]
    # else:
    #     metaid_count_mut_list_trunc = metaid_count_mut_list

    #- truncated v2
    if metaid_count_mut_list[0][0] == '1':
        del metaid_count_mut_list[0]
    metaid_count_mut_list_trunc = []
    for i in metaid_count_mut_list:
        if i[1] == metaid_count_mut_list[0][1]:
            metaid_count_mut_list_trunc.append(i)
        else:
            break

    #- get object
    metaid_count_mut_list_trunc_obj = metaid_count_mut_list_trunc
    i = 0
    location_list = []
    while i<len(metaid_count_mut_list_trunc_obj):
        try:
            metaobj = Covid19metadata.objects.get(pk=metaid_count_mut_list_trunc[i][0])
            location_list.append(metaobj.location)
        except (LookupError, Covid19metadata.DoesNotExist):
            print('LookupError:',metaid_count_mut_list_trunc[i])
            metaid_count_mut_list_trunc_obj[i].append(Covid19metadata.objects.get(pk=1))
        else:
            metaid_count_mut_list_trunc_obj[i].append(metaobj)
        i = i + 1

    # - sort by date
    metaid_count_mut_list_trunc_obj.sort(key=lambda x:x[3].sample_collection_date,reverse=True)

    #- geographic distibution
    country_list = [i.split('/')[0].strip() for i in location_list]
    country_count_dic = {}
    for k in country_list:
        country_count_dic[k] = country_count_dic.get(k, 0) + 1
    country_count_tlist = []
    for k, v in country_count_dic.items():
        country_count_tlist.append((k,v))
    country_count_tlist.sort(key=lambda x: x[1], reverse=True)

    #return HttpResponse(country_count_tlist)
    context = {'hits_list': metaid_count_mut_list_trunc_obj, 'country_count':country_count_tlist}
    return render(request, 'mutapp/multimut_hits.html', context)