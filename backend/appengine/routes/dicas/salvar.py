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
from routes.dicas.modulo import Cidade, Estado


@login_not_required
@no_csrf
def index(estado_selecionado=None):
    ctx={'pesquisar_path': router.to_path(pesquisar),
         'salvar_path': router.to_path(salvar)}
    if estado_selecionado is None:
        ctx['estado']=Estado.query_ordenada_por_nome().fetch()
        ctx['estado_selecionado'] = None
    else:
        ctx['estado_selecionado'] = Estado.get_by_id(int(estado_selecionado))
        ctx['cidade']=Cidade.query_por_estado_cidade_por_nome(estado_selecionado).fetch()
    return TemplateResponse(ctx,'dicas/salvar.html')



    #ctx={'salvar_path': router.to_path(salvar)}
    #return TemplateResponse(ctx,'dicas/form.html')


@login_not_required
@no_csrf
def salvar(_resp, **propriedade):
    ctx = propriedade
    _resp.write(ctx)
    propriedade['cidade']=ndb.Key(Cidade,int(propriedade['cidade']))
    ctx = propriedade
    _resp.write(ctx)
    from routes.dicas.modulo import DicasForm
    dicas_form = DicasForm(**propriedade)
    erros = dicas_form.validate()
    if erros:
       contexto = {'salvar_path':router.to_path(salvar),
                   'erros':erros,
                   'dica':dicas_form}
       return TemplateResponse(contexto, 'dicas/salvar.html')
    else:
        dica = dicas_form.fill_model()
        dica.put()
        return RedirectResponse(dicas)



@login_not_required
@no_csrf
def pesquisar(estado_selecionado):
    ctx={'salvar_path': router.to_path(salvar)}
    if estado_selecionado is None:
        ctx['cidade']='Selecione um estado'
        ctx['estado_selecionado'] = None
    else:
        ctx['estado_selecionado'] = Estado.get_by_id(int(estado_selecionado))
        ctx['cidade']=Cidade.query_por_estado_cidade_por_nome(estado_selecionado).fetch()
    return TemplateResponse(ctx,template_path='dicas/salvar.html')
