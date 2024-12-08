$(function() {
  queryString = window.location.search;
  params = new URLSearchParams(queryString);
  lang = params.get('lang'); //'jp', 'en', 'null
  // switch visible contents
  if (lang === 'en') {
    $('.lang-jp').hide();
    $('.lang-en').show();
  } else {
    $('.lang-en').hide();
    $('.lang-jp').show();
  }
})
