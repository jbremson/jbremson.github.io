import json
import re


def calculate_monthly_payment(principal, annual_interest_rate, years):
    monthly_rate = annual_interest_rate / 100 / 12
    total_payments = years * 12
    if monthly_rate == 0:
        return principal / total_payments
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / (
                (1 + monthly_rate) ** total_payments - 1)
    return monthly_payment


def calculate_payoff_miles(car1_name, car1_price, car1_mpg, car2_name, car2_price, car2_mpg,
                           fuel_cost_per_gallon, annual_interest_rate, financing_years):
    if car1_mpg < car2_mpg:
        car1_name, car2_name = car2_name, car1_name
        car1_price, car2_price = car2_price, car1_price
        car1_mpg, car2_mpg = car2_mpg, car1_mpg

    monthly_payment_car1 = calculate_monthly_payment(car1_price, annual_interest_rate, financing_years)
    monthly_payment_car2 = calculate_monthly_payment(car2_price, annual_interest_rate, financing_years)

    total_cost_car1 = monthly_payment_car1 * financing_years * 12
    total_cost_car2 = monthly_payment_car2 * financing_years * 12

    cost_diff = total_cost_car1 - total_cost_car2

    cost_per_mile_car1 = fuel_cost_per_gallon / car1_mpg
    cost_per_mile_car2 = fuel_cost_per_gallon / car2_mpg

    savings_per_mile = cost_per_mile_car2 - cost_per_mile_car1


    if savings_per_mile < 0:
        return f"{car1_name} with {car1_mpg} MPG will never pay off compared to {car2_name} with {car2_mpg} MPG"
    elif savings_per_mile == 0:
        return f"{car1_name} and {car2_name} are equivalent in terms of MPG and financing costs"
    miles_to_payoff = cost_diff / savings_per_mile

    return f"{car1_name} with {car1_mpg} MPG will pay off after {miles_to_payoff:,.0f} miles compared to {car2_name} with {car2_mpg} MPG, including financing at {annual_interest_rate}% over {financing_years} years"


def lambda_handler(event, context):
    # Get the Origin header from the request
    print("Received event:")
    print(json.dumps(event))  # Log the entire event object

    origin = event.get('headers', {}).get('origin', '')

    # Define allowed origin pattern (subdomains of autopiaproject.org)
    cors_headers = {
        'Access-Control-Allow-Origin': "https://www.autopiaproject.org",
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,content-type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    }

    if not event.get('httpMethod'):
        event['httpMethod'] = None

    # Handle preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'CORS preflight'})
        }

    try:

        # Validate required fields
        required_fields = [
            'car1_name', 'car1_price', 'car1_mpg',
            'car2_name', 'car2_price', 'car2_mpg',
            'fuel_cost', 'interest_rate', 'financing_years'
        ]

        body = json.loads(event.get('body', '{}'))

        print(f"body = {body}")
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f"Missing required field: {field} - {event}"})
                }

        # Extract and convert inputs
        car1_name = body['car1_name']
        car1_price = float(body['car1_price'])
        car1_mpg = float(body['car1_mpg'])
        car2_name = body['car2_name']
        car2_price = float(body['car2_price'])
        car2_mpg = float(body['car2_mpg'])
        fuel_cost = float(body['fuel_cost'])
        interest_rate = float(body['interest_rate'])
        financing_years = int(body['financing_years'])

        # Calculate result
        result = calculate_payoff_miles(
            car1_name, car1_price, car1_mpg,
            car2_name, car2_price, car2_mpg,
            fuel_cost, interest_rate, financing_years
        )

        return {
            'statusCode': 200,
            'headers': cors_headers,
            'event': json.dumps({'result': result})
        }

    except (ValueError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'event': json.dumps({'error': 'Invalid input format'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'event': json.dumps({'error': f'Server error: {e}'})
        }