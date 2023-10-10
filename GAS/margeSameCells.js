// Add a function for testing
function testFunction() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const activeSheet = ss.getActiveSheet();

  const newSheet = createPrintSheet(ss, activeSheet);
  Logger.log('New sheet: ', newSheet);
  clearSameCells(newSheet, 'O6:AZ55');

  function createPrintSheet(ss, sheet) {
    let sheetName = '印刷用';
    let i = 1;
    const copiedSheet = sheet.copyTo(ss);

    while (ss.getSheetByName(sheetName) !== null) {
      sheetName = '印刷用' + i;
      i++;
    }

    deleteRow = 53

    copiedSheet.setName(sheetName);
    copiedSheet.deleteRows(deleteRow, copiedSheet.getLastRow());

    // Assuming copyAndPaste function is defined elsewhere
    copyAndPaste(copiedSheet, 'F6:F54'); // 従業員名
    copyAndPaste(copiedSheet, 'J6:M54'); // 勤務時間、休憩時間
    return copiedSheet;
  }

  function copyAndPaste(sheet, rangeString) {
  const copyRange = sheet.getRange(rangeString);
  const valuesToPaste = copyRange.getValues();

  copyRange.setValues(valuesToPaste);
  }

  function clearSameCells(newSheet, rangeString) {
  const range = newSheet.getRange(rangeString);
  const values = range.getValues();

  for (let i = 0; i < values.length; i++) {
    let startClear = 0;
    let prevValue = values[i][0];
    let j;
      for (j = 1; j < values[i].length; j++) {
        const currentValue = values[i][j];
        if (currentValue !== prevValue || currentValue == "") {
          if (startClear !== j-1 && prevValue !== "") {
            const clearRange = newSheet.getRange(i + range.getRow(), startClear + range.getColumn() + 1, 1, j - startClear - 1);
            clearRange.clearContent();
          }
          startClear = j;
        }
        prevValue = currentValue;
      }
      if (startClear !== j-1 && prevValue !== "") {
        const clearRange = newSheet.getRange(i + range.getRow(), startClear + range.getColumn() + 1, 1, j - startClear - 1);
        clearRange.clearContent();
      }
    }
  }


}