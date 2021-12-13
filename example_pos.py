if __name__ == "__main__":
    from src.wom_connector.pointofsale import POS
    from src.wom_connector.filter import Filter

    privk = open("keys/pos1.pem", "rb")

    filter = Filter.create(aim='H', left_top_bound=[46.0, -17.0], right_bottom_bound=[12.0, 160.0], max_age=14)

    pos = POS(domain='dev.wom.social',
              pos_id='5e74205c5f21bb265a2d26d8',  # POS ID
              pos_privk=privk.read())

    otc, password = pos.request_payment(amount=100,
                                        pocket_ack_url='https://example.org',
                                        filter=filter,
                                        pos_ack_url='https://example.org',
                                        persistent=False,
                                        nonce=None,
                                        password=None)

    print("Otc: {otc} Password:{password}".format(otc=otc, password=password))
