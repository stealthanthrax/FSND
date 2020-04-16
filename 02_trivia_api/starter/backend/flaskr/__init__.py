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

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categories():
	category = Category.query.all()
	return jsonify({"categories": category})

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def return_question():
	  	page_no = int(request.args.get('page_no'))
		question = Question.query.pagination(page_no, QUESTIONS_PER_PAGE,error_out=False) # todo
		return jsonify(question)
  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/delete', methods=['DELETE'])
  def delete_ques_from_id():
	if request.method != "DELETE":
	  return
	
	ques_id = request.args.get('id')
	question = Question.query.filter_by(id=ques_id).first()
	question.delete()
	
	return 200
	

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/create_question',methods=['POST'])
  def create_question():
	question = request.args.get('question')
	answer = request.args.get('answer')
	category = request.args.get('category')
	difficulty = request.args.get('difficulty_score')
	question = Question(question,answer,category,difficulty)
	question.insert()
	

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search_term', methods=['POST'])
  def search_term():
      term = request.args.get('search_term')
      question_list = Question.query.filter(Question.question.contains(term))
      
      return jsonify(enumerate(question_list),200)
	


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/get_question_by_category')
  def get_question_by_category():
      category = request.args.get('category')
      c_list = Question.query.filter_by(category=category)
      
      return jsonify(enumerate(c_list))


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # todos
  @app.route('get_random_question', methods=["POST"])
  def return_random_question():
	category = request.args.get('category')
	q_list = request.args.get('prev_params')
	query = []
	if category!="":
		query = Question.query.filter_by(category)
	else:
		query = Question.query

	while query[0] not in prev_params:
		random.shuffle(query)

	return query[0]

			
  

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def page_not_found(e):
	  return 404
	
  @app.errorhandler(402)
  def page_not_found(e):
	  return 402
  
  
  return app

	