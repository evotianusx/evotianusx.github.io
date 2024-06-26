---
title: Google App Script
---

Needed to copy and rename a google sheet ? For example you have a template and needed to create a brand new instance each day

Can use the code snippet below

1. Open the template in google sheet
2. Go to Extensions -> App Script
3. Copy and paste the script into the box
   - You might need to create a project, just follow the steps
4. Hit Run and it will then create a duplicates of the template sheet

```js

# There is a +- 5 minutes run time, and each creation of sheet takes +- 5 seconds
# You might need to create
function myFunction() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  # Example duplicate the file 10 times, with an ascending counter
  duplicate = 10;
  for (var i = 0; i <= duplicate; i++) {
    # Here I pad the number to be 4 digits, but this can be changed as per requirement
    var new_sheet = ss.copy("Pohon-" + String(i).padStart(4, '0'));
    # It will then print the sheet URL into the log 
    Logger.log(String(i) + "|" + new_sheet.getUrl());
  }
}
```