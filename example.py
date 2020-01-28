if __name__ == "__main__":
    from src.wom_connector.connector import Connector
    import datetime

    pubk = open("keys/registry.pub", "rb")
    privk = open("keys/source1.pem", "rb")

    connector = Connector(base_url='http://dev.wom.social/api/v1',
                          ID=1,
                          registry_pubk=pubk.read(),
                          instrument_privk=privk.read())

    otc, password = connector.request_vouchers(vouchers=[
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 100},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1},
        {'Aim': 'H',
         'Latitude': 46.0,
         'Longitude': 12.0,
         'Timestamp': datetime.datetime.utcnow().isoformat(),
         "Count": 1}
    ])

    print("Otc: {otc} Password:{password}".format(otc=otc, password=password))