import airportcodes as air
import pandas as pd
import string

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
letras = list(string.ascii_lowercase)
pags = [6, 7, 6, 4, 3, 3, 4, 4, 3, 3, 6, 5, 7, 4, 4, 6, 2, 4, 7, 6, 3, 2, 3, 2, 6, 2]
pags = list(map(lambda x: x + 1, pags))
df = pd.DataFrame()
for idx, let in enumerate(letras):
    for pag in range(1,pags[idx]):
        url = "https://www.world-airport-codes.com/alphabetical/airport-code/"+str(let)+".html?page="+str(pag)
        result = air.getAIRPORTs(url,headers=headers)
        df0 = pd.DataFrame(result, columns = ['Airport','Type','City','Country','IATA', 'ICAO', 'FAA'])
        df = df.append(df0)
        print("Letra:", str(let), "Pagina:", str(pag))
df.to_csv("airpot_codes.csv",encoding='utf-8-sig')