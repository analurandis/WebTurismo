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
def index(estado_selecionado=None):
    ctx={'pesquisar_path': router.to_path(pesquisar),
         'salvar_path': router.to_path(salvar)}
    if estado_selecionado is None:
        ctx['estado']=Estado.query_ordenada_por_nome().fetch()
        ctx['estado_selecionado'] = None
    else:
        ctx['estado_selecionado'] = Estado.get_by_id(int(estado_selecionado))
        ctx['cidade']=Cidade.query_por_estado_cidade_por_nome(estado_selecionado).fetch()
    return TemplateResponse(ctx,'dicas/form.html')



    #ctx={'salvar_path': router.to_path(salvar)}
    #return TemplateResponse(ctx,'dicas/form.html')


@login_not_required
@no_csrf
def salvar(_resp, **propriedade):
    ctx = propriedade
    cidade_id=(propriedade['cidade'])
    city=Cidade.query_buscar_cid_por_ID(cidade_id).fetch()
    propriedade['city']=city[0].cidade
    propriedade['cidade']=ndb.Key(Cidade,int(propriedade['cidade']))
    ctx = propriedade
    dicas_form = DicasForm(**propriedade)
    erros = dicas_form.validate()

    if erros:
       estado = Estado.get_by_id(int(propriedade['estado_selecionado']))
       ctx = {'salvar_path':router.to_path(salvar),
              'estado_selecionado':  estado,
              'cidade':Cidade.query_por_estado_cidade_por_nome(propriedade['estado_selecionado']).fetch(),
              'erros':erros,
              'dica':dicas_form}
       return TemplateResponse(ctx, 'dicas/form.html')
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
    return TemplateResponse(ctx,template_path='dicas/form.html')
