from flask import Flask, request, jsonify
import duckdb
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

conn = duckdb.connect('dw.duckdb', read_only=True)


@app.route('/get_table_data', methods=['GET'])
def get_table_data():
    table_name = request.args.get('table_name')
    limit = request.args.get('limit', default=10, type=int)

    try:
        app.logger.info(f"Recebendo dados da tabela: {table_name}, limite: {limit}")
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        result = conn.execute(query).fetchall()
        columns = [desc[0] for desc in conn.description]

        return jsonify({'columns': columns, 'data': result})
    except Exception as e:
        app.logger.error(f"Erro ao buscar dados da tabela: {e}")
        return jsonify({'error': str(e)})


@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql_query = request.json.get('query')

    try:
        app.logger.info(f"Executando consulta SQL: {sql_query}")
        result = conn.execute(sql_query).fetchall()
        columns = [desc[0] for desc in conn.description]

        return jsonify({'columns': columns, 'data': result})
    except Exception as e:
        app.logger.error(f"Erro ao executar consulta SQL: {e}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.logger.info("Iniciando a aplicação Flask...")
    app.run(debug=True)
