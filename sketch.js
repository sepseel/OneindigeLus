var staat = {};
var grid = false;
//const url = "http://users.ugent.be/~sevbesau/cgi-bin/script.cgi?";
var url = "http://0.0.0.0:8080/cgi-bin/infinitycgi.cgi?";



update = function(state) {
    // als er nog geen grid van divs bestaat, maak er dan een 
    if (!grid) {
        makeGrid(3, 4);
        grid = true;
    }

    // spelbord updaten
    for (let i = 0; i < state.board.length; i++) {
        for (let j = 0; j < state.board[0].length; j++) {
            $('#' + i + "" + j).text(state.board[i][j])
            $('#' + i + "" + j).fitText(0.1)
        }
    }

    // score updaten
    $('#score').text('stappen: ' + state.score)

    // als er een bericht is, geef het dan weer
    if (state.message) {
        alert(state.message);
    }
    
    // state opslagen als stringweergave
    staat = JSON.stringify(state)
}

makeGrid = function(r, k) {
    // maakt een leeg div grid aan met het opgegeven aantal rijen en kolommen
    grid = true;
    for (let i = 0; i < r; i++) {
        $(".rooster").append("<div id='row" + i + "'></div>")
        for (let j = 0; j < k; j++) {
            $("#row" + i).append("<div id='" + i + "" + j + "' class='tegel'></div>")
        }
    }
}

Startnew = function() {
    // start een nieuw spel
    fetch(url + "func=new_game")
    .then(function(response) {
        return response.json(); 
    })
    .then(function(myJson) {
        update(myJson);
        console.log('new', myJson)
    });
    
}

maakZet = function(staat, rij, kol) {
    // maakt een zet op basis van de opgeslagen staat en de geselecteerde kleur
    fetch(url + 'func=do_move&' + 'state=' + staat + '&rij=' + rij + '&kol=' + kol)
    .then(function(response) {
        return response.json(); 
    })
    .then(function(myJson) {
        update(myJson);
        console.log(myJson)
    });
};


makeGrid(3, 4)
Startnew();


$(document).ready(function(){
    // word uitgevoerd wanneer alle html geladen is

    $('.tegel').click(function(event){
        rij = event.target.id[0]
        kol = event.target.id[1]
        maakZet(staat, rij, kol)
    })
    

    $('#new').click(function(){
        Startnew();
    });

});
