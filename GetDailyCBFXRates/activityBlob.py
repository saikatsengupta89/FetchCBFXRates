from azure.storage.filedatalake import DataLakeServiceClient

class activityBlob:

    def initialize_storage_account(storage_account_name, storage_account_key):
        
        try:
            global service_client
            service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https", storage_account_name), credential=storage_account_key)
            # print(service_client)
        except Exception as e:
            print(e)

    def list_directory_contents(container_name):
        try:
            file_system_client = service_client.get_file_system_client(file_system=container_name)
            paths = file_system_client.get_paths(path="custom")
            for path in paths:
                print(path.name + '\n')

        except Exception as e:
            print(e)

    def upload_file_to_directory(csvDF, container_name, location_rdh):
        try:
            file_system_client = service_client.get_file_system_client(file_system=container_name)
            directory_client = file_system_client.get_directory_client(location_rdh)
            file_client = directory_client.create_file("exchange_rates.csv")

            file_contents = str.encode(csvDF)

            file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
            file_client.flush_data(len(file_contents))

        except Exception as e:
            print(e)