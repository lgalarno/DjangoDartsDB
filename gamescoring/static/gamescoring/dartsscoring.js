window.onload=function(){
    //console.log(gamecategory);
    if (gamecategory == '501'){
        setSelectOption ();
    }
}

function setSelectOption () {
    var nplayers = document.getElementsByName('pscore');
    var nplayersCount = 0;

    for (var i = 0; i < nplayers.length; i++) {
      if (nplayers[i].hasAttribute("disabled")) {} else {nplayersCount++;}
    }
    //console.log(nplayersCount);
    for (var i = 0; i < nplayers.length; i++) {
        //console.log(nplayers[i]);
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
    var splitID = clicked_id.split("-");
    var playerID = splitID[splitID.length - 1];
    var pscoreID = 'pscore-'.concat(playerID);
    //var c = "{{ gamecategory|safe }}";
    console.log(gamecategory)
    if(document.getElementById(clicked_id).checked == true){
        document.getElementById(pscoreID).removeAttribute("disabled");
    }else{
        document.getElementById(pscoreID).setAttribute("disabled","disabled");
    }
    if (gamecategory == '501'){
        setSelectOption ();
    }
}