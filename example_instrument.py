if __name__ == "__main__":
    from src.wom_connector.instrument import Instrument
    from src.wom_connector.voucher import Voucher
    import datetime

    privk = open("keys/instrument1.pem", "rb")

    coords = [(46.9, 12.0),
              (46.8, 12.1),
              (46.7, 12.2),
              (46.6, 12.3),
              (46.5, 12.4),
              (46.4, 12.5),
              (46.3, 12.6),
              (46.2, 12.7),
              (46.1, 12.8),
              (46.0, 12.9)]

    # vouchers can be specified as a list of Voucher instances
    vouchers = []
    for c in coords:
        vouchers.append(Voucher.create(aim='H', latitude=c[0], longitude=c[1], timestamp=datetime.datetime.utcnow()))

    '''
    # or as list of simple dictionaries
    vouchers = [{'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1},
                {'aim': 'H', 'latitude': 46.9, 'longitude': 12.0, 'timestamp': '2020-01-28T17:08:24.073280', 'count': 1}]
    '''

    connector = Instrument(domain='dev.wom.social',  # this will be 'http://wom.social/api/v1'
                           instrument_id='5e74203f5f21bb265a2d26bd',  # instrument ID
                           instrument_privk=privk.read())

    otc, password = connector.request_vouchers(vouchers=vouchers)

    print("Otc: {otc} Password:{password}".format(otc=otc, password=password))
