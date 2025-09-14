from flask import Flask, request, jsonify
import hashlib
from database import fetch_account_birthdate_hash, fetch_account_balance

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome! Please verify your birth date to access your account balance."


@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    account_birth_date = data.get("birth_date", "")
    account_id = data.get("id", "")
    hashed_input = hashlib.md5(account_birth_date.encode()).hexdigest()
    hashed_secret = fetch_account_birthdate_hash(account_id)

    if hashed_input == hashed_secret:
        return jsonify({"success": True, "message": "Verification successful!", "secret_username": fetch_account_balance(account_id)})
    else:
        return jsonify({"success": False, "message": "Verification failed. Incorrect birth date."})
