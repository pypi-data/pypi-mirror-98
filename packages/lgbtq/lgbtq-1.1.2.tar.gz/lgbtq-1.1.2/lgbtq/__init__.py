import requests

class banks:
    btq_default = {
    '_l': 'lgbtq+',
    '_c': 'LGBTQ+',
    '_n': 'lgbtq',
    '-nc': 'LGBTQ',
    '+p': 'pansexual',
    '+l': 'lesbian',
    '+t': 'transexual',
    '+q': 'queer',
    '+fr': 'lesbiangaybisexualtransexualqueer',
    '+q': 'queer',
    '+g': 'gay',
    '+f': 'lesbian, gay, bisexual, transexual, queer, more'
    }

class btq(str):
    def qfy(str, bank=banks.btq_default):
        sentence = str
        al = []
        for key in bank:
            if not key in al:
                al.append(key)
                sentence = sentence.replace(key, bank.get(key))
        return sentence



    
    
    
