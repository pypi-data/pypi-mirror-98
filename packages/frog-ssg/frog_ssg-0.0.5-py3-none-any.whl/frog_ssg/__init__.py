from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
from shutil import copytree

print("\n|| Frog: __main__ executing ||\n")

class Frog():
    def __init__(self):
        self.output_folder = Path("output/")
    
    def build(self):
        print("\n|| Frog: build placeholder ||\n")


class Reader():
    def __init__(self, path):
        self.path = path # a pathlib path object
    
    def read(self):
        '''
            Returns a dict of content, read from self.path
        '''
        
        data = {
            "päälause": "",
            "tukilause": "",
            "yritys": "",
            "esittely": "",
            "kappale_1": [], # [otsikko, sisältö]
            "kappale_2": [],
            "kappale_3": [],
            "palvelu_1": [], # [otsikko, sisältö]
            "palvelu_2": [],
            "palvelu_3": [],
            "palaute_1": [], # [palautteen antaja, palaute]
            "palaute_2": [],
            "palaute_3": [],
        }
        
        with open(self.path) as file:
            text = file.read()
            text = text[4:-4]
            vapaa = text.find("vapaa:\n")
            palvelut = text.find("palvelut:\n")
            hero = text.find("hero:\n")
            # Extract data
            sets = [vapaa, palvelut, hero]
            sets.sort()
            sets.append(len(text)+1) # Add an int that's the end of the text
            print(sets)
            cont = text[:sets[1] - 1]
            
            
            kappaleet = [] # [title, content]
            päälause = ""
            tukilause = ""
            
            for i in range(len(sets)-1):
                # print(f"Iteration of set!: {i}")
                # print(f"Section cont set: [{sets[i]} : {sets[i+1]-1}]")
                cont = text[sets[i]:sets[i+1]-1]
                    
                # print(cont)

            
        # Manually setting the values since Reader hasn't been properly implemented yet
        
        data["päälause"] = "Esimerkkiotsikko"
        data["tukilause"] = "Esimerkkilause, Väliaikaista tekstiä. Esimerkkilause, Väliaikaista tekstiä."
        data["yritys"] = "Proverkko Oy on 2021 perustettu, yhden rakennusmestarin konsultointiyritys.<br><br>Yrityksen liiketoimintaidea on työmaapainotteinen, asiantuntijapalveluiden tuottaminen, rakennusalan eri toimijoille. Toiminta keskittyy pääkaupunkiseudulle."
        data["esittely"] = "Minulla on yli 30v kokemusta rakennusalan eri osa-alueilta, ja erittäin laaja asiantuntija- ja urakoitsijaverkosto. Vahvimmat osa-alueeni ovat käytännön toteutuksessa.<br><br>- rakenteiden lujitus<br>- korjausrakentaminen (tunnelit, sillat ja linjasaneeraus)<br>- toimitusjohtajan tehtävät (kokemusta kolmessa eri rakennusyrityksessä)<br>- yritysjärjestelyt (osapuolena viidessä yrityskaupassa)"
        
        data["kappale_1"] = ["Varamestari", "Yllättikö resurssipula? Ota yhteyttä ja kysy ehtisikö Tero Saarinen auttamaan. Saarisella on monipuolinen käytännön kokemus rakentamisen eri osa-alueilta:<br><br>- toimitusjohtaja<br>- työpäällikkö<br>- työmaapäällikkö<br>- vastaava työnjohtaja<br>- työnjohtaja"]
        data["kappale_2"] = ["Kustannusoptimointi", "Rakenteiden, esim. kallioleikkausten lujitustyöt, ovat suhteellisen harvinaisia monelle työnjohtajalle. Tämän takia osaaminen ei ole aina toivotulla tasolla.<br><br>Menetelmät on syytä valita hyvissä ajoin, mutta välillä kallion laatu yllättää kokeneekin tekijän. Tulen mielelläni konsultoimaan työmenetelmissä ja tarvittaessa johdan lujitustöitä"]
        data["kappale_3"] = ["Laadun varmistus työmaalla", "Nykytrendinä on laadun tekeminen ”paperilla”, mutta  valitettavan usein laatu ei valu työmaalle asti.<br>Hyvätkin suunnitelmat ja laadukkaat materiaalit voi pilata huonolla työllä. Kuinka varmistetaan esim. laadukas pulttaus? Takaavatko sertifikaatit ja työvaihesuunnitelmat suunnitellun lopputuloksen?<br>Onko laitteilla ja ainevalinnoilla merkitystä laatuun?"]
        
        data["palvelu_1"] = ["Laadun varmistus", "Esimerkkiteksti. Tämä korvataan oikealla tekstillä myöhemmin"]
        data["palvelu_2"] = ["Varamestari", "Esimerkkiteksti. Tämä korvataan oikealla tekstillä myöhemmin"]
        data["palvelu_3"] = ["Ja muut palvelut", "Esimerkkiteksti. Tämä korvataan oikealla tekstillä myöhemmin"]
        
        data["palaute_1"] = ["- Aatu, ABC Oy", "Esimerkkilause, Väliaikaista tekstiä. Väliaikainen teksti. Tämän tekstin tilalle tulee oikea teksti. "]
        data["palaute_2"] = ["- Eetu, ABC Oy", "Esimerkkilause, Väliaikaista tekstiä. Väliaikainen teksti. Tämän tekstin tilalle tulee oikea teksti. "]
        data["palaute_3"] = ["- Aapo, ABC Oy", "Esimerkkilause, Väliaikaista tekstiä. Väliaikainen teksti. Tämän tekstin tilalle tulee oikea teksti. "]
        
        return data


def build():
    reader = Reader(Path("input/front_page/content.md"))
    output_folder = Path("output/")
    data_read = reader.read()
    
    # Templating
    env = Environment(loader=FileSystemLoader(Path('templates/')))
    index_template = env.get_template('index.html')
    index_html = index_template.render(data=data_read)
    print(index_html)
    
    # Create file and assign it
    
    with open(output_folder / "index.html", "wt", encoding="utf-8") as file:
        result = file.write(index_html)
    
    # Copy the static folder into output/
    copytree(Path('templates/static'), output_folder / "static")
    
    

def main():
    reader = Reader(Path("input/front_page/content.md"))
    md = Markdown(extensions=["meta"])
    # result = reader.read()
    # md.convert(result)
    # print(md.Meta)
    reader.read()


 

if __name__ == "__main__":
    build()