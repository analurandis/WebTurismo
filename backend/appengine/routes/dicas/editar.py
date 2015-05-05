# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from routes import dicas
from tekton import router
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.redirect import RedirectResponse
from routes.dicas.modulo import Cidade, Estado


@login_not_required
@no_csrf
def index(_resp, dic_selecionada=None):
    ctx={'dic_selecionada': dic_selecionada}
    ctx={'editar': router.to_path(editar),
         'excluir':router.to_path(excluir)}
    if dic_selecionada is None:
        ctx['dic_selecionada']=None
    else:
        ctx['dic_selecionada'] = Dicas.get_by_id(int(dic_selecionada))
        ctx['dica']=Dicas.query_buscar_por_ID(dic_selecionada).fetch()
    return TemplateResponse(ctx,template_path='dicas/editar.html')


    #ctx={'salvar_path': router.to_path(salvar)}
    #return TemplateResponse(ctx,'dicas/form.html')

@login_not_required
@no_csrf
def excluir(_resp, dic_selecionada=None):
    return TemplateResponse(template_path='dicas/editar.html')

@login_not_required
@no_csrf
def editar(_resp, dic_selecionada=None):
    _resp.write('oiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    return TemplateResponse(template_path='dicas/editar.html')



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
       return TemplateResponse(contexto, 'dicas/form.html')
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


