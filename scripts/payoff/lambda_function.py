import json


def lambda_handler(event, context):
    try:
        # Extract body from POST request
        body = json.loads(event.get('body', '{}'))

        # Get input values and convert to float
        car1_mpg = float(body.get('car1_mpg', 0))
        car1_price = float(body.get('car1_price', 0))
        car2_mpg = float(body.get('car2_mpg', 0))
        car2_price = float(body.get('car2_price', 0))
        gas_price = 4.0  # $4/gallon as specified

        # Validate inputs
        if car1_mpg <= 0 or car2_mpg <= 0 or car1_price < 0 or car2_price < 0:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input: MPG must be positive, prices must be non-negative'})
            }

        # Determine which car has higher MPG
        if car1_mpg > car2_mpg:
            higher_mpg = car1_mpg
            lower_mpg = car2_mpg
            higher_price = car1_price
            lower_price = car2_price
        else:
            higher_mpg = car2_mpg
            lower_mpg = car1_mpg
            higher_price = car2_price
            lower_price = car2_price

        # If higher MPG car is cheaper, it already breaks even
        if higher_price <= lower_price:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'break_even_miles': 0,
                    'message': 'Higher MPG car is already cheaper or equal in price'
                })
            }

        # Calculate cost per mile for each car
        cost_per_mile_higher = gas_price / higher_mpg
        cost_per_mile_lower = gas_price / lower_mpg

        # Calculate break-even mileage
        price_diff = higher_price - lower_price
        cost_per_mile_diff = cost_per_mile_lower - cost_per_mile_higher
        break_even_miles = price_diff / cost_per_mile_diff if cost_per_mile_diff != 0 else float('inf')

        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'break_even_miles': round(break_even_miles, 2),
                'higher_mpg_car': {
                    'mpg': higher_mpg,
                    'price': higher_price
                },
                'lower_mpg_car': {
                    'mpg': lower_mpg,
                    'price': lower_price
                }
            })
        }

    except (ValueError, TypeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input: All parameters must be numeric'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }