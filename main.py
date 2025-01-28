import sys
from utils import generate_random_dates, get_today_date
from fetcher import fetch_news, save_to_folder

def main(start_date, end_date, folder, news_type):

    news_types = [
        'latest-announcements',
        'p2p-trading',
        'deposit-withdrawal-suspension-resumption',
        'derivatives',
        'fiat-gateway',
        'new-token',
        'introduction-to-digital-assets',
        'okb-buy-back-burn',
        'api',
        'spot-margin-trading',
        'others'
    ]

    if news_type not in news_types:
        print(f"Invalid news type. Valid options are: {', '.join(news_types)}")
        sys.exit(1)

    print(f"Selected news type: {news_type}")
    news_items = fetch_news(start_date, end_date, news_type)
    save_to_folder(news_items, folder)
    print(f"Downloaded {len(news_items)} news items from {start_date} to {end_date}.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py <start_date> <end_date> <output_directory> <news_type>")
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    output_directory = sys.argv[3]
    news_type = sys.argv[4]

    main(start_date, end_date, output_directory, news_type)