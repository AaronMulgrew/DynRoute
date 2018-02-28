function toggleHamburger(item) {
    item.classList.toggle("change");
    // css transitions don't work on visibility so toggle opacity instead.
    //document.getElementById('menubar').classList.toggle('fadein');
    if (document.getElementById('menubar').style.visibility == "visible") {
        // css transitions don't work on visibility so toggle opacity instead.
        document.getElementById('menubar').classList.toggle('fadein');
        setTimeout(function () {
            document.getElementById('menubar').style.visibility = "hidden";
        }, 1000)

    }
    else {
        document.getElementById('menubar').style.visibility = "visible";
        // css transitions don't work on visibility so toggle opacity instead.
        document.getElementById('menubar').classList.toggle('fadein');
    }


}