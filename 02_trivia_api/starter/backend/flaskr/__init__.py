import os
from flask import Flask, request, abort, jsonify
import sqlalchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app)

  

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request # blueprint can also be app~~
  def after_request(response):
	  header = response.headers
	  header['Access-Control-Allow-Origin'] = '*'
	  return response


  @app.route('/')
  def index_page():
    return "Hello World"


  @app.route('/categories')
  def categories():
    category = Category.query.all()
    d = {i.id: i.type for i in category}
    # print(d)
    result = {"categories":d}
    return jsonify(result)


  @app.route('/questions')
  def return_question():
    page_no = request.args.get('page_no')
    # question = Question.query.pagination(page_no, QUESTIONS_PER_PAGE,error_out=False) # todo
    question = Question.query.paginate(page_no, QUESTIONS_PER_PAGE,error_out=False)
    # all().pagina
    
    q = []
    curr = []
    # question = {i.question: i.answer for i in question}

    for i in question.items:
      q.append(i.question)
      # cat+=i.categories
      curr.append(i.category)

    res = {
      "questions":q,
      "totalQuestions": question.total,
      "categories":len(curr),
      "currentCategory": curr
    }

    return jsonify(res)
  
  
  @app.route('/delete/<int:id>', methods=['DELETE'])
  def delete_ques_from_id():
    if request.method != "DELETE":
      return
    
    ques_id = id
    question = Question.query.filter_by(id=ques_id).first()
    question.delete()
    
    r = {"question: "+ques_id: "deleted"}
    r = jsonify(r)
    r.status_code = 200
    return r
	
  
  @app.route('/create_question',methods=['POST'])
  def create_question():
    question = request.args.get('question')
    answer = request.args.get('answer')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty_score')
    question = Question(question,answer,category,difficulty)
    question.insert()
	

  @app.route('/search_term', methods=['POST'])
  def search_term():
    term = request.args.get('search_term')
    question_list = Question.query.filter(Question.question.contains(term))
    total = Question.query.all()

    question_list = []
    cat_list = []

    for i in question_list:
      question_list.append(i.question)
      # cat+=i.categories
      cat_list.append(i.category)

    return jsonify({
      "questions":question_list,
      "totalQuestions":len(total),
      "currentCategory": cat_list
    })
	


  @app.route('/categories/<int:id>/questions')
  def get_question_by_category():
    category = id
    c_list = Question.query.filter_by(category=category)
    all_ques = Question.query.all()
    
    rel_ques = []
    cat = []

    for i in c_list:
      rel_ques.append(i.question)
      cat.append(i.category)



    return jsonify({
      "questions": rel_ques,
      "totalQuestions": all_ques,
      "currentCategory": cat
    })


  @app.route('random_question', methods=["POST"])
  def return_random_question():
    category = request.args.get('category')
    q_list = request.args.get('prev_params')
    query = []
    if category!="":
      query = Question.query.filter_by(category)
    else:
      query = Question.query.all()

    while query[0] not in q_list:
      random.shuffle(query)

    return query[0]


  @app.errorhandler(404)
  def page_not_found(e):
	  return 404
	
  
  
  return app

	