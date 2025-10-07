"""
Debug: Sprawdź WSZYSTKIE metryki które zwraca Finnhub dla AAPL
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.services.finnhub_client import FinnhubClient
import json

client = FinnhubClient()
fundamentals = client.get_fundamentals("AAPL")

print("=" * 80)
print("FINNHUB FUNDAMENTALS - FULL RESPONSE FOR AAPL")
print("=" * 80)

if fundamentals and 'metric' in fundamentals:
    metrics = fundamentals['metric']

    print(f"\n📊 Total metrics: {len(metrics)}")

    # Wypisz WSZYSTKIE metryki alfabetycznie
    print("\n" + "=" * 80)
    print("ALL METRICS (alphabetically):")
    print("=" * 80)

    for key in sorted(metrics.keys()):
        value = metrics[key]
        print(f"{key:40s} = {value}")

    # Sprawdź które metryki są 0 lub None
    print("\n" + "=" * 80)
    print("ZERO OR NULL METRICS:")
    print("=" * 80)

    zero_metrics = {k: v for k, v in metrics.items() if v == 0 or v is None or v == 0.0}
    print(f"Found {len(zero_metrics)} zero/null metrics:\n")

    for key in sorted(zero_metrics.keys()):
        print(f"  {key}")

    # Sprawdź series (historical data)
    print("\n" + "=" * 80)
    print("SERIES (Historical Data):")
    print("=" * 80)

    if 'series' in fundamentals:
        series = fundamentals['series']
        print(f"Keys: {series.keys()}")

        if 'annual' in series:
            print(f"\nAnnual data keys: {series['annual'].keys()}")

            # Sprawdź revenue
            if 'revenue' in series['annual']:
                revenue = series['annual']['revenue']
                print(f"\nRevenue data points: {len(revenue)}")
                if revenue:
                    print(f"First entry: {revenue[0]}")
            else:
                print("\n❌ NO REVENUE DATA in annual series")
        else:
            print("\n❌ NO ANNUAL DATA in series")
    else:
        print("\n❌ NO SERIES DATA")

    # Szukaj konkretnych metryk które nas interesują
    print("\n" + "=" * 80)
    print("MULTIBAGGER SCANNER METRICS:")
    print("=" * 80)

    target_metrics = [
        'roeTTM',
        'roicTTM',
        'totalDebtToEquity',
        'debtEquityRatio',
        'currentDebtToEquity',
        'longTermDebtToEquity',
        'netMargin',
        'netMarginTTM',
        'operatingMargin',
        'operatingMarginTTM',
        'peTTM',
        'marketCapitalization',
        'revenueGrowth',
        'revenueGrowthTTM'
    ]

    for metric in target_metrics:
        value = metrics.get(metric, '❌ NOT FOUND')
        status = "✅" if value not in [0, 0.0, None, '❌ NOT FOUND'] else "❌"
        print(f"{status} {metric:30s} = {value}")

else:
    print("❌ NO FUNDAMENTALS DATA")

print("\n" + "=" * 80)
