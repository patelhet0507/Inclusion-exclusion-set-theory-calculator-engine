from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():

    result = None
    error = None

    if request.method == "POST":

        operation = request.form["operation"]

        try:
            A = int(request.form.get("A",0))
            B = int(request.form.get("B",0))
            C = int(request.form.get("C",0))

            AB = int(request.form.get("AB",0))
            AC = int(request.form.get("AC",0))
            BC = int(request.form.get("BC",0))
            ABC = int(request.form.get("ABC",0))

            if operation == "union3":

                result = A + B + C - AB - AC - BC + ABC

            elif operation == "union2":

                result = A + B - AB

            elif operation == "intersection":

                result = AB

            elif operation == "difference":

                result = A - AB

            else:
                error = "Please select a valid operation"

        except ValueError:
            error = "⚠ Please enter valid numbers only."

    return render_template("index.html", result=result, error=error)

@app.route("/calculate", methods=["POST"])
def calculate():
    operation = request.form.get("operation")
    if not operation:
        return jsonify({"error": "No operation selected"})
    
    try:
        A = int(request.form.get("A", 0))
        B = int(request.form.get("B", 0))
        AB = int(request.form.get("AB", 0))
        
        if operation == "union3":
            C = int(request.form.get("C", 0))
            AC = int(request.form.get("AC", 0))
            BC = int(request.form.get("BC", 0))
            ABC = int(request.form.get("ABC", 0))
            result = A + B + C - AB - AC - BC + ABC
            if result < 0:
                return jsonify({"error": "Invalid input: union cannot be negative"})
        elif operation == "union2":
            result = A + B - AB
            if result < 0:
                return jsonify({"error": "Invalid input: union cannot be negative"})
        elif operation == "intersection":
            result = AB
        elif operation == "difference":
            result = A - AB
            if result < 0:
                return jsonify({"error": "Invalid input: difference cannot be negative"})
        else:
            return jsonify({"error": "Invalid operation"})
        
        return jsonify({"result": result})
    except ValueError:
        return jsonify({"error": "Please enter valid numbers only."})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)