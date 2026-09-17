import requests

class DataExtractor:
    # VARIABLES
    iterable_tables = ["Empresas", "Estabelecimentos", "Socios"]
    url_cnpj_receita = "https://arquivos.receitafederal.gov.br/public.php/dav/files/YggdBLfdninEJX9"
    
    def __init__(self):
        self.extract_from_receita_federal = self.extract_from_receita_federal
        
        print("DataExtractor initialized. Ready to extract data from Receita Federal.")

    def download_file(self, url, filename):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"File downloaded successfully: {filename}")
        else:
            print(f"Failed to download file: {filename}")


    def extract_from_receita_federal(self, year_month, table_name):
        iterator_limit = [0,1,2,3,4,5,6,7,8,9]

        if table_name not in self.iterable_tables: 
            url = f"{self.url_cnpj_receita}/{year_month}/{table_name}.zip"
            print(f"Downloading: {url}")
            self.download_file(url, f"{table_name}.zip")
            return

        for iterator in iterator_limit:
            url = f"{self.url_cnpj_receita}/{year_month}/{table_name}{iterator}.zip"
            
            print(f"Downloading: {url}")
            self.download_file(url, f"{table_name}{iterator}.zip")

            if iterator == iterator_limit[-1]: 
                break
            
