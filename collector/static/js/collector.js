function prepare_ajax(){
  //console.log("Preparing Ajax Setup");
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();        
        xhr.setRequestHeader("X-CSRFToken",csrf_middlewaretoken);
        //console.log("Cookie csrf:      "+csrftoken);
        //console.log("Middleware csrf:  "+csrf_middlewaretoken);
      }
    }
  });
  }


function register_story(x){
  $('.view_'+x).off();
  $('.view_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $.ajax({
      url: x+'s/'+t_id+'/view',
      success: function(answer) {
        $('#'+x+'_'+t_id).html(answer);        
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer){
        console.log('ooops... on view '+x+' :(');
      }
    });
  });

  $('.hide_'+x).off();
  $('.hide_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $('#'+x+'_'+t_id).html('');
    prepare_ajax();
    rebootlinks();
  });

  $('.edit_'+x).off();
  $('.edit_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $.ajax({
      url: x+'s/'+t_id+'/edit',
      success: function(answer) {
        $('#'+x+'_'+t_id).html(answer);        
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer){
        console.log('ooops... on edit '+x+':(');
      }
    });
  });

  $('.'+x+'_update').off();
  $('.'+x+'_update').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var owner = $(this).closest('div.storyarticle').attr('id');
    var id = $(this).closest('div.storyarticle').attr('id').split('_')[1];
    var form = $(this).closest('form');
    formdata = form.serialize();
    var urlupdate = x+'s/'+id+'/edit';    
    $.ajax({    
      url: urlupdate,
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: formdata,
      dataType: 'json',
      success: function(answer) {
        console.log('Success... ');
        $('#'+owner).html(answer);
        rebootlinks();
        $('button#'+id+'.view_'+x).click();
      },
      error: function(answer) {
        console.log('Error... ');
        console.log(answer);
      },
    });  
  });

  $('.add_'+x).off();
  $('.add_'+x).on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var id = $(this).parent('p').prop('className');
    console.log(id);    
    //var form = $(this).closest('form');
    var urlupdate = x+'s/add';    
    $.ajax({    
      url: urlupdate,
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {'id': id},
      dataType: 'json',
      success: function(answer) {
        console.log('Success... ');
        console.log(id);
        //$('#'+id).html(answer);
        rebootlinks();
        //$('button#'+id+'.view_'+x).click();
      },
      error: function(answer) {
        console.log('Error... ');
        console.log(answer);
      },
    });  
  });
  
}
  
function loadajax(){
    $.ajax({
      url: 'ajax/storyline/none/',
      success: function(answer) {
        $('.storyline').html(answer)
        $.ajax({
          url: 'ajax/list/none/1/',
          success: function(answer) {
            $('.charlist').html(answer)
            rebootlinks();
          },
        });
      },
    });
}


