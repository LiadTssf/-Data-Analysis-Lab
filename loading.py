import kagglehub
from kagglehub import KaggleDatasetAdapter

FILE_PATH = "mobile_sales_data.csv"
HANDLE = "vinothkannaece/mobiles-and-laptop-sales-data"
def load_base_dataset() :
# Load the latest version
    return kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
  HANDLE,FILE_PATH)