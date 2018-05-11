class Tegel:

    def __init__(self, getal=0):
        """
        constructor functie voor een tegel, 
        neemt een getal in [0, 15] dat aangeeft
        wat voor tegel het is
        """
        if getal < 0 or getal > 15:
            raise AssertionError('ongeldige tegel')
        else:
            self.getal = getal
            self.bin_to_sides(maak_bin(getal))

    def __str__(self):
        """
        geeft de stringweergave van een tegel trug
        """
        chars = {0: ' ', 1: '╹', 2: '╺', 3: '┗', 4: '╻', 5: '┃', 6: '┏', 7: '┣', 8: '╸', 9: '┛' ,10: '━', 11: '┻', 12: '┓', 13: '┫', 14: '┳', 15: '╋'}
        return chars[self.getal]

    def draai(self, wijzerzin=True):
        """
        draait een tegel in wijzerzin of tegen wijzerzin
        standaard in wijzerzin
        """
        w = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 1, 9: 3, 10: 5, 11: 7, 12: 9, 13: 11, 14: 13, 15: 15}
        tw = {0: 0, 1: 8, 2: 1, 4: 2, 8: 4, 3: 9, 5: 10, 6: 3, 7: 11, 9: 12, 10: 5, 11: 13, 12: 6, 13: 14, 14: 7, 15: 15}
        if wijzerzin:
            self.getal = w[self.getal]
        else:
            self.getal = tw[self.getal]
        self.bin_to_sides(maak_bin(self.getal))
        return self

    def bin_to_sides(self, b):
        """
        zet welke zijden er zijn op basis van een binair getal
        """
        self.boven = b[3] == '1'
        self.rechts = b[2] == '1'
        self.onder = b[1] == '1'
        self.links = b[0] == '1'
    

class OneindigeLus:
    
    def __init__(self, tegels, kol, score):
        """
        constructor functie voor een spel van Oneindigde lus,
        neemt een reeks getallin in die de tegels voorsstellen,
        en het aantal kolommen voor het spelbord
        """
        if len(tegels) % kol != 0:
            raise AssertionError('ongeldig rooster')
        self.tegels = []
        self.score = score
        self.kol = kol
        rij = []
        for getal in tegels:
            rij.append(Tegel(getal))
            if len(rij) == kol:
                self.tegels.append(rij)
                rij = []

    def __str__(self):
        """
        geeft de stringweergave van het spelbord trug
        """
        string = ''
        for rij in self.tegels:
            for tegel in rij:
                string += str(tegel)
            string += '\n'
        return string[0:-1]


    def draai(self, rij, kol, wijzerzin=True):
        """
        roept de draai functie op van een tegel uit het spelbord
        """
        if rij > len(self.tegels) or kol > len(self.tegels[0]):
            raise AssertionError('ongeldige positie')
        self.tegels[rij][kol].draai(wijzerzin)
        return self

    def opgelost(self):
        """
        kijkt na of de puzzel opgelost is
        """
        for rij in range(len(self.tegels)):
            for kol in range(len(self.tegels[0])):
                tegel = self.tegels[rij][kol]
                buren = self.get_buren(rij, kol)
                if (
                    (buren[0].onder != tegel.boven) or
                    (buren[1].links != tegel.rechts) or
                    (buren[2].boven != tegel.onder) or
                    (buren[3].rechts != tegel.links)
                ):
                    return False
        return True

    def get_buren(self, rij, kol):
        """
        geeft alle buren trug van een opgegeven coordinaat van het spelbord
        """
        rijen = len(self.tegels)
        kols = len(self.tegels[0])
        ri = [rij -1 * (rij > 0), rij, rij +1 * (rij < rijen-1), rij]
        ki = [kol, kol +1 * (kol < kols-1), kol, kol -1 * (kol > 0)]
        buren = []
        for i in range(4):
            buur = self.tegels[ri[i]][ki[i]]
            if buur != self.tegels[rij][kol]:
                buren.append(buur)
            else:
                buren.append(Tegel(0))
        return buren

    def state(self):
        """
        geeft dict trug die de huidige staat van het spel beschrijft
        """
        staat = {
            "tegels": self.board_state(),
            "board": str(self).split('\n'),
            "kol": self.kol,
            "rij": len(self.tegels),
            "score": self.score,
            "message": "Proficiat! Je hebt de puzzel opgelost in %d stappen"%self.score * self.opgelost()
        }
        return staat

    def board_state(self):
        board = []
        for r in self.tegels:
            for t in r:
                board.append(t.getal)
        return board



def maak_bin(getal):
    """
    geeft de binaire weergave van het opgegeven getal, 
    voorgegaan door het juiste aantal nullen zodat het altijd
    een lentgte van 4 heeft
    """
    b = bin(getal)[2:]
    while len(b) < 4:
        b = '0' + b
    return b


spel = OneindigeLus([9, 12, 12, 6, 10, 13, 13, 5, 3, 3, 9, 3], 4, 0)
print(spel.board_state())