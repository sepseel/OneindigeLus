class Tegel {

    constructor(getal=0) {
        if (getal < 0 || getal > 15) {
            throw {
                name: 'AssertionError',
                message: 'ongeldige tegel'
            };
        } else {
            this.getal = getal;
            this.bin_to_sides(maak_bin(getal));
        }
    }

    toString() {
        let chars = {0: ' ', 1: '╹', 2: '╺', 3: '┗', 4: '╻', 5: '┃', 6: '┏', 7: '┣', 8: '╸', 9: '┛' ,10: '━', 11: '┻', 12: '┓', 13: '┫', 14: '┳', 15: '╋'};
        return chars[this.getal];
    }

    draai(zin=true) {
        let wijzerzin = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 1, 9: 3, 10: 5, 11: 7, 12: 9, 13: 11, 14: 13, 15: 15};
        let tegenwijzerzin = {0: 0, 1: 8, 2: 1, 4: 2, 8: 4, 3: 9, 5: 10, 6: 3, 7: 11, 9: 12, 10: 5, 11: 13, 12: 6, 13: 14, 14: 7, 15: 15};
        if (zin === true) {
            this.getal = wijzerzin[this.getal];
        } else {
            this.getal = tegenwijzerzin[this.getal];
        }
        this.bin_to_sides(maak_bin(this.getal));
        return this;
    }

    bin_to_sides(bin) {
        this.boven = bin[3] == true;
        this.rechts = bin[2] == true;
        this.onder = bin[1] == true;
        this.links = bin[0] == true;
    }
} 


class OneindigeLus {

    constructor(tegels, kol) {
        if (tegels.length % kol !== 0) {
            throw {
                name: 'AssertionError',
                message: 'ongeldig rooster'
            };
        }
        this.tegels = [];
        let rij = [];
        for (let getal of tegels) {
            rij.push(new Tegel(getal));
            if (rij.length == kol) {
                this.tegels.push(rij);
                rij = [];
            }
        }
    }

    toString() {
        let string = '';
        for (let rij of this.tegels) {
            for (let tegel of rij) {
                string += tegel.toString();
            }
            string += '\n'
        }
        return string.substring(0, string.length-1);
    }

    draai(rij, kol, wijzerzin=true) {
        if (rij > this.tegels.length || kol > this.tegels[0].length) {
            throw {
                name: 'AssertionError',
                message: 'ongeldige positie'
            };
        }
        this.tegels[rij][kol].draai(wijzerzin);
        return this;
    }

    opgelost() {
        let buren;
        let tegel;
        for (let rij = 0; rij < this.tegels.length; rij++) {
            for (let kol = 0; kol < this.tegels[0].length; kol++) {
                tegel = this.tegels[rij][kol];
                buren = this.get_buren(rij, kol);
                if ((buren[0].onder != tegel.boven) ||
                    (buren[1].links != tegel.rechts) ||
                    (buren[2].boven != tegel.onder) ||
                    (buren[3].rechts != tegel.links)) {
                        return false;
                    }
            }
        }
        return true;
    }

    get_buren(rij, kol) {
        // boven, rechts, onder, links
        let zijkant = new Tegel();
        let rijen = this.tegels.length;
        let kols = this.tegels[0].length;
        let ri = [rij -1 * (rij > 0), rij, rij +1 * (rij < rijen-1), rij];
        let ki = [kol, kol +1 * (kol < kols-1), kol, kol -1 * (kol > 0)];
        let buren = [];
        let buur;
        for (let i = 0; i < 4; i++) {
            buur = this.tegels[ri[i]][ki[i]];
            if (buur != this.tegels[rij][kol]) {
                buren.push(buur);
            } else {
                buren.push(zijkant);
            }
        }
        return buren;
    }
}

maak_bin = function(getal) {
    let bin = (getal >>> 0).toString(2);
    while (bin.length < 4) {
        bin = '0' + bin;
    }
    return bin;
}