//
//	Christopher Place
//	CS498 Capstone
//  Filename: updates.js
//
//  Overview:
//  Handles all changes on screen
//
//

// Updates File label whenever a file is selected to be displayed on Screen
$(document).on("change", ".custom-file-input", function (event) {
  if (
    typeof document.getElementsByTagName("input")[0].files[0] === "undefined"
  ) {
    $(this).next(".custom-file-label").html("Select File");

  }else{
  $(this).next(".custom-file-label").html(event.target.files[0].name);

  }
});

function pluginUpdate(init){
  let { PythonShell } = require("python-shell");
  const path = require("path");
  var options = {
  scriptPath : path.join('resources','app','src'),
  };
  PythonShell.run("plugins.py", options, function (err, plugins) {
    if(err){
      document.getElementById("alertError").innerHTML ="<strong>Error:</strong> Could not update plugin list."
      $("#alertError").show(); }
    else if(init===false) {
      document.getElementById("alertSuccess").innerHTML ="<strong>Success:</strong> Plugins list updated.";
      $("#alertSuccess").show();
    }
  });

  document.getElementById("command").innerHTML = '<option value="default" selected disabled>Choose Command</option>'

  $.getJSON("./plugins.json", function (data) {
    $.each(data, function (key, command) {
      $("#command").append(
        $("<option></option>")
          .attr("value", command.Command)
          .attr("class", command.OS)
          .text(command.Name)
      );
    });
  });

}

//Update python dependencies using pip script
function pythonDepend(){
  let { PythonShell } = require("python-shell");
  const path = require("path");
  var options = {
  scriptPath : path.join('resources','app','src'),
  };
  PythonShell.run("pythonDepend.py", options, function (err) {
    if(err){
      document.getElementById("alertError").innerHTML ="<strong>Error:</strong> Unable to update Pip dependencies."
      $("#alertError").show(); }
    else{
      document.getElementById("alertSuccess").innerHTML ="<strong>Success:</strong> Pip dependencies updated.";
      $("#alertSuccess").show();
    }
  });

}

//Update Volatility by pulling git repo
function volatilityUpdate(){
  const download = require("download-git-repo");
          download(
            "volatilityfoundation/volatility3",
            "./resources/app/src/volatility3",
            function (err) {
                if(err){
                  document.getElementById("alertError").innerHTML ="<strong>Error:</strong> Could not update Volatility."
                  $("#alertError").show(); }
                else {
                  document.getElementById("alertSuccess").innerHTML ="<strong>Success:</strong> Volatility updated.";
                  $("#alertSuccess").show();
                }
            }
          );
}

// Once the html page loads, query python to have the possible plugins gathered and added to command list
$(document).ready(function () {
  pluginUpdate(true); //Notifies that it is initializing and not to show unless error
  $.fn.dataTable.ext.classes.sPageButton = 'btn btn-outline-danger';
});

// Updates the command list based on platform selected
$("#platform").change(function (event) {
  $("#command").removeAttr("disabled");  
  $("#command option:default").prop("selected", true)
  let platformChosen = document.getElementById("platform");
  let value = platformChosen[platformChosen.selectedIndex].value;
  let commandList = document
    .getElementById("command")
    .querySelectorAll("option");

  commandList.forEach(function (os) {
    if (os.classList.contains(value)) {
      os.style.display = "block";
      $("#command").removeAttr("disabled");
    } else {
      os.style.display = "none";
    }
  });
});

// Removes pop-up for errors when clicked
$("#alertError").on("click", function (event) {
  $("#alertError").hide();
});

//Removes pop-up for success alert when clicked
$("#alertSuccess").on("click", function (event) {
  $("#alertSuccess").hide();
});

//Opens link for volatility in default browser instead of in app
let shell = require("electron").shell
$('a[href^="https://"]').click(function(url){
  url.preventDefault();
  shell.openExternal(this.href);
});