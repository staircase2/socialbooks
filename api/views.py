from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

from socialbooks.library import models 
from socialbooks.library.views import download_epub, add_by_url_field, add_data_to_document, download_jsbook
from socialbooks.api import HttpResponseCreated, SocialbooksHttpResponseNotAcceptable 
from socialbooks.api.forms import APIUploadForm
from socialbooks.library import cyclops

import json

@never_cache
@login_required
def library(request, select=None):
	
	if request.method == 'GET':
		documents = models.EpubArchive.objects.only('id', 'title', 'orderable_author').filter(user_archive__user=request.user).order_by(settings.DEFAULT_ORDER_FIELD).distinct()

		out = []
		if select is None:
			out = [
				{
					'id': d.id,
					'title': d.title,
					'author': d.orderable_author
				}
				for d in documents
			]

		elif select == 'authors':
			out = {'authors':
				[ d.orderable_author for d in documents ]
			}

		elif select == 'titles':
			out = {'titles':
				[ d.title for d in documents ]
			}
		else:
			raise Http404()
		
		response = HttpResponse(json.dumps(out))
		response['Content-Type'] = 'application/json'
		return response
		
	else:
		return HttpResponseNotAllowed()

@never_cache
@login_required
def api_book(request, title, key, nonce=None):
	return download_jsbook(request, title, key, nonce)


@never_cache
@login_required
def main(request, SSL=True):
    '''Main entry point; dispatch by request type for upload vs. GET operations'''
    if request.method == 'GET':
        # No-arg GET request is a library listing; return all the user's documents
        documents = models.EpubArchive.objects.filter(user_archive__user=request.user).order_by(settings.DEFAULT_ORDER_FIELD).distinct()
        return direct_to_template(request, 'api/list.html', 
                                  {'documents': documents})

    # Accept an epub file either by URL or by direct POST file upload with epub bytes as `epub_data`
    elif request.method == 'POST':
        resp = None
        if 'epub_url' in request.POST:
            resp = add_by_url_field(request, request.POST['epub_url'], redirect_success_to_page=False)        

        elif request.FILES:
            form = APIUploadForm(request.POST, request.FILES)
            if form.is_valid():
                temp_file = request.FILES['epub_data'].temporary_file_path()
                document_name = form.cleaned_data['epub_data'].name
                document = models.EpubArchive.objects.create(name=document_name)
                document.save()
                resp = add_data_to_document(request, document, open(temp_file), form, redirect_success_to_page=False)
                
            else:
                return SocialbooksHttpResponseNotAcceptable('You did not provide a correctly-formatted epub_data parameter: %s' % form.errors) 
        else:
            return SocialbooksHttpResponseNotAcceptable("You must either include epub_url or epub_data in your request")

        if isinstance(resp, models.EpubArchive):
            # This was a successful add and we got back a document
            return HttpResponseCreated("%s%s" % (settings.SECURE_HOSTNAME, reverse('api_download', args=[resp.id])))

        # Otherwise this was an error condition
        return SocialbooksHttpResponseNotAcceptable(resp) # Include the complete Socialbooks response

    else:
        return HttpResponseNotAllowed('GET, POST')


@never_cache
@login_required
def api_download(request, epub_id, SSL=True):
    '''Download an epub file by its ID'''
    if request.method != 'GET':
        return HttpResponseNotAllowed('GET')

    return download_epub(request, '', epub_id)


