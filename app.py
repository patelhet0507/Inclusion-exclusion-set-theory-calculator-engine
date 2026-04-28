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

                result = A + B - AB
                if result < 0:
                    error = "Invalid input: intersection cannot be negative"

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

        if A < 0 or B < 0 or AB < 0:
            return jsonify({"error": "Invalid input: values cannot be negative"})

        if operation == "union3":
            C = int(request.form.get("C", 0))
            AC = int(request.form.get("AC", 0))
            BC = int(request.form.get("BC", 0))
            ABC = int(request.form.get("ABC", 0))

            if C < 0 or AC < 0 or BC < 0 or ABC < 0:
                return jsonify({"error": "Invalid input: values cannot be negative"})
            if AB > min(A, B) or AC > min(A, C) or BC > min(B, C):
                return jsonify({"error": "Invalid input: pairwise intersections cannot exceed the corresponding set sizes"})
            if ABC > min(AB, AC, BC):
                return jsonify({"error": "Invalid input: triple intersection cannot exceed pairwise intersections"})

            result = A + B + C - AB - AC - BC + ABC
            if result < 0:
                return jsonify({"error": "Invalid input: union cannot be negative"})

            formula = "|A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|"
            breakdown = f"{A} + {B} + {C} - {AB} - {AC} - {BC} + {ABC} = {result}"
        elif operation == "union2":
            if AB > min(A, B):
                return jsonify({"error": "Invalid input: intersection cannot exceed the smaller set size"})

            result = A + B - AB
            if result < 0:
                return jsonify({"error": "Invalid input: union cannot be negative"})

            formula = "|A ∪ B| = |A| + |B| - |A ∩ B|"
            breakdown = f"{A} + {B} - {AB} = {result}"
        elif operation == "intersection":
            if AB < max(A, B):
                return jsonify({"error": "Invalid input: |A ∪ B| cannot be less than the larger set size"})

            result = A + B - AB
            if result < 0:
                return jsonify({"error": "Invalid input: intersection cannot be negative"})

            formula = "|A ∩ B| = |A| + |B| - |A ∪ B|"
            breakdown = f"{A} + {B} - {AB} = {result}"
        elif operation == "difference":
            if AB > A or AB > B:
                return jsonify({"error": "Invalid input: intersection cannot exceed the size of either set"})

            result = A - AB
            if result < 0:
                return jsonify({"error": "Invalid input: difference cannot be negative"})

            formula = "|A - B| = |A| - |A ∩ B|"
            breakdown = f"{A} - {AB} = {result}"
        else:
            return jsonify({"error": "Invalid operation"})
        
        return jsonify({"result": result, "formula": formula, "breakdown": breakdown})
    except ValueError:
        return jsonify({"error": "Please enter valid numbers only."})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)