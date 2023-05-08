import hub_scrapper
from flask import Flask, request
from dotenv import load_dotenv
import traceback
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hub Scrapper API'


@app.route('/hub_scrapper/get_scrapped_results')
def get_scrapped_results():

    try:
        query = request.args.get('q')
        home_page = request.args.get('home_page', default='false')
        if home_page.lower() == 'true':
            home_page = True
        elif home_page.lower() == 'false':
            home_page = False
        else:
            home_page = False

        data = hub_scrapper.get_scrape_results(query, home_page)

        return {'results': data}, 200
    except Exception as ex:
        traceback.print_exc()
        return {'message': 'Bad request', 'Error': traceback.format_exc()}, 400


if __name__ == '__main__':
    app.run()
