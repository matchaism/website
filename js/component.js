function IncludeWorkPage(rootdir, workname, simplecard){
  $.ajax({
    url: rootdir + "component/work/" + workname + ".html",
    cache: false,
    async: false,
    dataType: "html",
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootdir);
      if(simplecard==true){
        html = $(html).find('#simple-card').html();
      }
      document.write(html);
    }
  });
}

function IncludeHeader(rootdir, currentpagetype){
  $.ajax({
    url: rootdir + "component/header.html",
    cache: false,
    async: false,
    dataType: "html",
    success: function(html){
      html = html.replace(/\{\$root\}/g, rootdir);
      if(rootdir=="./"){
        html = $(html).find('#navbar-'+currentpagetype).addClass("active").attr("aria-current", "page").attr("href", "#").end().prop('outerHTML');
      }else{
        html = $(html).find('#navbar-'+currentpagetype).addClass("active").attr("aria-current", "page").end().prop('outerHTML');
      }
      document.write(html);
    }
  });
}