function goToUrl() {
  const url = "http://yoojiyangportfolio.pythonanywhere.com";
  const html = '<script>window.open("' + url + '"); google.script.host.close();</script>';
  const userInterface = HtmlService.createHtmlOutput(html)
    .setWidth(10)
    .setHeight(10);
  SpreadsheetApp.getUi().showModalDialog(userInterface, 'Opening URL');
}
