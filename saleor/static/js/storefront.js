/* @flow */

import 'bootstrap-sass'
import $ from 'jquery'
import 'jquery.cookie'

import '../scss/storefront.scss'

let csrftoken = $.cookie('csrftoken')

function csrfSafeMethod(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken)
    }
  }
})

$(function() {
  const $carousel = $('.carousel')
  const $items = $('.product-gallery-item')
  const $modal = $('.modal')

  $items.on('click', function(e) {
    if ($carousel.is(':visible')) {
      e.preventDefault()
    }
    const index = $(this).index()
    $carousel.carousel(index)
  })

  $modal.on('show.bs.modal', function() {
    const $img = $(this).find('.modal-body img')
    const dataSrc = $img.attr('data-src')
    $img.attr('src', dataSrc)
  })
})


// Address offices dynamic forms
function onToOfficeChange() {
  let $toOfficeCheckbox = $('#id_to_office');
  if ($toOfficeCheckbox) {
    if ($toOfficeCheckbox.is(':checked')) {
      $('#id_office').prop("disabled", false);

      $('#id_street_address_1').prop("disabled", true);
      $('#id_street_address_2').prop("disabled", true);
      $('#id_city_area').prop("disabled", true);
    } else {
      $('#id_office').prop("disabled", true);

      $('#id_street_address_1').prop("disabled", false);
      $('#id_street_address_2').prop("disabled", false);
      $('#id_city_area').prop("disabled", false);
    }
  }
}

$("#id_to_office").click(onToOfficeChange).change(onToOfficeChange);

function filterOffices() {
    $("#id_city").change(function () {
    var optionSelected = $(this).find("option:selected");
    var valueSelected = optionSelected.val();

    $.ajax({
      type: 'GET',
      url: '/shipping/cities/' + valueSelected + '/offices/',
      dataType: 'json',
      success: function (json) {

        console.log(json);
        $('#id_office option').remove();
        $("#id_office").append('<option value="" selected="selected">---------</option>');
        for (var i = json.length - 1; i >= 0; i--) {
          console.log('<option value="' + json[i].id + '">' + json[i].name + '</option>');
          $("#id_office").append('<option value="' + json[i].id + '">' + json[i].name + '</option>');
        }
      }
    });
  });
}

filterOffices();

$(document).ready(function () {
    onToOfficeChange();
});

$(function() {
    $(".language_change").click(function() {
      var form = $("#language_form");
      var code = $(this).data("code");

      form.find("input[name=language]").val(code);
      form.submit();
    });
});
