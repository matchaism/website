$.getJSON('./data/atcoder.json', function(data) {

  // データの取得が成功した場合
  try {

    // データの最後の要素からNewRatingを取得
    var lastNewRating = data[data.length - 1].NewRating;
    // 取得したNewRatingを表示する要素にセット
    $('#atcoder_raiting').html('<i class="bi bi-graph-up pe-1"></i>Rating ' + lastNewRating + ' (Max 799), 茶色');

  } catch (error) {

    // エラーハンドリング: データの取得や処理中にエラーが発生した場合
    console.error('データ処理中にエラーが発生しました:', error);
    $('#atcoder_raiting').html('<i class="bi bi-graph-up pe-1"></i>Rating 799 (Max 799), 茶色');

  }

}).fail(function(jqXHR, textStatus, errorThrown) {

  // エラーハンドリング: リクエスト自体が失敗した場合
  console.error('./data/atcoder.json の取得に失敗しました:', textStatus, errorThrown);
  $('#atcoder_raiting').html('<i class="bi bi-graph-up pe-1"></i>Rating 799 (Max 799), 茶色');

});
