import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response
from flask import flash, request
from contextlib import closing

basic_auth = auth

#Criando as Rotas API para a Tabela Cursos
@app.route('/produtos', methods = ['POST'])
@basic_auth.required
def add_produtos_cursos():
	try:
		_json = request.get_json(force = True)
		_id = _json['idCurso']
		_nome = _json['nome']
		_descricao = _json['descricao']
		_carga = _json['carga']
		_totalaulas = _json['total_aulas']
		_ano = _json['ano']
		_preco = _json['preco']	
		_ativo = _json['ativo']	
		if _nome and _descricao and _carga and _totalaulas and _ano and _preco and _ativo and request.method == 'POST':			
			sqlQuery = "INSERT INTO produtos.cursos(idCurso, nome, descricao, carga, total_aulas, ano, preco, ativo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
			bindData = (_id, _nome, _descricao, _carga, _totalaulas, _ano, _preco, _ativo)
			with closing(mysql.connect()) as conn:
				with closing(conn.cursor()) as cursor:
					conn = mysql.connect()
					cursor = conn.cursor(pymysql.cursors.DictCursor)
					cursor.execute(sqlQuery, bindData)
					conn.commit()
					response = jsonify('Employee added successfully!')
					response.status_code = 200
					return response
		else:
			return not_found()
	except Exception as e:
		print(e)

@app.route('/produtos', methods = ['GET'])
@basic_auth.required
def cursos():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCurso, nome, descricao, carga, total_aulas, ano, preco, ativo FROM produtos.cursos")
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/produtos/<int:idCurso>', methods =['GET'])
@basic_auth.required
def produtos_pesquisar_id(idCurso):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCurso, nome, descricao, carga, total_aulas, ano, preco, ativo FROM produtos.cursos WHERE idCurso = %s", idCurso)
		userRows = cursor.fetchone()
		if not userRows:
			return Response('Produto não encontrado', status = 404)
		print(type(userRows))
		response = jsonify(userRows)
		response.status_code = 200
		return response

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/produtos', methods=['PUT'])
@basic_auth.required
def update_produtos():
	try:
		_json = request.get_json(force = True)
		_id = _json['idCurso']
		_nome = _json['nome']
		_descricao = _json['descricao']
		_carga = _json['carga']
		_totalaulas = _json['total_aulas']
		_ano = _json['ano']
		_preco = _json['preco']	
		_ativo = _json['ativo']	
		if _nome and _descricao and _carga and _totalaulas and _ano and _preco and _ativo and request.method == 'PUT':
			sqlQuery = "UPDATE produtos.cursos SET nome=%s, descricao=%s, carga=%s, total_aulas=%s, ano=%s, preco=%s, ativo=%s WHERE idCurso=%s"
			bindData = (_nome, _descricao, _carga, _totalaulas, _ano, _preco, _ativo, _id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('User updated successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()

	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

@app.route('/produtos/<int:idCurso>', methods=['DELETE'])
@basic_auth.required
def delete_produtos(idCurso):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM produtos.cursos WHERE idCurso ={}".format(idCurso))
		conn.commit()
		response = jsonify('Employee deleted successfully!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5200)
