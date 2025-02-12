import os
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, String, or_ , case


app = Flask(__name__) 

# Настройки базы данных (из переменных окружения)
DB_PATH = os.getenv("DATABASE_URL", "sqlite:///coins.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Базовый URL для изображений
PHOTO_BASE_URL = os.getenv("PHOTO_BASE_URL", "https://nreestr.ru/img/all/bpict")


# Определяем модель (таблица coins)
class Coin(db.Model):
    __tablename__ = 'coins'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    weight = db.Column(db.Float)
    year = db.Column(db.Integer)         # Можно использовать тип Date, если требуется
    condition = db.Column(db.String)
    value = db.Column(db.String)
    text = db.Column('text', db.String)   # Имя столбца – text

    def to_dict(self):
        return {
            "number": self.number,
            "weight": self.weight,
            "year": self.year,
            "condition": self.condition,
            "value": self.value,
            "text": self.text
        }

    def __repr__(self):
        return f'<Coin {self.number}>'


#def create_db():
    """
    Если файл coins.db отсутствует, создаём базу и заполняем её данными из DataFrame.
    В реальном приложении данные можно загрузить из CSV или другого источника.
    """
	
    # Загрузка данных из CSV
    #df = pd.read_csv('data/coins.csv')
    #df['year'] = df['year'].str.replace(r'\D', '', regex=True)
    #df.loc[df['year']=='','year']=0
    #df['year']=df['year'].fillna(value=0)

    #if not os.path.exists("instance\\coins.db"):
    #    db.create_all()
        # Заполняем базу данных
    #    for _, row in df.iterrows():
    #        coin = Coin(
    #            number=row['number'],
    #            weight=float(row['weight']),
    #            year=int(row['year']),
    #            condition=row['condition'],
    #            value=row['value'],
    #            text=row['text']
    #        )
    #        db.session.add(coin)
    #    db.session.commit()
    #    print("База данных создана и заполнена данными.")

def apply_filters_and_sort(coins_query, search_query, sort_by, order):
    """Применяет фильтрацию и сортировку к запросу с учетом пользовательского порядка для condition."""
    # Фильтрация: для каждого токена ищем его наличие хотя бы в одном из полей
    if search_query:
        tokens = search_query.split()
        for token in tokens:
            coins_query = coins_query.filter(
                or_(
                    Coin.number.ilike(f'%{token}%'),
                    cast(Coin.weight, String).ilike(f'%{token}%'),
                    cast(Coin.year, String).ilike(f'%{token}%'),
                    Coin.condition.ilike(f'%{token}%'),
                    Coin.value.ilike(f'%{token}%'),
                    Coin.text.ilike(f'%{token}%')
                )
            )

    allowed_sort = ['number', 'year', 'condition']
    if sort_by in allowed_sort:
        if sort_by == 'condition':
            # Определяем пользовательский порядок сортировки
            condition_order = case(
                    (Coin.condition == 'G det.', 0),
                    (Coin.condition == 'G2', 1),
                    (Coin.condition == 'G4', 2),
                    (Coin.condition == 'G6', 3),
                    (Coin.condition == 'VG det.', 4),
		    (Coin.condition == 'VG8', 5),
                    (Coin.condition == 'VG10', 6),
                    (Coin.condition == 'F det.', 7),
                    (Coin.condition == 'F12', 8),
                    (Coin.condition == 'F15', 9),
		    (Coin.condition == 'F15BN', 10),
                    (Coin.condition == 'VF det.', 11),
                    (Coin.condition == 'VF20', 12),
                    (Coin.condition == 'VF20BN', 13),
                    (Coin.condition == 'VF25', 14),
		    (Coin.condition == 'VF25BN', 15),
		    (Coin.condition == 'VF30', 16),
		    (Coin.condition == 'VF30BN', 17),
                    (Coin.condition == 'VF35', 18),
		    (Coin.condition == 'VF35BN', 19),
                    (Coin.condition == 'XF det.', 20),
                    (Coin.condition == 'XF40', 21),
		    (Coin.condition == 'XF40BN', 22),
                    (Coin.condition == 'XF45', 23),
		    (Coin.condition == 'XF45BN', 24),
		    (Coin.condition == 'AU det.', 25),
                    (Coin.condition == 'AU50', 26),
		    (Coin.condition == 'AU50BN', 27),
		    (Coin.condition == 'AU53', 28),
		    (Coin.condition == 'AU53BN', 29),
		    (Coin.condition == 'AU55', 30),
		    (Coin.condition == 'AU55BN', 31),
	      	    (Coin.condition == 'AU55RB', 32),
		    (Coin.condition == 'AU58', 33),
		    (Coin.condition == 'AU58BN', 34),
		    (Coin.condition == 'AU58RB', 35),
		    (Coin.condition == 'PL58', 36),
		    (Coin.condition == 'PF58', 37),
		    (Coin.condition == 'UNC det.', 38),
		    (Coin.condition == 'PF det.', 39),
		    (Coin.condition == 'PL det.', 40),
                    (Coin.condition == 'MS60', 41),
                    (Coin.condition == 'MS60BN', 42),
                    (Coin.condition == 'MS60RB', 43),
		    (Coin.condition == 'MS60RD', 44),
		    (Coin.condition == 'PL60', 45),
		    (Coin.condition == 'PF60', 46),
		    (Coin.condition == 'MS61', 47),
                    (Coin.condition == 'MS61BN', 48),
                    (Coin.condition == 'MS61RB', 49),
		    (Coin.condition == 'MS61RD', 50),
		    (Coin.condition == 'PL61', 51),
		    (Coin.condition == 'PF61', 52),
		    (Coin.condition == 'MS62', 53),
                    (Coin.condition == 'MS62BN', 54),
                    (Coin.condition == 'MS62RB', 55),
		    (Coin.condition == 'MS62RD', 56),
		    (Coin.condition == 'PL62', 57),
		    (Coin.condition == 'PF62', 58),
		    (Coin.condition == 'MS63', 59),
                    (Coin.condition == 'MS63BN', 60),
                    (Coin.condition == 'MS63RB', 61),
		    (Coin.condition == 'MS63RD', 62),
		    (Coin.condition == 'PL63', 63),
		    (Coin.condition == 'PF63', 64),
		    (Coin.condition == 'MS64', 65),
                    (Coin.condition == 'MS64BN', 66),
                    (Coin.condition == 'MS64RB', 67),
		    (Coin.condition == 'MS64RD', 68),
		    (Coin.condition == 'PL64', 69),
		    (Coin.condition == 'PF64', 70),
		    (Coin.condition == 'MS65', 71),
                    (Coin.condition == 'MS65BN', 72),
                    (Coin.condition == 'MS65RB', 73),
		    (Coin.condition == 'MS65RD', 74),
		    (Coin.condition == 'PL65', 75),
		    (Coin.condition == 'PF65', 76),
		    (Coin.condition == 'MS66', 77),
                    (Coin.condition == 'MS66BN', 78),
                    (Coin.condition == 'MS66RB', 79),
		    (Coin.condition == 'MS66RD', 80),
		    (Coin.condition == 'PL66', 81),
		    (Coin.condition == 'PF66', 82),
		    (Coin.condition == 'MS67', 83),
                    (Coin.condition == 'MS67BN', 84),
                    (Coin.condition == 'MS67RB', 85),
		    (Coin.condition == 'MS67RD', 86),
		    (Coin.condition == 'PL67', 87),
		    (Coin.condition == 'PF67', 88),
		    (Coin.condition == 'MS68', 89),
                    (Coin.condition == 'MS68BN', 90),
                    (Coin.condition == 'MS68RB', 91),
		    (Coin.condition == 'MS68RD', 92),
		    (Coin.condition == 'PL68', 93),
		    (Coin.condition == 'PF68', 94),
		    (Coin.condition == 'MS69', 95),
                    (Coin.condition == 'MS69BN', 96),
                    (Coin.condition == 'MS69RB', 97),
		    (Coin.condition == 'MS69RD', 98),
		    (Coin.condition == 'PL69', 99),
		    (Coin.condition == 'PF69', 100),
		    (Coin.condition == 'MS70', 101),
                    (Coin.condition == 'MS70BN', 102),
                    (Coin.condition == 'MS70RB', 103),
		    (Coin.condition == 'MS70RD', 104),
		    (Coin.condition == 'PL70', 105),
		    (Coin.condition == 'PF70', 106),
                    else_=-1
            )
            if order == 'asc':
                coins_query = coins_query.order_by(condition_order.asc())
            else:
                coins_query = coins_query.order_by(condition_order.desc())
        else:
            sort_column = getattr(Coin, sort_by)
            if order == 'asc':
                coins_query = coins_query.order_by(sort_column.asc())
            else:
                coins_query = coins_query.order_by(sort_column.desc())
    return coins_query


@app.route('/')
def index():
    search_query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort_by', '')
    order = request.args.get('order', 'asc')

    coins_query = Coin.query
    coins_query = apply_filters_and_sort(coins_query, search_query, sort_by, order)

    PER_PAGE = 5  # Количество записей на одну порцию
    coins = coins_query.offset(0).limit(PER_PAGE).all()
    total_count = coins_query.count()  # Общее число записей, подходящих под фильтры

    return render_template('index.html',
                           coins=coins,
                           q=search_query,
                           sort_by=sort_by,
                           order=order,
                           total_count=total_count)


# AJAX-эндпоинт для подгрузки следующей порции данных
@app.route('/get_coins')
def get_coins():
    search_query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort_by', '')
    order = request.args.get('order', 'asc')
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    coins_query = Coin.query
    coins_query = apply_filters_and_sort(coins_query, search_query, sort_by, order)

    PER_PAGE = 5
    coins = coins_query.offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()
    coins_list = [coin.to_dict() for coin in coins]
    return jsonify(coins=coins_list)




@app.route('/photos/<filename>')
def photos(filename):
    
    # Изображения на сайте ННР
    remote_url = f"{PHOTO_BASE_URL}/{filename}"
    return redirect(remote_url)

if __name__ == "__main__":
    #with app.app_context():
    #    create_db()
    app.run(host="0.0.0.0", port=5000, debug=False)