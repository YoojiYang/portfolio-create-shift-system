function calculateValues() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName('②従業員マスタ[編集用]');
  const bToKValues = sheet.getRange('B4:K100').getValues();
  const pToAAValues = sheet.getRange('P4:AA11').getValues();

  // 処理開始時にメッセージを出力
  const messageCell = 'AC18';
  sheet.getRange(messageCell).clearContent();
  sheet.getRange(messageCell).setValue("更新中...");
  // 保留中の変更を強制的に適用
  SpreadsheetApp.flush();

  // スキル値を初期化
  const clearRange = 'L4:L100'
  sheet.getRange(clearRange).clearContent();

  // 文字列が一致したら1を返し、そうでなければ0を返す処理
  function checkValue(value, referenceString) {
    return value === referenceString ? '1' : '0';
  }

  // ポジション別の優先順位を確認する処理
  function findNameIndex(row, col, name) {
    for (let j = 0; j < pToAAValues.length; j++) {
      if (pToAAValues[j][col] === name) {
        return (j + 1).toString();
      }
    }
    return '0';
  }

  // 25桁のスキルコードを1桁ずつ設定する
  for (let i = 0; i < bToKValues.length; i++) {
    let result = '';

    // 1桁目の処理
    result += checkValue(bToKValues[i][2], "OK!"); // D列

    // 2桁目から21桁目の処理
    let previousValue = 0;
    for (let digit = 1; digit <= 20; digit++) {
      const bToICol = Math.floor((digit - 1) / 4) + 3; // E列からスタートして4桁ごとに1列ずつ右に移動
      const pToYCol = Math.floor((digit - 1) / 2); // P列からスタートして2桁ごとに1列ずつ右に移動
      const referenceString = (digit % 4 <= 1) ? "main" : "sub"; // 2桁ごとに参照文字列を変更

      if (digit % 2 !== 0) { // 奇数桁
        previousValue = checkValue(bToKValues[i][bToICol], referenceString);
        result += previousValue;
      } else if (previousValue === '1') { // 偶数桁
        const name = bToKValues[i][1]; // C列はBから数えて2番目
        result += findNameIndex(i, pToYCol, name);
      } else {
        result += '0';
      }
    }

    // 22桁目と25桁目の処理
    for (let digit = 21; digit <= 24; digit++) {
      const jToKCol = Math.floor((digit - 21) / 2) + 8; // J列からスタートして2桁ごとに1列ずつ右に移動
      const zToAaCol = Math.floor((digit - 21) / 2) + 10; // Z列からスタートして2桁ごとに1列ずつ右に移動

      if (digit % 2 !== 0) { // 奇数桁
        previousValue = checkValue(bToKValues[i][jToKCol], "main");
        result += previousValue;
      } else if (previousValue === '1') { // 偶数桁
        const name = bToKValues[i][1]; // C列はBから数えて2番目
        result += findNameIndex(i, zToAaCol, name);
      } else {
        result += '0';
      }
    }
    sheet.getRange('L' + (i + 4)).setValue(result);
  }

  // 処理終了時にメッセージを出力
  sheet.getRange(messageCell).clearContent();
  sheet.getRange(messageCell).setValue("完了しました！");
}
