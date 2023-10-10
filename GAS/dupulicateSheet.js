// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// 必要情報の取得
// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// シートを取得
const ss = SpreadsheetApp.getActiveSpreadsheet();
const shiftSheet = ss.getSheetByName('①出勤可否連絡シート');
const assignSheetTemplate = ss.getSheetByName('アサイン表(コピー元)');
const masterShiftSheet = ss.getSheetByName('シフト表マスタ');
const workDataSheet = ss.getSheetByName('勤務情報');
const targetPeriodSheet = ss.getSheetByName('③実行ページ');
const sheets = ss.getSheets();

// 出勤可否連絡シートから試合日付と試合開始時間を取得

// 試合開始時間別のシフト表マスタからのデータ取得範囲の設定
const assignPattern = {
  // 13時試合開始
  "13" : {
    icRange: 'I10:I42',
    positionRange: 'K9:AV42',
  },
  // 14時試合開始
  "14" : {
    icRange: 'I50:I82',
    positionRange: 'K49:AV82',
  },
  // 18時試合開始
  "18" : {
    icRange: 'I100:I132',
    positionRange: 'K99:AV132',
  },
}

// 複製したシートの貼り付け先範囲
const setIcRange = 'I6:I38';
const setPositionRange = 'O5:AZ38';

// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// 補助関数
// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝

// 日付データをmm/dd形式に変換する処理
function formatDate(dateValue) {
  const timeZone = Session.getScriptTimeZone();
  const formattedDate = Utilities.formatDate(new Date(dateValue), timeZone, "MM/dd");
  return formattedDate;
}

// 試合の日付を取得し、 mm/dd形式に加工して、gameDateValues配列に格納する
function getAllGameDates() {
  const allGameDates = [];

  // シフトシートから日付の範囲を取得
  const gameDateValuesRow = shiftSheet.getRange('D2:U2').getValues()[0];

  // 各日付をフォーマットし、新しい配列に追加
  gameDateValuesRow.forEach((dateValue) => {
    if (dateValue !== "") {
      try {
        const formattedDate = formatDate(dateValue);
        allGameDates.push(formattedDate);
      } catch (error) {
        console.error(`Date formatting error for value: ${dateValue}`, error);
      }
    }
  });

  return allGameDates;
}

// 対象期間を取得
function getTargetPeriod() {
  // 値があることを確認
  if (!targetPeriodSheet) {
    throw new Error("Sheet 'アサイン対象期間設定' not found");
  }

  // 対象期間情報を取得
  const startPeriodData = targetPeriodSheet.getRange('B4').getValue(); 
  const endPeriodData = targetPeriodSheet.getRange('D4').getValue(); 

  // mm/dd形式に変換
  const startPeriod = formatDate(startPeriodData);
  const endPeriod = formatDate(endPeriodData);

  return { startPeriod, endPeriod };
}

// 今回の処理の対象となる期間を設定
function selectTargetGameDates() {
  const { startPeriod, endPeriod } = getTargetPeriod();
  const allGameDates = getAllGameDates();
  const targetGameDates =[];

  allGameDates.forEach((date, index) => {
    if (date >= startPeriod && date <= endPeriod) {
      targetGameDates.push(date);
    };
  });

  return targetGameDates;
}

// データを貼り付ける処理
function pasteValues(sheet, range, values) {
  sheet.getRange(range).setValues(values);
}

// シートを複製して、必要情報を貼り付ける
function pasteData(dateValue, index) {
    const newAssignSheet = assignSheetTemplate.copyTo(ss);

    // 複製したシートの名前を試合日の日付に設定し、そのシートのF２セルにも試合日を入力する。
    newAssignSheet.setName(dateValue);
    newAssignSheet.getRange('F2').setValue(dateValue);
    newAssignSheet.setTabColor("yellow");

    // 複製したアサイン表に試合開始時間ごとのアサインのテンプレを貼り付ける
    // データを取得 
    const playballTimeValuesRow = shiftSheet.getRange('D4:T4').getValues()[0];
    const playballTime = playballTimeValuesRow[index].substring(0, 2);; // その日付の試合時間を取得する。
    const targetDateAssignment = assignPattern[playballTime]; // 試合時間に対応するデータの取得範囲を設定
    // 取得したデータを貼り付け
    pasteValues(newAssignSheet, setIcRange, masterShiftSheet.getRange(targetDateAssignment.icRange).getValues());
    pasteValues(newAssignSheet, setPositionRange, masterShiftSheet.getRange(targetDateAssignment.positionRange).getValues());

}

// 対応している日付と同じ名前のシートがある場合、対応するセルに日付を出力する
function workDataRefresh() {
  const allGameDates = getAllGameDates();
  const sheetNames = ss.getSheets().map(sheet => sheet.getName());

  const printRow = 2;
  const startColumn = 19; // S列目

  allGameDates.forEach((dateValue, index) => {
    console.log(`dateValue: ${dateValue}`);
    console.log(`dateValue: ${typeof(dateValue)}`);
    console.log(`sheetNames: ${sheetNames}`);
    console.log(dateValue === sheetNames);

    if (sheetNames.includes(dateValue)) {
      workDataSheet.getRange(printRow, startColumn + index).setValue(dateValue);
    } else {
      workDataSheet.getRange(printRow, startColumn + index).setValue("----");
    }
  });
}

// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
// メイン関数
// ＝＝＝＝＝＝＝＝＝＝＝＝＝＝


// アサイン表の複製処理
function createAssignSheets() {

  // 今回設定する試合日付の配列を設定
  const targetGameDates = selectTargetGameDates();
  
  // 既存のシート名のリストを取得
  const sheetNames = ss.getSheets().map(sheet => sheet.getName());
  
  // 対象期間の試合日ごとのアサイン表の雛形を作成する
  targetGameDates.forEach((dateValue, index) => {

    // 既に同じ日付のシートが存在する場合はスキップ
    if (sheetNames.includes(dateValue)) {
      return;
    }

    // アサイン表を複製し、必要なデータを貼り付ける
    pasteData(dateValue, index);

  });

  // 保留中の変更を強制的に適用
  SpreadsheetApp.flush();

  // 勤務情報シートの日付を入力
  workDataRefresh();

}