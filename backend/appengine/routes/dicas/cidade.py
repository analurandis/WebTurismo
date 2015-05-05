# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from routes import dicas
from tekton import router
from gaecookie.decorator import no_csrf
from routes.dicas.modulo import CidadeForm, EstadoForm, Estado
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    contexto={'salvarCidade_path': router.to_path(salvarCidade),
              'estado' : Estado.query_ordenada_por_nome().fetch()}
    return TemplateResponse(contexto)




@login_not_required
@no_csrf
def salvarCidade(_resp, **propriedade):
    propriedade['estado']=ndb.Key(Estado,int(propriedade['estado']))
    cidade_form = CidadeForm(**propriedade)
    erros = cidade_form.validate()
    if erros:
       contexto = {'salvar_path':router.to_path(salvarCidade),
                   'erros':erros,
                   'cidade':cidade_form}
       return TemplateResponse(contexto, 'dicas/cidade.html')
    else:
        cidade = cidade_form.fill_model()
        cidade.put()
        return RedirectResponse(dicas)
