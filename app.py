from flask import Flask, render_template, request, redirect
from forms.user_form import UserForm
from forms.neural_form import NeuronForm
from forms.edit_user_form import EditUserForm
from forms.parameter_form import ParameterForm
from forms.edit_parameter_form import EditParameterForm
from forms.edit_class_form import EditClassForm
from forms.class_form import ClassForm
from forms.method_form import MethodForm
from forms.edit_method_form import EditMethodForm
from forms.hastag_form import HastagForm
import uuid
import json
import plotly
from sqlalchemy.sql import func
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, FunctionTransformer, MaxAbsScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import random as rnd
from math import fabs


app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vkntpqzmequvzy:d0cfa0ace686dbc41dd553bd05555159211f45db3571ab404cac94be19047fa8@ec2-174-129-254-231.compute-1.amazonaws.com:5432/dbm1daba6oq9rk'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:fastdagger@localhost/milev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OrmUser(db.Model):
    __tablename__ = 'user'
    user_email = db.Column(db.String(45), primary_key=True)
    user_name = db.Column(db.String(25), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_university = db.Column(db.String(25), nullable=False, unique=True)

    class_ = db.relationship('OrmClass')

class OrmClass(db.Model):
    __tablename__ = 'class'
    class_name = db.Column(db.String(30), primary_key=True)
    methods_quantity = db.Column(db.Integer, nullable=False)
    class_description = db.Column(db.String(50), nullable=True)
    user_email = db.Column(db.String(45), db.ForeignKey('user.user_email'), nullable=False)

    method_ = db.relationship('OrmMethod')


class OrmMethod(db.Model):
    __tablename__ = 'method'
    method_name = db.Column(db.String(30), primary_key=True)
    method_description = db.Column(db.String(50), nullable=False)
    output_type = db.Column(db.String(50), nullable=False)
    memory_size = db.Column(db.String(4), nullable=False)
    class_name = db.Column(db.String(30), db.ForeignKey('class.class_name'), nullable=False)

    parameter_ = db.relationship('OrmParameter')

class OrmParameter(db.Model):
    __tablename__ = 'parameter'

    parameter_name = db.Column(db.String(30), primary_key=True)
    parameter_description = db.Column(db.String(50), nullable=False)
    parameter_type = db.Column(db.String(25), nullable=False)
    method_name = db.Column(db.String(30), db.ForeignKey('method.method_name'), nullable=False)

db.drop_all()


db.create_all()

User1 = OrmUser(
    user_email='Sergei@gmail.com',
    user_name ='Сергей',
    user_age=20,
    user_university='КВ12345678'
)

User2 = OrmUser(
    user_email='Igor@gmail.com',
    user_name ='Игорь',
    user_age=25,
    user_university='КТ12345678'
)
User3 = OrmUser(
    user_email='Petr@gmail.com',
    user_name ='Петр',
    user_age=16,
    user_university='КЕ12345678'
)
User4 = OrmUser(
    user_email='Gorg@gmail.com',
    user_name ='Георгий',
    user_age=20,
    user_university='КП12345678'
)


Class1 = OrmClass(
    class_name='Numeric operations',
    methods_quantity=3,
    class_description='Adding, substracting, multiplying numbers',
    user_email='Gorg@gmail.com'
)

Class2 = OrmClass(
    class_name='Numeric operations advanced',
    methods_quantity=2,
    class_description='Powering, rooting numbers',
    user_email='Gorg@gmail.com'
)

Class3 = OrmClass(
    class_name='String operations',
    methods_quantity=2,
    class_description='Basic actions with strings',
    user_email='Petr@gmail.com'
)

Class4 = OrmClass(
    class_name='String operations advanced',
    methods_quantity=2,
    class_description='Complicated actions with strings',
    user_email='Sergei@gmail.com'
)

Class5 = OrmClass(
    class_name='String operations advanced',
    methods_quantity=2,
    class_description='Complicated actions with strings',
    user_email='Igor@gmail.com'
)

Class6 = OrmClass(
    class_name='String operations advanced',
    methods_quantity=2,
    class_description='Complicated actions with strings',
    user_email='Sergei@gmail.com'
)



Method1 = OrmMethod(
    method_name='Adding numbers',
    method_description='Adding two numbers',
    output_type='Numeric',
    memory_size='32',
    class_name='Numeric operations'
)

Method2 = OrmMethod(
    method_name='Number exponentiation',
    method_description='Raising first number to the power of second one',
    output_type='Numeric',
    memory_size='64',
    class_name='Numeric operations advanced'
)

Method3 = OrmMethod(
    method_name='Adding strings',
    method_description='Adding two strings',
    output_type='String',
    memory_size='128',
    class_name='String operations'
)

Method4 = OrmMethod(
    method_name='Finding string',
    method_description='Defies, if one string contains another',
    output_type='String',
    memory_size='256',
    class_name='String operations advanced'
)

Method5 = OrmMethod(
    method_name='Substracting numbers',
    method_description='Substracting second number from the first one',
    output_type='Numeric',
    memory_size='256',
    class_name='String operations advanced'
)


Method6 = OrmMethod(
    method_name='1 more then 2',
    method_description='Defies, if first number bigger than second one',
    output_type='Boolean',
    memory_size='32',
    class_name='String operations advanced'
)
Parameter1 = OrmParameter(
    parameter_name='Parameter 1',
    parameter_type='integer',
    parameter_description='First number in adding',
    method_name='Adding numbers'
)

Parameter2 = OrmParameter(
    parameter_name='Parameter 2',
    parameter_type='string',
    parameter_description='Second number in adding ',
    method_name='Adding numbers'
)

Parameter3 = OrmParameter(
    parameter_name='Parameter 3',
    parameter_type='float',
    parameter_description='First string in finding',
    method_name='Finding string'
)

Parameter4 = OrmParameter(
    parameter_name='Parameter 4',
    parameter_type='float',
    parameter_description='First parameter for exponentiation',
    method_name='Number exponentiation'
)

Parameter5 = OrmParameter(
    parameter_name='Parameter 5',
    parameter_type='float',
    parameter_description='Second parameter for exponentiation',
    method_name='Number exponentiation'
)

Parameter6 = OrmParameter(
    parameter_name='Parameter 6',
    parameter_type='string',
    parameter_description='Second string in finding',
    method_name='Finding string'
)
db.session.add_all([

    User1,
    User2,
    User3,
    User4,
    Class1,
    Class2,
    Class3,
    Class4,
    Method1,
    Method2,
    Method3,
    Method4,
    Method5,
    Method6,
    Parameter1,
    Parameter2,
    Parameter3,
    Parameter4,
    Parameter5,
    Parameter6
])

db.session.commit()

@app.route('/parameters')
def parameters():
    res = db.session.query(OrmParameter).all()

    return render_template('parameters_table.html', parameters=res)


@app.route('/new_parameter/<string:method_name>', methods=['GET', 'POST'])
def new_parameter(method_name):
    form = ParameterForm()

    f_id_prep = db.session.query(OrmMethod.method_name).filter(OrmMethod.method_name == method_name).one()
    f_id = f_id_prep[0]

    if request.method == 'POST':
        if form.validate():
            try:
                new_parameter = OrmParameter(
                    parameter_name=form.parameter_name.data,
                    parameter_description=form.parameter_description.data,
                    parameter_type=form.parameter_type.data,
                    method_name=f_id
                )
                db.session.add(new_parameter)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('parameter_form.html', form=form)
        else:
            return render_template('parameter_form.html', form=form)
    elif request.method == 'GET':
        return render_template('parameter_form.html', form=form)


@app.route('/edit_parameter/<string:parameter_name>', methods=['GET', 'POST'])
def edit_parameter(parameter_name):
    form = EditParameterForm()
    result = db.session.query(OrmParameter).filter(OrmParameter.parameter_name == parameter_name).one()

    if request.method == 'GET':

        form.parameter_description.data = result.parameter_description
        form.parameter_type.data = result.parameter_type

        return render_template('edit_parameter.html', form=form, form_name='edit parameter')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.parameter_description = form.parameter_description.data
                result.parameter_type = form.parameter_type.data

                db.session.commit()
                return redirect('/parameters')
            except:
                return render_template('edit_parameter.html', form=form)
        else:
            return render_template('edit_parameter.html', form=form)


@app.route('/delete_parameter/<string:parameter_name>', methods=['GET', 'POST'])
def delete_parameter(parameter_name):
    result = db.session.query(OrmParameter).filter(OrmParameter.parameter_name == parameter_name).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/users')
def users():
    res = db.session.query(OrmUser).all()

    return render_template('users_table.html', users=res)



@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()


    if request.method == 'POST':
        if form.validate():
            try:
                new_user = OrmUser(
                    user_email=form.user_email.data,
                    user_name=form.user_name.data,
                    user_age=form.user_age.data,
                    user_university=form.user_university.data
                )
                db.session.add(new_user)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('user_form.html', form=form)
        else:
            return render_template('user_form.html', form=form)
    elif request.method == 'GET':
        return render_template('user_form.html', form=form)


@app.route('/user_edit/<string:user_email>', methods=['GET', 'POST'])
def edit_user(user_email):
    form = EditUserForm()
    result = db.session.query(OrmUser).filter(OrmUser.user_email == user_email).one()

    if request.method == 'GET':

        form.user_name.data = result.user_name
        form.user_age.data = result.user_age
        form.user_university.data = result.user_university

        return render_template('edit_user.html', form=form, form_name='edit user')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.user_name = form.user_name.data
                result.user_age = form.user_age.data
                result.user_university = form.user_university.data

                db.session.commit()
                return redirect('/users')
            except:
                return render_template('edit_user.html', form=form)
        else:
            return render_template('edit_user.html', form=form)


@app.route('/delete_user/<string:user_email>', methods=['GET', 'POST'])
def delete_user(user_email):
    result = db.session.query(OrmUser).filter(OrmUser.user_email == user_email).one()

    classes_rows = db.session.query(OrmClass).filter(OrmClass.user_email == user_email).all()
    classes_ids = db.session.query(OrmClass.class_name).filter(OrmClass.user_email == user_email).all()


    m_id = []
    for id in classes_ids:
        methods = db.session.query(OrmMethod.method_name).filter(OrmMethod.class_name == id).all()
        for met_name in methods:
            m_id.append(met_name)


    for id in m_id:
        params = db.session.query(OrmParameter).filter(OrmParameter.method_name == id).all()
        for par in params:
            db.session.delete(par)

        met_del = db.session.query(OrmMethod).filter(OrmMethod.method_name == id).one()
        db.session.delete(met_del)
        db.session.commit()

    for row in classes_rows:
        db.session.delete(row)
        db.session.commit()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


@app.route('/class')
def classes():
    res = db.session.query(OrmClass).all()

    return render_template('class_table.html', classes=res)

@app.route('/new_class/<string:user_email>', methods=['GET', 'POST'])
def new_class(user_email):
    form = ClassForm()

    u_id_prep = db.session.query(OrmUser.user_email).filter(OrmUser.user_email == user_email).one()
    u_id = u_id_prep[0]

    if request.method == 'POST':
        if form.validate():
            try:
                new_class = OrmClass(
                    class_name=form.class_name.data,
                    methods_quantity=form.methods_quantity.data,
                    class_description=form.class_description.data,
                    user_email=u_id
                )
                db.session.add(new_class)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('class_form.html', form=form)
        else:
            return render_template('class_form.html', form=form)
    elif request.method == 'GET':
        return render_template('class_form.html', form=form)

@app.route('/edit_class/<string:class_name>', methods=['GET', 'POST'])
def edit_class(class_name):
    form = EditClassForm()
    result = db.session.query(OrmClass).filter(OrmClass.class_name == class_name).one()

    if request.method == 'GET':

        form.methods_quantity.data = result.methods_quantity
        form.class_description.data = result.class_description

        return render_template('edit_class.html', form=form, form_name='edit class')
    elif request.method == 'POST':

        if form.validate():
            try:
                result.methods_quantity = form.methods_quantity.data
                result.class_description = form.class_description.data

                db.session.commit()
                return redirect('/class')
            except:
                return render_template('edit_class.html', form=form)
        else:
            return render_template('edit_class.html', form=form)



@app.route('/delete_class/<string:class_name>', methods=['GET', 'POST'])
def delete_class(class_name):
    result = db.session.query(OrmClass).filter(OrmClass.class_name == class_name).one()
    method_rows = db.session.query(OrmMethod).filter(OrmMethod.class_name == class_name).all()
    method_ids = db.session.query(OrmMethod.method_name).filter(OrmMethod.class_name == class_name).all()

    med_ids = []
    for class_name in method_ids:
        med_ids.append(class_name[0])

    for method_name in med_ids:
        parameters = db.session.query(OrmParameter).filter(OrmParameter.method_name == method_name).all()
        for row in parameters:
            db.session.delete(row)

    for row in method_rows:
        db.session.delete(row)

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


# remedy
@app.route('/methods')
def methods():
    res = db.session.query(OrmMethod).all()

    return render_template('methods_table.html', methods=res)


@app.route('/new_method/<string:class_name>', methods=['GET', 'POST'])
def new_method(class_name):
    form = MethodForm()

    f_id_prep = db.session.query(OrmClass.class_name).filter(OrmClass.class_name == class_name).one()
    f_id = f_id_prep[0]

    if request.method == 'POST':
        if form.validate():
            try:
                new_method = OrmMethod(
                    method_name=form.method_name.data,
                    method_description=form.method_description.data,
                    output_type=form.output_type.data,
                    memory_size=form.memory_size.data,
                    class_name=f_id
                )
                db.session.add(new_method)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('method_form.html', form=form)
        else:
            return render_template('method_form.html', form=form)
    elif request.method == 'GET':
        return render_template('method_form.html', form=form)


@app.route('/edit_method/<string:method_name>', methods=['GET', 'POST'])
def edit_method(method_name):
    form = EditMethodForm()
    result = db.session.query(OrmMethod).filter(OrmMethod.method_name == method_name).one()

    if request.method == 'GET':

        form.method_description.data = result.method_description
        form.output_type.data = result.output_type
        form.memory_size.data = result.memory_size

        return render_template('edit_method.html', form=form, form_name='edit method')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.method_description = form.method_description.data
                result.output_type = form.output_type.data
                result.memory_size = form.memory_size.data
                db.session.commit()
                return redirect('/methods')
            except:
                return render_template('edit_method.html', form=form)
        else:
            return render_template('edit_method.html', form=form)


@app.route('/delete_method/<string:method_name>', methods=['GET', 'POST'])
def delete_method(method_name):
    result = db.session.query(OrmMethod).filter(OrmMethod.method_name == method_name).one()
    parameter_rows = db.session.query(OrmParameter).filter(OrmParameter.method_name == method_name).all()

    for row in parameter_rows:
        db.session.delete(row)
    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


@app.route('/NeuralForm', methods=['GET', 'POST'])
def NeuralForm():
    form = NeuronForm()

    #Sample = db.session.query(ormUsers).join(ormLesson)

    # Sample = db.session.query(ormUsers).join(ormLesson).filter(ormLesson.lesson_number == 4)
    # for row in Sample:
    #     for inv in row.invoices:
    #         print(row.id, row.name, inv.invno, inv.amount)

    Sample = db.session.query(OrmMethod.output_type,OrmMethod.memory_size,OrmParameter.parameter_type).all()
    X = []
    y = []
    for i in Sample:
        X.append([i.output_type, i.memory_size])
        y.append(i.parameter_type)

    Coder1 = ColumnTransformer(transformers=[('code1', OneHotEncoder(), [0,1])])

    Coder2 = MaxAbsScaler()

    Model = MLPClassifier(hidden_layer_sizes=(5, 4))

    Model = Pipeline(steps=[('code1', Coder1), ('code2', Coder2), ('neur', Model)])
    Model.fit(X, y)

    if request.method == 'POST':
        if form.validate() == True:
            return render_template('AI_form.html', form=form)

        new_method = [
            [form.output_type.data, form.memory_size.data]]
        y_ = Model.predict(new_method)
        # print(y_)
        return render_template('ok.html', result=y_[0])
    elif request.method == 'GET':
        return render_template('AI_form.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    my_query = (
        db.session.query(
            OrmUser.user_email,
            func.count(OrmClass.class_name).label('classes_count')
        ).join(OrmClass, OrmClass.user_email == OrmUser.user_email).
            group_by(OrmUser.user_email)
    ).all()

    re_query = (
        db.session.query(
            OrmClass.class_name,
            func.count(OrmMethod.method_name).label('methods_count')
        ).join(OrmMethod, OrmMethod.class_name == OrmClass.class_name).
            group_by(OrmClass.class_name)
    ).all()


    user_id, feature_count = zip(*my_query)

    bar = go.Bar(
        x=user_id,
        y=feature_count
    )

    feature_id, remedy_count = zip(*re_query)
    pie = go.Pie(
        labels=feature_id,
        values=remedy_count
    )

    query3 = db.session.query(OrmClass.methods_quantity,func.count(OrmClass.class_name)).group_by(OrmClass.methods_quantity).all()

    names, skill_counts = zip(*query3)
    scat = go.Scatter(
        x=names,
        y=skill_counts,
        mode='markers'
    )

    data = {
        "bar": [bar],
        "pie": [pie],
        "scat": [scat]
    }

    x = []
    y = []

    query_for_cor = db.session.query(OrmClass.methods_quantity,func.count(OrmClass.class_name)).group_by(OrmClass.methods_quantity).all()
    print(query_for_cor)
    for i in query_for_cor:
        x.append((i[0]))
        y.append(i[1])
    corr_coef = np.corrcoef(x, y)[0][1]

    massage = None

    if fabs(corr_coef) < 0.33:
        massage = 'weak dependence'
    else:
        massage = 'perceptible dependence'


    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphsJSON=graphs_json,massage=massage,corr_coef=corr_coef)


def trio(word, number):
    return(word[number:number+3])


def search_in_sent(search_word, description_str):
    desc_split = description_str.split()
    count_overlap = 0
    for three in range(len(search_word)):
        for word in desc_split:
            if len(word) >= 3 and len(word) > len(search_word):
                for i in range(len(word) - 2):
                    if trio(word, i) == trio(search_word, three):
                        count_overlap += 0.24
            else:
                continue

    for word in desc_split:
        if len(word) >= 3 and len(word) <= len(search_word):
            diff = len(search_word) - len(word)
            for s in range(diff + 1):
                if search_word[s:s + len(word)] == word:
                    count_overlap += 1
    return count_overlap


@app.route('/Hashtag', methods=['GET', 'POST'])
def Hashtag():
    form = HastagForm()
    if request.method == 'POST':
        if form.validate():
            choice = form.choice.data
            words = form.words.data

            if choice == 'class':
                descriptions = db.session.query(OrmClass.class_description).all()
            if choice == 'method':
                descriptions = db.session.query(OrmMethod.method_description).all()
            if choice == 'parameter':
                descriptions = db.session.query(OrmParameter.parameter_description).all()

            desc_score = {}
            scores = []
            for desc in list(descriptions):
                sum_score = 0
                for word in words.split():
                    sum_score += search_in_sent(word, desc[0])
                desc_score[sum_score] = desc
                scores.append(sum_score)


            scores.sort(reverse = True)

            if max(scores) < 0.2:
                return render_template('not_found.html')

            scores = list(dict.fromkeys(scores))
            sorted_for_html = []
            print(scores)
            print(desc_score)
            if choice == 'class':
                for score in scores:
                    if score < 0.22:
                        continue
                    res = db.session.query(OrmClass).filter(OrmClass.class_description == desc_score[score]).all()
                    for row in res:
                        sorted_for_html.append(row)
                return render_template('class_table.html', classes=sorted_for_html)

            if choice == 'method':
                for score in scores:
                    if score < 0.22:
                        continue
                    res = db.session.query(OrmMethod).filter(OrmMethod.method_description == desc_score[score]).all()
                    for row in res:
                        sorted_for_html.append(row)
                return render_template('methods_table.html', methods=sorted_for_html)

            if choice == 'class':
                for score in scores:
                    if score < 0.22:
                        continue
                    res = db.session.query(OrmParameter).filter(OrmParameter.parameter_description == desc_score[score]).all()
                    for row in res:
                        sorted_for_html.append(row)
                return render_template('parameters_table.html', parameters=sorted_for_html)
        else:
            return render_template('hashtag_form.html', form=form)
    elif request.method == 'GET':
        return render_template('hashtag_form.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