function rebootlinks(){
  $('.nav').off();
  $('.nav').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val(); 
    if (key == ''){
      key='none';
    }
    $.ajax({
      url: 'ajax/list/'+key+'/'+$(this).attr('page')+'/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });   
  });

  $('.episode_cast').off();
  $('.episode_cast').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    slug = $(this).attr('id');
    $('#customize').val(slug); 
    $.ajax({
      url: 'ajax/list/'+slug+'/'+$(this).attr('page')+'/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });   
  });


  $('#current_storyline').off();
  $('#current_storyline').on('change',function(event){
    event.preventDefault();
    event.stopPropagation();
    slug = $('#current_storyline').val();
    console.log(slug);
    $.ajax({      
      url: 'ajax/storyline/'+slug+'/',
      success: function(answer) {
        $('.storyline').html(answer)
        $.ajax({
          url: 'ajax/list/none/1/',
          success: function(answer) {
            $('.charlist').html(answer)
            rebootlinks();
          },
        });
      },
    });
  });

  $(window).scroll(function(){
    var sticky = $('.menu'), scroll = $(window).scrollTop(), wrap = $('.wrapper');
    if (scroll >= 85){
      sticky.addClass('fixed');
      wrap.addClass('stickyoffset');
    }else{
      sticky.removeClass('fixed');
      wrap.removeClass('stickyoffset');
    }
  });

  


  $('#go').off();
  $('#go').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    //console.log($('.character_form').serialize());
    //console.log($('.character_form input[name=cid]').val());
    var urlupdate = 'ajax/update/character/';
    $.ajax({    
      url: urlupdate,
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {
        cid: $('.character_form input[name=cid]').val(),
        character: $('.character_form').serialize(),
      },
      dataType: 'json',
      success: function(answer) {
          $('.details').html(answer.character);          
          $('li#'+answer.rid).html(answer.line);
          $('li').removeClass('selected');
          rebootlinks();
      },
      error: function(answer) {
        console.log('Error... '+answer);
      },
    });  
  });

  $('#add_character').off();
  $('#add_character').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/add/character/',
      success: function(answer) {
        $('.details').html('done')
        rebootlinks();
      },
      error: function(answer) {
        $('.details').html('oops, broken')
        rebootlinks();
      },

    });
  });

  $('#conf_details').off();
  $('#conf_details').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/conf_details/',
      success: function(answer) {
        console.log(answer);
        $('.details').html(answer)
        rebootlinks();
      },
    });
  });

  $('#build_config_pdf').off();
  $('#build_config_pdf').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/build_config_pdf/',
    }).done(function(answer) {
        console.log(answer.comment);
        $('.details').html(answer.comment);
        rebootlinks();
    });
  });

  $('#seek').off();
  $('#seek').on('click',function(event){
    event.preventDefault();
    key = $('#customize').val(); 
    $.ajax({
      url: 'ajax/view/character/'+key+'/',
      success: function(answer) {
        $('.details').html(answer);
        prepare_ajax();
        rebootlinks();
      },
    });
  });



  $('#search').off();
  $('#search').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val(); 
    if (key == ''){
      key='none';
    }
    $.ajax({
      url: 'ajax/list/'+key+'/1/',
      success: function(answer) {
        $('.charlist').html(answer);
        prepare_ajax();
        rebootlinks();        
      },
    });
  });

  $('.custom_glance').off();
  $('.custom_glance').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    $('#customize').val($(this).attr('id'));
    $('#search').click();
  });



  $('.view_character').off();
  $('.view_character').on('click',function(event){
    console.log('View: '+$(this).attr('id'));
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li');
    $('li').removeClass('selected');
    $(dad).addClass('selected');
    $.ajax({      
      url: 'ajax/view/character/'+$(this).attr('id')+'/',
      success: function(answer) {
        $('.details').html(answer)
        $('li').removeClass('selected');
        rebootlinks();
      },
      error: function(answer){
        console.log('Vew error...'+answer);
      }
    });
  });

  // Touching skills
  $('th.edit span.fa').off();
  $('th.edit span.fa').on('click',function(event){    
    block = $(this).parent();
    sender = block.attr('id').split('_')[1];
    target = 'val_'+block.attr('id').split('_')[1];
    fingerval = 0;
    if ($(this).hasClass('fa-plus-circle')){
      fingerval = 1;
    }
    if ($(this).hasClass('fa-minus-circle')){
      fingerval = -1;
    }
    console.log(sender);
    console.log(target);
    $.ajax({
      url: 'ajax/skill_touch/',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      dataType:'json',
      data: {skill:sender,finger:fingerval},      
      success: function(answer) {
          console.log(answer);
          $('th#'+target).html(answer);
        },
      error: function(answer){
          console.log(answer);
          $('th#'+target).html(answer.responseText);
       },
    });
  
  });

/*
  $('.pdf_character').off();
  $('.pdf_character').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/pdf/'+$(this).attr('id')+'/',
      success: function(answer) {
          $('.details').html(answer)
          
        },
      error: function(answer) {
          $('.details').html(answer)
        },
        
    });
  });
*/
  $('.edit_character').off();
  $('.edit_character').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li');
    $('li').removeClass('selected');
    $(dad).addClass('selected');
    $('body').toggleClass('waiting');
    $.ajax({
      url: 'ajax/edit/character/'+$(this).attr('id')+'/',
      success: function(answer) {
          $('.details').html(answer.character);
          $('body').toggleClass('waiting');         
          prepare_ajax();
          rebootlinks();
      },
      error: function(answer){
        console.log('ooops... :(');
      }
    });
  });

  register_story('epic');
  register_story('drama');
  register_story('act');
  register_story('event');

  $('.tabber').off();
  $('.tabber').on('click', function(event){
    var x = $(this).attr('id');
    $('.tabs').removeClass('tab_up');
    var target = '.tabs#'+x+'t';
    $(target).toggleClass('tab_up');
    console.log(target);
  });

  $('#floatingk').off();
  $('#floatingk').on('click', function(event){
    $(this).find('ul').toggleClass('tab_up');
    console.log('ul.floating_keywords');
  });

  
}

rebootlinks();










/* CSRF code on load */

/*
  function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (i; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');  
  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        console.log("Before send: token is: "+csrftoken);
      }
    }
  });
*/
  // https://www.djangoproject.com/weblog/2011/feb/08/security/
  
          



