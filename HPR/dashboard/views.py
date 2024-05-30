from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

# Use the Agg backend for rendering plots to a file instead of displaying them
plt.switch_backend('Agg')

def run_script(request):
    best_image_base64 = None
    worst_image_base64 = None

    if request.method == "POST":
        # Define the path to the CSV file
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(BASE_DIR, 'data', 'bitcoin_price_consolidated_weekdays.csv')

        # Your script here
        df = pd.read_csv(csv_file_path)
        
        P = df['Price'].tolist()
        dates = df['Date'].tolist()
        T = len(P)
        hmin = 251
        hmax = T

        def buildR(P, T, hmin, hmax):
            R = {}
            for h in range(hmin, hmax):
                for t in range(1, T-h):
                    buy_price = P[t]
                    sell_price = P[t+h]
                    return_val = ((((sell_price/buy_price) ** (251.0 / h))) - 1)
                    R[(t,h)] = return_val
            return R

        def build_best(R, T, hmin, hmax):
            best = [None] * (hmax - hmin)
            dates_best_horizon = [None] * (hmax - hmin)
            best_info = []
            for h in range(hmin, hmax):
                best_value = -float('inf')
                best_index = None
                for t in range(1, T-h):
                    if R[(t,h)] >= best_value:
                        best_value = R[(t,h)]
                        best_index = t
                if best_index is not None:
                    buy_price = P[best_index]
                    sell_price = P[best_index+h]
                    buy_date = dates[best_index]
                    sell_date = dates[best_index+h]
                    best_info.append([h/251, best_value, buy_price, buy_date, sell_price, sell_date])
                    best[h - hmin] = best_value
                    dates_best_horizon[h - hmin] = buy_date
            df_best = pd.DataFrame(best_info, columns=['Holding Period(Years)', 'Annualized Return', 'Buy Price', 'Buy Date', 'Sell Price', 'Sell Date'])
            df_best.to_csv(os.path.join(BASE_DIR, 'data', 'best_btc_consolidated_weekdays.csv'), index=False)
            return best, dates_best_horizon

        def build_worst(R, T, hmin, hmax):
            worst = [None] * (hmax - hmin)
            dates_worst_horizon = [None] * (hmax - hmin)
            worst_info = []
            for h in range(hmin, hmax):
                worst_value = float('inf')
                worst_index = None
                for t in range(1, T-h):
                    if R[(t,h)] <= worst_value:
                        worst_value = R[(t,h)]
                        worst_index = t
                if worst_index is not None:
                    buy_price = P[worst_index]
                    sell_price = P[worst_index+h]
                    buy_date = dates[worst_index]
                    sell_date = dates[worst_index+h]
                    worst_info.append([h/251, worst_value, buy_price, buy_date, sell_price, sell_date])
                    worst[h - hmin] = worst_value
                    dates_worst_horizon[h - hmin] = buy_date
            df_worst = pd.DataFrame(worst_info, columns=['Holding Period(Years)', 'Annualized Return', 'Buy Price', 'Buy Date', 'Sell Price', 'Sell Date'])
            df_worst.to_csv(os.path.join(BASE_DIR, 'data', 'worst_btc_consolidated_weekdays.csv'), index=False)
            return worst, dates_worst_horizon

        R = buildR(P, T, hmin, hmax)
        best, best_dates = build_best(R, T, hmin, hmax)
        worst, worst_dates = build_worst(R, T, hmin, hmax)
        
        # Plotting the best return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(best, hmin) if val is not None], 
                 [x * 100 for x in best if x is not None], linestyle='-', color='b', label='Best Return')
        plt.title('Best Return by Holding Period')
        plt.suptitle('Value of Scarcity', fontsize=16)
        plt.xlabel('Holding Period (Years)')
        plt.ylabel('Average Annualized Return (%)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        best_image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Plotting the worst return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(worst, hmin) if val is not None], 
                 [x * 100 for x in worst if x is not None], 
                 linestyle='-', color='r', label='Worst Return')
        plt.title('Worst Return by Holding Period')
        plt.suptitle('Value of Scarcity', fontsize=16)
        plt.xlabel('Holding Period (Years)')
        plt.ylabel('Average Annualized Return (%)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        worst_image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

    # Render plot_display.html with data
    return render(request, 'dashboard/index.html', {'best_image_base64': best_image_base64, 'worst_image_base64': worst_image_base64})
