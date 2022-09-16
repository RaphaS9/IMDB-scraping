from bs4 import BeautifulSoup
import requests
import openpyxl

#criando uma tabela para armazenar os dados
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Top Rated Movies'
sheet.append(["Movie Rank", "Movie Name", "Year of Release", "IMDB Rating"])

try:
    #definindo a fonte para nosso "raspamento" de dados
    source = requests.get("https://www.imdb.com/chart/top/")
    source.raise_for_status()
    soup = BeautifulSoup(source.text, "html.parser")

    #definindo quais elemento devo procurar na página
    movies = soup.find("tbody", class_="lister-list").find_all("tr")
    for movie in movies:
        title = movie.find("td", class_="titleColumn").a.text
        rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]
        year = movie.find("td", class_="titleColumn").span.text.strip("()")
        rating = movie.find("td", class_="ratingColumn imdbRating").strong.text
        sheet.append([rank, title, year, rating])

except Exception as e:
    print(e)

#salva um arquivo xlsx no local em que o programa é rodado
excel.save("IMDB Movie Ratings.xlsx")