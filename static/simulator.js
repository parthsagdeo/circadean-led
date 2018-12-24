function load_current_color(){
    var ajax = new XMLHttpRequest();
    ajax.open("GET", "/get_current_color", true);
    ajax.onload = function() {
        var responseText = ajax.responseText;
        colors_dict = JSON.parse(responseText);
        console.log(colors_dict);
        setProgressbar = function(id, num) {
          document.getElementById(id).style = "width: " + num + "%";
          document.getElementById(id).innerHTML = num + "%";
        }
        
        //Get color data
        w_pc = colors_dict['w']
        r_pc = colors_dict['r']
        g_pc = colors_dict['g']
        b_pc = colors_dict['b']
        
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
    ajax.send()
}

load_current_color();