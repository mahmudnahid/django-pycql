import uuid
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import time


from node.forms import NodeForm
from models import Node


def node_add(request):
    form = NodeForm(request.POST or None)
    if form.is_valid():
        data = {'nid' : uuid.uuid4().hex,
                'title' : str(form.cleaned_data['title']),
                'body' : str(form.cleaned_data['body']),
                'author' : str(form.cleaned_data['author']),
                'node_timestamp' : int(time.time()),
                'revision_log' : str(form.cleaned_data['revision_log']),
                'is_front_page' : form.cleaned_data['is_front_page'],
                'is_sticky' : form.cleaned_data['is_sticky'],
                'is_published' : form.cleaned_data['is_published'],
                'can_comment' : form.cleaned_data['can_comment'],
                # 'tags': str(form.cleaned_data['tags']),
                'node_type' : str(form.cleaned_data['node_type'])
        }
        query = Node().insert(data)
        node = query.execute()

        #Increase the views count
        # count = {'views' : 'views+1'
        # }
        # count_query = NodeCount().update().where('nid', data['nid'], '=', True)
        # nodecount = count_query.execute()

        return HttpResponseRedirect(reverse('node_index'))
    context = {
        'form': form,
        }
    return render_to_response('addNode.html', context,
                              context_instance=RequestContext(request))



def node_edit(request, pk):
    query = Node().select().compare('nid', pk)
    node_list = query.execute()
    node_dict = {}
    for node in node_list:
        for key, value in node.items():
            node_dict[key] = value

    form = NodeForm(request.POST or None, initial=node_dict)
    if request.method == 'POST':
        if form.is_valid():
            data = {'title' : '"' + str(form.cleaned_data['title'])+'"',
                    'body' : '"' + str(form.cleaned_data['body'])+'"',
                    'author' : '"' + str(form.cleaned_data['author']) +'"',
                    'node_timestamp' : int(time.time()),
                    'revision_log' : '"' + str(form.cleaned_data['revision_log'])+'"',
                    'is_front_page' : form.cleaned_data['is_front_page'],
                    'is_sticky' : form.cleaned_data['is_sticky'],
                    'is_published' : form.cleaned_data['is_published'],
                    'can_comment' : form.cleaned_data['can_comment'],
                    # 'tags': '"' + str(form.cleaned_data['tags'])+'"',
                    'node_type' : '"' + str(form.cleaned_data['node_type'])+'"'
            }

            query = Node().update(data).where('nid', pk , '=', True)
            node_update = query.execute()

        return HttpResponseRedirect(reverse('node_index'))
    context = {
        'form': form,
        }
    return render_to_response('editNode.html', context,
                              context_instance=RequestContext(request))


def node_delete(request, pk):
    query = Node().delete().where('nid', pk)
    node_del = query.execute()
    return HttpResponseRedirect(reverse('node_index'))


def node_detail(request, pk):
    query = Node().select().compare('nid', pk)
    node_list = query.execute()
    #Increase the views count
    # count = {'views': 'views+1'
    # }
    # count_query = NodeCount().update(count).where('nid', pk, '=', True)
    # nodecount = count_query.execute()

    context = {
        'node_list': node_list
    }
    return render_to_response('nodeDetail.html', context)




def node_index(request):
    query = Node().select('nid', 'title')
    query.compare('is_published', True, '=', True).compare('node_timestamp', int(time.time()), '<=', True).allowFiltering()
    node_list = query.execute()
    context = {
        'node_list': node_list,
        }
    return render_to_response('nodes.html', context)

