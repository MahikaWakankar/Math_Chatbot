from flask import Flask, request, jsonify, session, render_template, redirect
from flask_mysqldb import MySQL
import sympy as sp

app = Flask(__name__)

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change if using a remote MySQL server
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # Your MySQL password
app.config['MYSQL_DB'] = 'math_chatbot'  # Name of the database

# Initialize MySQL
mysql = MySQL(app)

# Secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key'

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Differentiation page
@app.route('/differentiation', methods=['GET'])
def differentiation_page():
    return render_template('differentiation.html')

# Integration page
@app.route('/integration', methods=['GET'])
def integration_page():
    return render_template('integration.html')

# Trigonometry page
@app.route('/trigonometry', methods=['GET'])
def trigonometry_page():
    return render_template('trigonometry.html')

# Inverse Trigonometry page
@app.route('/inverse_trigonometry', methods=['GET'])
def inverse_trigonometry_page():
    return render_template('inverse_trigonometry.html')

# Simplify page
@app.route('/simplify', methods=['GET'])
def simplify_page():
    return render_template('simplify.html')

# Calculate differentiation with working
@app.route("/calculate_differentiation", methods=["POST"])
def calculate_differentiation():
    data = request.json
    expression = data.get('expression', '').strip()

    try:
        func = sp.sympify(expression)
        variable = sp.symbols('x')
        derivative = sp.diff(func, variable)

        # Create a working explanation
        working_steps = f"To differentiate {func}, we apply the power rule and get: {derivative}"

        return jsonify({"response": f"Derivative: {derivative}", "working": working_steps})
    
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

# Calculate integration with working
@app.route("/calculate_integration", methods=["POST"])
def calculate_integration():
    data = request.json
    expression = data.get('expression', '').strip()

    try:
        func = sp.sympify(expression)
        variable = sp.symbols('x')
        integral = sp.integrate(func, variable)

        # Create a working explanation
        working_steps = f"To integrate {func}, we apply the integration rules and get: {integral}"

        return jsonify({"response": f"Integral: {integral}", "working": working_steps})
    
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

# Calculate trigonometry result with working
# Calculate trigonometry result with working
@app.route("/calculate_trigonometry", methods=["POST"])
def calculate_trigonometry():
    data = request.json
    expression = data.get('expression', '').strip()

    try:
        # Check if the input is in degrees and convert to radians
        if "sin(" in expression or "cos(" in expression or "tan(" in expression:
            # Extract the angle from the expression
            angle_str = expression.split('(')[1].split(')')[0]
            angle = float(angle_str)  # Convert to float
            
            # Convert degrees to radians
            radians = sp.rad(angle)
            
            # Replace the original expression with the radian equivalent
            expression = expression.replace(angle_str, str(radians))

        # Now evaluate the expression
        expr = sp.sympify(expression)
        result = expr.evalf()  # Evaluate the expression to get a numerical result
        res=f"{result:.2f}"
        

        return jsonify({"response": f"Result: {res}"})
    
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# Calculate inverse trigonometry result with working

# Simplify expression with working
@app.route("/calculate_simplify", methods=["POST"])
def calculate_simplify():
    data = request.json
    expression = data.get('expression', '').strip()

    try:
        # Convert the expression to a sympy object
        expr = sp.sympify(expression)
        
        # Perform the simplification
        simplified = sp.simplify(expr)

        # Create a working explanation
        working_steps = f"To simplify the expression {expr}, we apply simplification rules and get: {simplified}"

        return jsonify({"response": f"Simplified: {simplified}", "working": working_steps})
    
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# Chat route (for chatbot functionality)
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if 'user_id' not in session:
        return jsonify({"response": "Please log in first"}), 401
    
    user_input = request.json.get("message", "").lower()
    user_id = session['user_id']
    response = ""
    options = []

    try:
        # Handle Trigonometry
        if "trigonometry" in user_input:
            func_str = user_input.replace("sin", "sp.sin").replace("cos", "sp.cos") \
                                  .replace("tan", "sp.tan").replace("cot", "sp.cot") \
                                  .replace("sec", "sp.sec").replace("csc", "sp.csc").strip()
            result = sp.sympify(func_str)
            response = f"Result: {result}"
            options = ["Solve another expression", "Differentiate", "Integrate"]
        
        # Handle Inverse Trigonometry
        elif "inverse trigonometry" in user_input:
            user_input = user_input.replace("sin^-1", "asin").replace("cos^-1", "acos") \
                                   .replace("tan^-1", "atan").replace("cot^-1", "acot") \
                                   .replace("sec^-1", "asec").replace("csc^-1", "acsc")
            expr_str = user_input.strip()
            result = sp.sympify(expr_str)
            response = f"Result: {result}"
            options = ["Solve", "Differentiate", "Integrate"]

        # Handle Differentiation
        elif "differentiate" in user_input:
            func_str = user_input.replace("differentiate", "").strip()
            func = sp.sympify(func_str)
            variable = sp.symbols('x')
            derivative = sp.diff(func, variable)
            response = f"Derivative: {derivative}"
            options = ["Differentiate another function", "Solve", "Integrate"]
        
        # Handle Integration
        elif "integrate" in user_input:
            func_str = user_input.replace("integrate", "").strip()
            func = sp.sympify(func_str)
            variable = sp.symbols('x')
            integral = sp.integrate(func, variable)
            response = f"Integral: {integral}"
            options = ["Integrate another function", "Solve", "Differentiate"]
        
        # Handle Simplification
        elif "simplify" in user_input:
            expr_str = user_input.replace("simplify", "").strip()
            expr = sp.sympify(expr_str)
            simplified = sp.simplify(expr)
            response = f"Simplified: {simplified}"
            options = ["Simplify another expression", "Solve", "Differentiate"]
        
        # Handle other cases
        else:
            response = "Sorry, I didn't understand that."
            options = ["Solve", "Differentiate", "Integrate"]

        # Store the chat history in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO chat_history (user_message, bot_response, user_id) VALUES (%s, %s, %s)",
                    (user_input, response, user_id))
        mysql.connection.commit()

    except Exception as e:
        response = f"Error: {str(e)}"

    return jsonify({"response": response, "options": options})

if __name__ == "__main__":
    app.run(debug=True)
