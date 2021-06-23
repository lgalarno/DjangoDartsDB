let gamecategory = document.getElementById("gamecategory").value;

if (gamecategory == '501'){
    setSelectOption ();
}

function setSelectOption () {
    let nplayers = document.getElementsByName('pscore');
    let nplayersCount = 0;

    for (var i = 0; i < nplayers.length; i++) {
      if (nplayers[i].hasAttribute("disabled")) {} else {nplayersCount++;}
    }
    for (var i = 0; i < nplayers.length; i++) {
        nplayers[i].options.length=0;
        for (var j = 0; j < nplayersCount; j++) {
            var opt = document.createElement('option');
            opt.text = j+1;
            opt.value = j+1;
            nplayers[i].add(opt, null);
        }
    }
}

function disableSelect(clicked_id){
    let splitID = clicked_id.split("-");
    let playerID = splitID[splitID.length - 1];
    let pscoreID = 'pscore-'.concat(playerID);
    //var c = "{{ gamecategory|safe }}";
    if(document.getElementById(clicked_id).checked == true){
        document.getElementById(pscoreID).removeAttribute("disabled");
    }else{
        document.getElementById(pscoreID).setAttribute("disabled","disabled");
    }
    if (gamecategory == '501'){
        setSelectOption ();
    }
}