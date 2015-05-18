$(document).ready(function () {
  var $txtInput = $('#txt-input');
  var $listaDiv = $('#lista-div');
  var $ajaxImg = $('#ajax-img');
  var $dicasLista = $('#dicas-lista');
  $ajaxImg.hide();

  function adicionarDica(dica) {
    var li = '<li id="li-' + dica.id + '" ><button id="btn-apagar-' + dica.id;
    li += '" class="btn btn-danger"><i class="glyphicon glyphicon-trash"></i></button>';
    li += ' - ';
    li += dica.titulo + ' - ' + dica.datas + '</li>';
    $dicasLista.append(li);
    $('#btn-apagar-' + dica.id).click(function () {
      $.post('/dicas/rest/apagar', {'dica_id': dica.id}, function () {
        $('#li-' + dica.id).remove();
      });
    });
  }

  $.get('/dicas/rest/listar', function (dicas) {
    $.each(dicas, function (i, dica) {
      adicionarDica(dica);
    });
  });

  var $msgUl = $('#msg-ul');

  var $selectCidade = $("select[name='cidade']");
  var $inputTitulo = $("input[name='titulo']");
    var $inputDatas = $("input[name='datas']");
    var $inputDescDica = $("input[name='descDica']");

  function obterInputs() {
    return {
      'cidade': $selectCidade.val(),
      'titulo': $inputTitulo.val(),
      'datas': $inputDatas.val(),
        'descDica': $inputDescDica.val()
    };
  }

  var $salvarBotao = $('#salvar-btn');
  $salvarBotao.click(function () {
    $('div.has-error').removeClass('has-error');
    $('span.help-block').text('');
    $ajaxImg.fadeIn();
    $salvarBotao.attr('disabled', 'disabled');
    $.post('/dicas/rest/salvar', obterInputs(), function (dica) {
      adicionarDica(dica);
      $('input.form-control').val('');
    }).error(function (erro) {
      var errosJson = erro.responseJSON;
      for (propriedade in  errosJson) {
        $('#' + propriedade + '-div').addClass('has-error');
        $('#' + propriedade + '-span').text(errosJson[propriedade]);
      }
    }).always(function () {
      $ajaxImg.fadeOut();
      $salvarBotao.removeAttr('disabled');
    });

  });

  $('#jq').click(function fcn(evento) {
    $listaDiv.slideToggle();
  });

  $('#jq2').click(function fcn(evento) {
    $listaDiv.empty();
  });

  $('#enviar-btn').click(function () {
    var msg = $txtInput.val();
    $txtInput.val('');
    var item = '<li>' + msg + '</li>';
    $msgUl.prepend(item);
    $msgUl.fadeOut(400, function () {
      $msgUl.fadeIn(2000);
    });
  });


});