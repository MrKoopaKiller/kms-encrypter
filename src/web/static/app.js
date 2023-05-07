function getKMSAliases() {
  var accountValue = document.getElementById("account-dropdown").value;
  var regionValue = document.getElementById("region-dropdown").value;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var aliasesDropdown = document.getElementById("aliases-dropdown");
        aliasesDropdown.innerHTML = "";

        var aliasesArray = JSON.parse(xhr.responseText);
        for (var i = 0; i < aliasesArray.length; i++) {
          var option = document.createElement("option");
          option.text = aliasesArray[i];
          aliasesDropdown.add(option);
        }
      } else {
        console.log("Error: " + xhr.status);
      }
    }
  };
  xhr.open(
    "GET",
    "/api/getKMSAliases?account=" + accountValue + "&region=" + regionValue,
    true
  );
  xhr.send();
}

function encryptData() {
  var accountValue = document.getElementById("account-dropdown").value;
  var aliasValue = document.getElementById("aliases-dropdown").value;
  var inputText = document.getElementById("input-text").value;
  var regionValue = document.getElementById("region-dropdown").value;
  var encContextKey = document.getElementById("enc-context-key").value;
  var encContextValue = document.getElementById("enc-context-value").value;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var outputTextarea = document.getElementById("output-text");
        outputTextarea.value = xhr.responseText;
      } else {
        console.log("Error: " + xhr.status);
      }
    }
  };
  xhr.open("POST", "/api/encryptData", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(
    JSON.stringify({
      account: accountValue,
      region: regionValue,
      alias: aliasValue,
      input: inputText,
      context: (encContext = encContextKey + "=" + encContextValue),
    })
  );
}

function copyToClipboard() {
  var outputText = document.getElementById("output-text").value;
  var tempTextarea = document.createElement("textarea");
  tempTextarea.value = outputText;
  document.body.appendChild(tempTextarea);
  tempTextarea.select();
  document.execCommand("copy");
  document.body.removeChild(tempTextarea);
}
