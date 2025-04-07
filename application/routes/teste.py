from flask import Blueprint, jsonify
from application.models import (
    create_tables,
    insert_user,
    get_all_users,
    get_user_balance,
    list_user_transactions,
    make_transfer,
    get_user_by_email,
)

teste_bp = Blueprint("teste", __name__, url_prefix="/teste")


@teste_bp.route("/", methods=["GET"])
def getUsers():
    # Criação dos usuários (evitar duplicados seria o ideal com try/except, aqui é só para testes rápidos)
    try:
        user1 = get_user_by_email("joao@email.com") or insert_user(
            "João da Silva", "12345678901", "joao@email.com", "hashed_password", "comum"
        )
    except Exception as e:
        return jsonify({"error": "Usuário João já existe"}), 400

    try:
        user2 = get_user_by_email("contato@xpto.com") or insert_user(
            "Loja XPTO", "12345678000199", "contato@xpto.com", "hashed_pass", "lojista"
        )
    except Exception as e:
        return jsonify({"error": "Usuário Loja já existe"}), 400

    # Saldo
    saldo_joao = get_user_balance(user1)

    # Transferência
    try:
        transfer_id = make_transfer(user1, user2, 50.00)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Transações
    transacoes_joao = list_user_transactions(user1)

    return jsonify(
        {
            "usuarios": get_all_users(),
            "saldo_joao": str(saldo_joao),
            "transferencia_id": transfer_id,
            "transacoes_joao": transacoes_joao,
        }
    )
