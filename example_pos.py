

if __name__ == "__main__":
    from src.wom_connector.pointofsale import POS
    from src.wom_connector.filter import Filter


    pubk = open("keys/registry.pub", "rb")
    privk = open("keys/pos1.pem", "rb")

    filter = Filter.create(aim='H', left_top_bound=[46.0, -17.0], right_bottom_bound=[12.0, 160.0], max_age=14)

    pos = POS(base_url='http://dev.wom.social/api/v1',  # this will be 'http://wom.social/api/v1'
              pos_id=1,  # instrument ID
              registry_pubk=pubk.read(),
              pos_privk=privk.read())

    otc, password = pos.request_payment(amount=100,
                                        pocket_ack_url='http://google.it',
                                        filter=filter,
                                        pos_ack_url='http://libero.it',
                                        persistent=False,
                                        nonce=None,
                                        password=None)

    print("Otc: {otc} Password:{password}".format(otc=otc, password=password))
