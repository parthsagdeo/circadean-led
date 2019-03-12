function setProgressbar(id, num) {
    document.getElementById(id).style = "width: " + num + "%";
    document.getElementById(id).innerHTML = num + "%";
}

function getColorAtTime(oFormElement){
    if (!oFormElement.action) { return; }
    var ajax = new XMLHttpRequest();
    ajax.open("post", "/get_color_at_datetime");
    ajax.onload = function() {
        var responseText = ajax.responseText;
        colors_tuple = JSON.parse(responseText);
        console.log(colors_tuple);


        //Get color data
        r_pc = colors_tuple[0]
        g_pc = colors_tuple[1]
        b_pc = colors_tuple[2]
        w_pc = colors_tuple[3]

        // Set progress bars
        setProgressbar("whiteProgressbar", w_pc)
        setProgressbar("redProgressbar", r_pc)
        setProgressbar("greenProgressbar", g_pc)
        setProgressbar("blueProgressbar", b_pc)

        //Set Color
        r_8bit = Math.round(r_pc * 2.55)
        g_8bit = Math.round(g_pc * 2.55)
        b_8bit = Math.round(b_pc * 2.55)

        rgbToHex = function (r, g, b) {
            return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
        }
        document.getElementById("colorCell").style = "width:300px; height:300px; background-color: " + rgbToHex(r_8bit, g_8bit, b_8bit) + ";";

    }
    ajax.send(new FormData(oFormElement))
}