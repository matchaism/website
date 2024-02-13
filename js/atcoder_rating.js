function GetAtCoderRating(rootdir) {

  path = rootdir + 'data/atcoder.json';
  lastNewRating = 799;
  maxRating = 799;
  color = '茶色';
  if (rootdir=='../') color = 'Brown';

  $.ajax({

    url: path,
    cache: false,
    async: false,
    dataType: "json"

  }).done(function(data, status, xhr) {

    // データの取得が成功した場合
    try {

      // データの最後の要素からNewRatingを取得
      lastNewRating = data[data.length - 1].NewRating;
      if (rootdir=='../') color = 'Brown';

    } catch (error) {

      // エラーハンドリング: データの取得や処理中にエラーが発生した場合
      console.error('データ処理中にエラーが発生しました:', error);

    }

  }).fail(function(xhr, status, error) {

    // エラーハンドリング: リクエスト自体が失敗した場合
    console.error('atcoder.json の取得に失敗しました:', textStatus, errorThrown);

  }).always(function(arg1, status, arg2) {

    // 取得したNewRatingを表示する要素にセット
    $('#atcoder_raiting').html('<i class="bi bi-graph-up pe-1"></i>Rating ' + lastNewRating + ' (Max '+maxRating+'), ' + color);

  });
}