from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import *
from collections import OrderedDict
from data import db_session
from data.shelters import Shelters
from data.users import Users
from data.cats import Cats
from api.v1 import cats_api
from api.v1 import shelters_api
from api.v1 import users_api
from api.v2 import cats_resource
from api.v2 import shelters_resource
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash
from forms.login import LoginForm
from forms.cats import CatForm
from forms.register import RegisterForm
from forms.shelter import ShelterForm
from requests import get, put, post, delete

app = Flask(__name__)
app.config['SECRET_KEY'] = 'its_not_a_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    user = db_session.create_session().query(Users).get(user_id)
    return user


# Стартовая страница
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = db_session.create_session().query(Users).filter(Users.login == form.login.data).first()

            if not user:
                flash('Пользователь с таким логином не найден', 'danger')
            elif not check_password_hash(user.hashed_password, form.password.data):
                flash('Неверный пароль', 'danger')
            else:
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно вошли в систему', 'success')
                return redirect(url_for('main_page'))

        except Exception as e:
            flash('Произошла ошибка при авторизации', 'danger')
            app.logger.error(f'Login error: {str(e)}')

    return render_template('login.html', form=form)


# Основная страница авторизирированного пользователя
@app.route('/main_page')
@login_required
def main_page():
    return render_template('main_page.html')


# Панель администратора (утверждение приютов)
@app.route('/view-shelter-applications', methods=['GET', 'POST'])
@login_required
def view_shelter_applications():
    if current_user.login != 'admin':
        abort(403)
    shelters = get('http://localhost:8080/api/v2/shelters').json()['shelters']
    return render_template('view_shelter_applications.html', shelters=shelters)


# Добавление приюта
@app.route('/add_shelter/<int:shelter_id>', methods=['GET', 'POST', 'PUT'])
def add_shelter(shelter_id):
    put(f'http://127.0.0.1:8080/api/shelters/{shelter_id}', json={'validated': 1}).json()
    return redirect('/view-shelter-applications')


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают', 'danger')
        elif db_session.create_session().query(Users).filter(Users.email == form.email.data).first():
            flash('Пользователь с такой почтой уже существует', 'danger')
        elif db_session.create_session().query(Users).filter(Users.login == form.login.data).first():
            flash('Пользователь с таким логином уже существует', 'danger')
        else:
            post('http://127.0.0.1:8080/api/users', json={'login': form.login.data,
                                                          'email': form.email.data,
                                                          'password': form.password.data}).json()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Страница для просмотра собственного приюта
@app.route('/my_shelter')
def my_shelter():
    # Если пользователь помечен как приют - отображается информация об его приюте
    if current_user.is_shelter:
        my_shelter = db_session.create_session().query(Shelters).filter(Shelters.user_id == current_user.id).first()
        my_shelter = get(f'http://127.0.0.1:8080/api/v2/shelters/{my_shelter.id}').json()['shelters']
        return render_template('my_shelter.html', is_shelter=1, my_shelter=my_shelter)
    # Если пользователь не помечен в системе как приют, но в системе есть заявка на регистрацию приюта от него - покажется информация, что приют подтверждается
    if (not current_user.is_shelter) and db_session.create_session().query(Shelters).filter(
            Shelters.user_id == current_user.id).first():
        return render_template('my_shelter.html', is_shelter=0, my_shelter=False)
    # Иначе же окно для регистрации приюта
    else:
        return redirect(url_for('register_shelter'))


# Добавление кота
@app.route('/register_cat', methods=['GET', 'POST'])
def register_cat():
    form = CatForm()
    shelter = db_session.create_session().query(Shelters).filter(Shelters.user_id == current_user.id).first()
    if form.validate_on_submit():
        post('http://127.0.0.1:8080/api/cats', json={'name': form.name.data,
                                                     'age': form.age.data,
                                                     'breed': form.breed.data,
                                                     'features': form.features.data, 'shelter_id': shelter.id}).json()
        flash('Котик добавлен!', 'success')
        return redirect(url_for('register_cat'))
    return render_template('register_cat.html', form=form)


# Удаление кота
@app.route('/delete_cat/<int:cat_id>', methods=['GET', 'POST'])
def delete_cat(cat_id):
    delete(f'http://127.0.0.1:8080/api/cats/{cat_id}')
    return redirect('/view_our_cats')


# Регистрация приюта
@app.route('/register_shelter', methods=['GET', 'POST'])
def register_shelter():
    form = ShelterForm()
    if form.validate_on_submit():
        if db_session.create_session().query(Shelters).filter(Shelters.name == form.name.data).first():
            flash('Приют с таким именем существует', 'danger')
        elif db_session.create_session().query(Shelters).filter(Shelters.phone == form.phone.data).first():
            flash('Такой номер уже используется', 'danger')
        else:
            post('http://127.0.0.1:8080/api/shelters', json={'name': form.name.data,
                                                             'phone': form.phone.data,
                                                             'address': form.address.data,
                                                             'validated': 0, 'user_id': current_user.id}).json()
            flash('Ожидайте подвтерждения.', 'success')
            return redirect(url_for('my_shelter'))
    return render_template('register_shelter.html', form=form)


# Просмотр котов всех приютов
@app.route('/view_cats')
def view_cats():
    cats = get('http://127.0.0.1:8080/api/cats').json()['cats']
    return render_template('view_cats.html', cats=cats)


# Просмотр котов приюта текущего пользователя
@app.route('/view_our_cats')
def view_our_cats():
    my_shelter = db_session.create_session().query(Shelters).filter(Shelters.user_id == current_user.id).first()
    cats = get(f'http://127.0.0.1:8080/api/shelters/{my_shelter.id}').json()['cats']
    return render_template('view_our_cats.html', cats=cats)


# Просмотр всех приютов
@app.route('/view_shelters')
def view_shelters():
    shelters = get('http://127.0.0.1:8080/api/shelters').json()['shelters']
    return render_template('view_shelters.html', shelters=shelters)


# Выгрузка пользователя
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Обработчик ошибки 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/we_are_cats.db")
    app.register_blueprint(cats_api.blueprint)
    app.register_blueprint(shelters_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(shelters_resource.SheltersListResource, '/api/v2/shelters')
    api.add_resource(shelters_resource.SheltersResource, '/api/v2/shelters/<int:shelters_id>')
    api.add_resource(cats_resource.CatsListResource, '/api/v2/cats')
    api.add_resource(cats_resource.CatsResource, '/api/v2/cats/<int:cats_id>')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
