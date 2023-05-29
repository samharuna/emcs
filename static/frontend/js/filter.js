// init Isotope
"use strict";
var $container = $('.portfolio-items').isotope('layout');

// filter items on button click
$('.portfolio-filter').on( 'click', 'a', function filter(e) {
  e.preventDefault();
  var filterValue = $(this).attr('data-filter');
  $container.isotope({ filter: filterValue });


  $('.portfolio-filter li').removeClass('active');
  $(this).closest('li').addClass('active');

});