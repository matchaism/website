// 指定されたワーク名の作業ページを取得し、ルートディレクトリに基づいて表示する関数
function IncludeWorkPage(rootdir, subdir, workname, simplecard) {
  $.ajax({

    url: rootdir + "component/" + subdir + workname + ".html",
    cache: false,
    async: false,
    dataType: "html",

  }).done(function(html, status, xhr) {

    // ルートディレクトリのプレースホルダーを実際のルートディレクトリに置換
    html = html.replace(/\{\$root\}/g, rootdir);

    // シンプルカード表示が指定されている場合、対応する要素のみ抽出
    if (simplecard === true) html = $(html).find('.simple-card').html();

    // HTMLをドキュメントに書き込む
    document.write(html);

  });
}

// ヘッダーコンポーネントを取得し、現在のページタイプに応じて表示する関数
function IncludeHeader(rootdir, currentpagetype) {
  $.ajax({

    url: rootdir + "component/header.html",
    cache: false,
    async: false,
    dataType: "html",

  }).done(function(html, status, xhr) {

    // ルートディレクトリのプレースホルダーを実際のルートディレクトリに置換
    html = html.replace(/\{\$root\}/g, rootdir);

    // ルートディレクトリが "./" の場合とそれ以外の場合で処理を分岐
    if (rootdir === "./") {
      html = $(html).find('#navbar-' + currentpagetype).addClass("active").attr("aria-current", "page").attr("href", "#").end().prop('outerHTML');
    } else {
      html = $(html).find('#navbar-' + currentpagetype).addClass("active").attr("aria-current", "page").end().prop('outerHTML');
    }

    // HTMLをドキュメントに書き込む
    document.write(html);

  });
}
