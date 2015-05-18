# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from gaepermission.decorator import login_not_required
from routes import dicas
from tekton import router
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path
from routes.dicas.modulo import Cidade, Estado, DicasForm


@login_not_required
@no_csrf
def index(cidade=None):
    ctx={'cidade': Cidade.query_ordenada_por_nome().fetch()}
    if cidade is None:
        ctx['cidade'] = Cidade.query_ordenada_por_nome().fetch()
    else:
        ctx['cidade'] = Cidade.get_by_id(int(cidade))
    return TemplateResponse(ctx,'/dicas/form.html')

