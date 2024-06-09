import json
import os

# Lista de sites populares no Brasil, categorizados por letra
sites_populares = {
    'A': ["amazon.com.br", "americanas.com.br", "apple.com", "abril.com.br", "aliexpress.com",
          "atarde.uol.com.br", "academia.edu", "abril.com", "archlinux.org", "asus.com"],
    'B': ["buscape.com.br", "blogspot.com", "bbb.globo.com", "bradesco.com.br", "bing.com",
          "bol.uol.com.br", "bing.com.br", "bb.com.br", "buzzfeed.com", "bbc.com"],
    'C': ["correios.com.br", "catho.com.br", "clicrbs.com.br", "conjur.com.br", "conta.uol.com.br",
          "canva.com", "compras.net.br", "conta.azul.com.br", "cisco.com", "casa.uol.com.br"],
    'D': ["dicio.com.br", "digikala.com", "dropshipping.com.br", "dell.com", "diariodonordeste.com.br",
          "download.com", "duckduckgo.com", "discord.com", "decolar.com", "dictionary.com"],
    'E': ["ebay.com", "elpaís.com", "estadão.com.br", "exame.com", "espn.com.br",
          "elpais.com.br", "evernote.com", "economia.uol.com.br", "extra.globo.com", "em.com.br"],
    'F': ["facebook.com", "folha.uol.com.br", "fiescnet.com.br", "fifa.com", "foursquare.com",
          "fiverr.com", "ford.com.br", "fnac.com.br", "foxsports.com.br", "fifa.com.br"],
    'G': ["globo.com", "g1.globo.com", "google.com", "github.com", "gazzetta.it",
          "google.com.br", "giphy.com", "gol.com.br", "globo.com.br", "gq.globo.com"],
    'H': ["hotmail.com", "huffpostbrasil.com", "hbr.org", "hp.com", "huanqiu.com",
          "hoteis.com", "hootsuite.com", "hsbc.com.br", "hostgator.com.br", "hulu.com"],
    'I': ["ig.com.br", "indeed.com.br", "instagram.com", "imdb.com", "intuit.com",
          "ibm.com", "icloud.com", "iherb.com", "ikea.com", "imovelweb.com.br"],
    'J': ["jornaldacidadeonline.com.br", "jornalextra.globo.com", "jusbrasil.com.br", "jornalggn.com.br", "jobatus.com.br",
          "jovempan.uol.com.br", "jus.com.br", "jejumintermitente.com.br", "jornalopcao.com.br", "jornalcorreiodopovo.com.br"],
    'K': ["kantar.com", "kasikornbank.com", "kaspersky.com", "kinghost.com.br", "kiwify.com.br",
          "klook.com", "kabum.com.br", "korreio.com.br", "kotaku.com.br", "kboing.com.br"],
    'L': ["linkedin.com", "live.com", "letras.mus.br", "lopes.com.br", "loterias.caixa.gov.br",
          "linkedin.com.br", "live.com.br", "lefigaro.fr", "libertymutual.com", "lifestyle.com"],
    'M': ["mercadolivre.com.br", "magazineluiza.com.br", "mapfre.com.br", "mundodomarketing.com.br", "microsoft.com",
          "megacurioso.com.br", "mlb.com", "myspace.com", "mtv.com.br", "medium.com"],
    'N': ["netflix.com", "nasa.gov", "nature.com", "nbcnews.com", "natura.com.br",
          "nfl.com", "nexon.com", "nike.com", "npr.org", "nytimes.com"],
    'O': ["olx.com.br", "outlook.com", "onet.pl", "orange.fr", "office.com",
          "opera.com", "oreilly.com", "openai.com", "opentable.com", "overstock.com"],
    'P': ["pagseguro.uol.com.br", "paypal.com", "petrobras.com.br", "pinterest.com", "pr.gov.br",
          "panasonic.com", "periscope.tv", "pontofrio.com.br", "projeto10envolvimento.com.br", "python.org"],
    'Q': ["quora.com", "quiksilver.com", "qualcomm.com", "quizlet.com", "quintoandar.com.br",
          "qualtrics.com", "qvc.com", "quickbooks.intuit.com", "quest.com", "qubit.com"],
    'R': ["rihappy.com.br", "rackspace.com", "reddit.com", "renner.com.br", "riotgames.com",
          "rocketlawyer.com", "royalmail.com", "r7.com", "redhat.com", "reclameaqui.com.br"],
    'S': ["submarino.com.br", "santander.com.br", "samsung.com.br", "saude.gov.br", "safra.com.br",
          "spotify.com", "stackoverflow.com", "slideshare.net", "skyscanner.com.br", "sp.senai.br"],
    'T': ["terra.com.br", "techtudo.com.br", "twitter.com", "telegram.org", "target.com",
          "twitch.tv", "tnt.com", "tesla.com", "tumblr.com", "trivago.com.br"],
    'U': ["uol.com.br", "universia.com.br", "uniceub.br", "und.com", "uber.com",
          "usnews.com", "udemy.com", "univision.com", "upwork.com", "usajobs.gov"],
    'V': ["vivo.com.br", "vimeo.com", "verizon.com", "vice.com", "variety.com",
          "vodafone.com", "visa.com.br", "vmware.com", "volkswagen.com.br", "vice.com.br"],
    'W': ["whatsapp.com", "walmart.com.br", "wp.com", "wikipedia.org", "wellsfargo.com",
          "weather.com", "weibo.com", "webmd.com", "wired.com", "whoscall.com"],
    'X': ["xbox.com", "xerox.com", "xfinity.com", "xiaomi.com", "xataka.com",
          "xaprb.com", "xilam.com", "xang.com", "xcaret.com", "xeneta.com"],
    'Y': ["youtube.com", "yahoo.com", "yahoo.com.br", "yelp.com", "yahoo.co.jp",
          "yn.com", "yellowpages.com", "yandex.ru", "yammer.com", "yahoo.net"],
    'Z': ["zoom.com.br", "zara.com", "zendesk.com", "zoho.com", "zapimoveis.com.br",
          "zomato.com", "zerply.com", "zillow.com", "zynga.com", "zazzle.com"]
}

def criar_arquivo_particao(letra, sites):
    nome_arquivo = f'particoes/particao_{letra}.json'
    dados = {site: f'192.0.2.{i+1}' for i, site in enumerate(sites)}
    with open(nome_arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

def main():
    os.makedirs('particoes', exist_ok=True)
    
    for letra, sites in sites_populares.items():
        criar_arquivo_particao(letra, sites)
    print("Arquivos de partição criados com sucesso.")

if __name__ == "__main__":
    main()
