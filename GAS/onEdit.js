function onEdit(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const activeSheet = ss.getActiveSheet();
  const editedRange = e.range;
  const row = editedRange.getRow();
  const column = editedRange.getColumn();

  if (column === 10 && row >= 3 && row <= 99 && editedRange.getValue() === true && activeSheet.getName() === '②従業員マスタ[編集用]') {
    processMatchingRows(ss, row);
  }

  if (editedRange.getA1Notation() === 'J2' && activeSheet.getRange('J2').getValue() === true) {
    sortRange(activeSheet);
  }

  if (editedRange.getA1Notation() === 'K2' && activeSheet.getRange('K2').getValue() === true) {
    // createPrintSheet now returns the newly created sheet
    const newSheet = createPrintSheet(ss, activeSheet);
    // apply mergeSameCells function to the newly created sheet
    mergeSameCells(newSheet, 'O6:AZ54');
  }

  if (activeSheet.getName().includes('/')) {
    processEmployeeMaster(e);
  }
}

function processMatchingRows(ss, row) {
  const sheetsToProcess = ['①出勤可否連絡シート', 'シフト表(確定)', '勤務情報', '従業員マスタ'];
  const masterSheet = ss.getSheetByName('従業員マスタ[編集用]');
  const matchValue = masterSheet.getRange('B' + row).getValue();

  sheetsToProcess.forEach(function(sheetName) {
    const sheet = ss.getSheetByName(sheetName);
    const columnRange = (sheetName === '①出勤可否連絡シート') ? 'AD' : 'B';
    deleteMatchingRow(sheet, matchValue, 'B', columnRange);
  });

  // Delete the row in masterSheet and shift up
  masterSheet.deleteRow(row);
  
  // Copy the data from row to end and paste it from row-1
  const dataToMove = masterSheet.getRange('A' + (row + 1) + ':' + 'J' + masterSheet.getLastRow()).getValues();
  masterSheet.getRange('A' + row + ':' + 'J' + (masterSheet.getLastRow() - 1)).setValues(dataToMove);
  
}

// make createPrintSheet return the newly created sheet
function createPrintSheet(ss, sheet) {
  const sheetName = '印刷用';
  const i = 1;
  const copiedSheet = sheet.copyTo(ss);

  while (ss.getSheetByName(sheetName) !== null) {
    sheetName = '印刷用' + i;
    i++;
  }

  copiedSheet.setName(sheetName);
  copiedSheet.deleteRows(57, copiedSheet.getLastRow() - 40);

  copyAndPaste(copiedSheet, 'F6:F54');
  copyAndPaste(copiedSheet, 'J6:M54');

  // return the newly created sheet
  return copiedSheet;
}

function copyAndPaste(sheet, rangeString) {
  const copyRange = sheet.getRange(rangeString);
  const valuesToPaste = copyRange.getValues();

  copyRange.setValues(valuesToPaste);
}

function processEmployeeMaster(e) {
  const activeSheet = e.source.getActiveSheet();
  const editedRange = e.range;
  const editedColumn = editedRange.getColumn();

  if (editedColumn === 5) {
    const masterSheet = e.source.getSheetByName('従業員マスタ');
    const masterValues = masterSheet.getRange('B2:C' + masterSheet.getLastRow()).getValues();

    const editedValue = editedRange.getValue();
    for (const i = 0; i < masterValues.length; i++) {
      if (masterValues[i][1] === editedValue) {
        activeSheet.getRange(editedRange.getRow(), 3).setValue("'" + masterValues[i][0]);
        break;
      }
    }
  }
}

function deleteMatchingRow(sheet, matchValue, startColumn, endColumn) {
  const data = sheet.getRange(startColumn + '1:' + endColumn + sheet.getLastRow()).getValues();
  for (const i = 0; i < data.length; i++) {
    if (data[i][0] == matchValue) {
      sheet.deleteRow(i + 1);
      break;
    }
  }
}

function mergeSameCells(sheet, rangeString) {
  const range = sheet.getRange(rangeString);
  const values = range.getValues();

  for (const i = 0; i < values.length; i++) {
    const startMerge = 0;
    const prevValue = values[i][0];
    for (const j = 1; j < values[i].length; j++) {
      const currentValue = values[i][j];
      if (currentValue !== prevValue || currentValue == "") {
        if (startMerge !== j-1 && prevValue !== "") {
          const mergeRange = sheet.getRange(i + range.getRow(), startMerge + range.getColumn(), 1, j - startMerge);
          mergeRange.merge();
        }
        startMerge = j;
      }
      prevValue = currentValue;
    }
    if (startMerge !== j && prevValue !== "") {
      const mergeRange = sheet.getRange(i + range.getRow(), startMerge + range.getColumn(), 1, j - startMerge);
      mergeRange.merge();
    }
  }
}