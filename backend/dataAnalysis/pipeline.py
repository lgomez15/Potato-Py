import tempAPI
import lstRead
import predictiveModel
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Data Analysis Pipeline")
tempAPI.fetch_data('-5.664428', '40.935565', 'Salamanca', '09-01-2024', '12-01-2024')
lstRead.format_data()
predictiveModel.predict()