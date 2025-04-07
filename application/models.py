from application.db import get_db_connection


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            full_name TEXT NOT NULL,
            cpf_cnpj VARCHAR(14) NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            user_type VARCHAR(10) NOT NULL CHECK (user_type IN ('comum', 'lojista')),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # wallets
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            balance NUMERIC(14, 2) NOT NULL DEFAULT 0.00,
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # transactions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            payer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            payee_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
            created_at TIMESTAMP DEFAULT NOW(),
            status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed'))
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_user(full_name, cpf_cnpj, email, password_hash, user_type):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (full_name, cpf_cnpj, email, password_hash, user_type)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (full_name, cpf_cnpj, email, password_hash, user_type))
    user_id = cur.fetchone()[0]

    # Cria a carteira
    cur.execute("""
        INSERT INTO wallets (user_id)
        VALUES (%s);
    """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()
    return user_id


def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, user_type, created_at FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


def get_user_balance(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (user_id,))
    balance = cur.fetchone()
    cur.close()
    conn.close()
    return balance[0] if balance else None


def make_transfer(payer_id, payee_id, amount):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Verifica se o pagador é lojista
        cur.execute("SELECT user_type FROM users WHERE id = %s", (payer_id,))
        user_type = cur.fetchone()
        if not user_type or user_type[0] == 'lojista':
            raise Exception("Lojistas não podem realizar transferências")

        # Verifica saldo
        cur.execute("SELECT balance FROM wallets WHERE user_id = %s", (payer_id,))
        payer_balance = cur.fetchone()
        if not payer_balance or payer_balance[0] < amount:
            raise Exception("Saldo insuficiente")

        # Debita
        cur.execute("UPDATE wallets SET balance = balance - %s WHERE user_id = %s", (amount, payer_id))

        # Credita
        cur.execute("UPDATE wallets SET balance = balance + %s WHERE user_id = %s", (amount, payee_id))

        # Registra transação
        cur.execute("""
            INSERT INTO transactions (payer_id, payee_id, amount, status)
            VALUES (%s, %s, %s, 'completed')
            RETURNING id;
        """, (payer_id, payee_id, amount))
        transaction_id = cur.fetchone()[0]

        conn.commit()
        return transaction_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()


def list_user_transactions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            t.id,
            CASE
                WHEN t.payer_id = %s THEN 'sent'
                ELSE 'received'
            END AS direction,
            t.amount,
            CASE
                WHEN t.payer_id = %s THEN t.payee_id
                ELSE t.payer_id
            END AS counterpart_id,
            t.created_at,
            t.status
        FROM transactions t
        WHERE t.payer_id = %s OR t.payee_id = %s
        ORDER BY t.created_at DESC;
    """, (user_id, user_id, user_id, user_id))
    transactions = cur.fetchall()
    cur.close()
    conn.close()
    return transactions

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None
