from nordpool import elspot
from datetime import datetime
from pytz import timezone
from currency_converter import CurrencyConverter

def get_current_price(prices, area, tz):
    now = datetime.now(tz).hour
    for period in prices['areas'][area]['values']:
        start, end = period['start'].hour, period['end'].hour
        if start <= now <= end:
            current_price = period['value']
            c = CurrencyConverter()
            # EUR/MWh -> øre/kWh
            converted_price = c.convert(current_price, 'EUR', 'NOK') / 10
            return converted_price
    return None

def print_price_table(prices, area):
    for period in prices['areas'][area]['values']:
        start = period['start'].strftime("%Y-%m-%d %H:%M")
        end = period['end'].strftime("%Y-%m-%d %H:%M")
        price = period['value']
        print(f"Period: {start} - {end}, Price: {price} EUR/MWh")

def should_charge(prices, area, tz, max_price):
    current_price = get_current_price(prices, area, tz)
    if current_price is not None:
        return current_price <= max_price
    return False

def main():
    # Time and Area
    area = 'Tr.heim'
    tz = timezone('Europe/Oslo')

    max_price = 50

    # Get hourly prices
    elspot_prices = elspot.Prices()
    prices = elspot_prices.hourly(areas=[area])

    print(f"Current price is: {round(get_current_price(prices, area, tz), 2)} øre/kWh")
    print(f"Price limit is: {max_price}")
    print("Should Charge?:", should_charge(prices, area, tz, max_price))

if __name__ == "__main__":
    main()
