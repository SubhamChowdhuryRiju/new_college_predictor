from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect
from BackEnd.college_list import finalList
from BackEnd.rank_predictor import pvr

college_predictor = Blueprint('BackEnd', __name__)


@college_predictor.route('/', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        try:
            mains_rank = int(request.form['mains_rank'])
        except Exception as e:
            mains_rank = 0
        try:
            mains_percentage = float(request.form['mains_percentile'])
        except Exception as e:
            mains_percentage = 0.0
        try:
            advance_rank = int(request.form['advanced_rank'])
        except Exception as e:
            advance_rank = 0
        state = request.form['inputState']
        category = request.form['category']
        gender = request.form['gender']
        pwd = request.form['pwd']
        limit = int(request.form['limit'])

        if mains_rank == 0:
            mains_rank = int((100 - mains_percentage) * 823967 / 100)

        rank_score = int(pvr(mains_percentage, pwd, category))
        college_list_result = finalList(mains_rank, mains_percentage, category, state, gender, pwd, limit, advance_rank)
        current_year = datetime.now().year

        return render_template('result.html', year=current_year, ranks=mains_rank, category=category,
                               college_list_result=college_list_result.to_html(classes='table table-striped table '
                                                                                       'table-bordered table-striped '
                                                                                       'custom-table',
                                                                               index=False)), 200
    return render_template('index.html'), 200

