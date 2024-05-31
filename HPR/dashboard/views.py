from django.shortcuts import render, redirect
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

# Use the Agg backend for rendering plots to a file instead of displaying them
plt.switch_backend('Agg')

def index(request):
    return render(request, 'dashboard/index.html')

def run_script(request):
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
            for h in range(hmin, hmax):
                best_value = -float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] >= best_value:
                        best_value = R[(t,h)]
                best[h - hmin] = best_value
            return best

        def build_worst(R, T, hmin, hmax):
            worst = [None] * (hmax - hmin)
            for h in range(hmin, hmax):
                worst_value = float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] <= worst_value:
                        worst_value = R[(t,h)]
                worst[h - hmin] = worst_value
            return worst

        R = buildR(P, T, hmin, hmax)
        best = build_best(R, T, hmin, hmax)
        worst = build_worst(R, T, hmin, hmax)
        
        # Plotting the best return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(best, hmin) if val is not None], 
                 [x * 100 for x in best if x is not None], linestyle='-', color='b', label='Best Return')
        plt.title('Best Return by Holding Period')
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

        # Store images in session or pass as context to new page
        request.session['best_image_base64'] = best_image_base64
        request.session['worst_image_base64'] = worst_image_base64

        # Redirect to a new page for displaying graphs
        return redirect('plot_display')

    # Render initial page template
    return render(request, 'dashboard/index.html')

def plot_display(request):
    # Retrieve images from session or context
    best_image_base64 = request.session.get('best_image_base64', None)
    worst_image_base64 = request.session.get('worst_image_base64', None)

    # Render plot_display.html with images
    return render(request, 'dashboard/plot_display.html', {'best_image_base64': best_image_base64, 'worst_image_base64': worst_image_base64})

def run_apple_analysis(request):
    if request.method == "POST":
        # Define the path to the CSV file for Apple data
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(BASE_DIR, 'data', 'AAPL_stock_data.csv')

        # Your script here for Apple data
        df = pd.read_csv(csv_file_path)

        P = df['Close'].tolist()
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
            for h in range(hmin, hmax):
                best_value = -float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] >= best_value:
                        best_value = R[(t,h)]
                best[h - hmin] = best_value
            return best

        def build_worst(R, T, hmin, hmax):
            worst = [None] * (hmax - hmin)
            for h in range(hmin, hmax):
                worst_value = float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] <= worst_value:
                        worst_value = R[(t,h)]
                worst[h - hmin] = worst_value
            return worst

        R = buildR(P, T, hmin, hmax)
        best = build_best(R, T, hmin, hmax)
        worst = build_worst(R, T, hmin, hmax)

        # Plotting the best return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(best, hmin) if val is not None], 
                 [x * 100 for x in best if x is not None], linestyle='-', color='b', label='Best Return')
        plt.title('Best Return by Holding Period - Apple Stock')
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
        plt.title('Worst Return by Holding Period - Apple Stock')
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

        # Store images in session or pass as context to new page
        request.session['best_image_base64'] = best_image_base64
        request.session['worst_image_base64'] = worst_image_base64

        # Redirect to a new page for displaying graphs
        return redirect('plot_display_apple')

    # Render initial page template
    return render(request, 'dashboard/index.html')

def plot_display_apple(request):
    # Retrieve images from session or context
    best_image_base64 = request.session.get('best_image_base64', None)
    worst_image_base64 = request.session.get('worst_image_base64', None)

    # Render plot_display_apple.html with images
    return render(request, 'dashboard/plot_display_apple.html', {'best_image_base64': best_image_base64, 'worst_image_base64': worst_image_base64})


def run_tesla_analysis(request):
    if request.method == "POST":
        # Define the path to the CSV file for Tesla data
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(BASE_DIR, 'data', 'TSLA_stock_data.csv')

        # Your script here for Tesla data
        df = pd.read_csv(csv_file_path)

        P = df['Close'].tolist()
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
            for h in range(hmin, hmax):
                best_value = -float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] >= best_value:
                        best_value = R[(t,h)]
                best[h - hmin] = best_value
            return best

        def build_worst(R, T, hmin, hmax):
            worst = [None] * (hmax - hmin)
            for h in range(hmin, hmax):
                worst_value = float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] <= worst_value:
                        worst_value = R[(t,h)]
                worst[h - hmin] = worst_value
            return worst

        R = buildR(P, T, hmin, hmax)
        best = build_best(R, T, hmin, hmax)
        worst = build_worst(R, T, hmin, hmax)

        # Plotting the best return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(best, hmin) if val is not None], 
                 [x * 100 for x in best if x is not None], linestyle='-', color='b', label='Best Return')
        plt.title('Best Return by Holding Period - Tesla Stock')
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
        plt.title('Worst Return by Holding Period - Tesla Stock')
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

        # Store images in session or pass as context to new page
        request.session['best_image_base64'] = best_image_base64
        request.session['worst_image_base64'] = worst_image_base64

        # Redirect to a new page for displaying graphs
        return redirect('plot_display_tesla')

    # Render initial page template
    return render(request, 'dashboard/index.html')

def plot_display_tesla(request):
    # Retrieve images from session or context
    best_image_base64 = request.session.get('best_image_base64', None)
    worst_image_base64 = request.session.get('worst_image_base64', None)

    # Render plot_display_apple.html with images
    return render(request, 'dashboard/plot_display_tesla.html', {'best_image_base64': best_image_base64, 'worst_image_base64': worst_image_base64})

def run_spy_analysis(request):
    if request.method == "POST":
        # Define the path to the CSV file for SPY data
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(BASE_DIR, 'data', 'SPY_stock_data.csv')

        # Your script here for SPY data
        df = pd.read_csv(csv_file_path)

        P = df['Close'].tolist()
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
            for h in range(hmin, hmax):
                best_value = -float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] >= best_value:
                        best_value = R[(t,h)]
                best[h - hmin] = best_value
            return best

        def build_worst(R, T, hmin, hmax):
            worst = [None] * (hmax - hmin)
            for h in range(hmin, hmax):
                worst_value = float('inf')
                for t in range(1, T-h):
                    if R[(t,h)] <= worst_value:
                        worst_value = R[(t,h)]
                worst[h - hmin] = worst_value
            return worst

        R = buildR(P, T, hmin, hmax)
        best = build_best(R, T, hmin, hmax)
        worst = build_worst(R, T, hmin, hmax)

        # Plotting the best return by holding period
        plt.figure(figsize=(12,10))
        plt.plot([(h / 251) for h, val in enumerate(best, hmin) if val is not None], 
                 [x * 100 for x in best if x is not None], linestyle='-', color='b', label='Best Return')
        plt.title('Best Return by Holding Period - SPY Stock')
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
        plt.title('Worst Return by Holding Period - SPY Stock')
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

        # Store images in session or pass as context to new page
        request.session['best_image_base64'] = best_image_base64
        request.session['worst_image_base64'] = worst_image_base64

        # Redirect to a new page for displaying graphs
        return redirect('plot_display_spy')

    # Render initial page template
    return render(request, 'dashboard/index.html')

def plot_display_spy(request):
    # Retrieve images from session or context
    best_image_base64 = request.session.get('best_image_base64', None)
    worst_image_base64 = request.session.get('worst_image_base64', None)

    # Render plot_display_apple.html with images
    return render(request, 'dashboard/plot_display_spy.html', {'best_image_base64': best_image_base64, 'worst_image_base64': worst_image_base64})