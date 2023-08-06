import secrets
from pathlib import Path

import pendulum

# from easy_pay.settings import time_zone, order_time_expire
# from easy_pay.wechat_pay import WechatPay
from easy_pay.settings import time_zone, order_time_expire
from easy_pay.wechat_pay import WechatPay

key = Path('test/apiclient_key.pem').read_text('utf8')
w = WechatPay(
    private_key=key, mch_id='1521083381',
    serial_no='615B92F0E84F431E00CBBFCEECB08EC84131B875',
    app_id='wx6ef7309c498abf29',
    app_secret="a05f23808233b5d09d0b0c82c522189d",
    v3_api_key="31eaf5d31eab60c92280b223822b68c8"
)

now = pendulum.now(tz=time_zone)


def test_get_cert():
    cert_url = "https://api.mch.weixin.qq.com/v3/certificates"
    r = w.request(method='GET', url=cert_url)
    assert r.status_code == 200


def test_pc_native():
    trade_order = secrets.token_hex(16)

    native_data = {
        "appid": w.app_id,
        "mchid": w.mch_id,
        "description": 'Image',
        "out_trade_no": trade_order,
        "time_expire": f"{now.add(seconds=order_time_expire)}",
        "notify_url": 'https://www.baidu.com',
        "amount": {
            "total": 1,
            "currency": "CNY"
        }
    }
    native_url = "https://api.mch.weixin.qq.com/v3/pay/transactions/native"
    r = w.request(method='POST', url=native_url, data=native_data)
    assert r.status_code == 200
    print(r.json())


def test_generate_qr_code():
    trade_order = secrets.token_hex(16)
    p = Path(f"{now.int_timestamp}.png")
    w.build_native_qr_code(
        description="中文 body", trade_no=trade_order, notice_url='https://www.baidu.com',
        price=1, path=p
    )


def test_get_prepay_id():
    trade_order = secrets.token_hex(16)
    r = w.build_jsapi_prepay(
        description="中文 body", trade_no=trade_order, notice_url='https://www.baidu.com',
        price=1, openid="ovwDJjj_g98G9X9-2KynNznEHmeM"
    )
    print(r)


def test_query_order():
    trade_order = secrets.token_hex(16)
    r = w.query_order(
        transaction_id=trade_order
    )
    print(r)


def test_get_openid():
    code = "081Vzo000hD6ZK1PFI000MISZS1Vzo0S"
    r = w.request_wx_openid(code=code)
    print(r)


def test_decrypt_wx_notice():
    data = {'id': 'b616f5b1-a35e-54ed-8066-aa701461b3bd', 'create_time': '2021-01-18T14:09:53+08:00',
            'resource_type': 'encrypt-resource', 'event_type': 'TRANSACTION.SUCCESS', 'summary': '支付成功',
            'resource':
                {'original_type': 'transaction', 'algorithm': 'AEAD_AES_256_GCM',
                 'ciphertext': 'Y4jspeMkO3JADx2oEexPCa496jLba/bkg4cfN0vEaAWtLZ+qih95m+gZM/'
                               'BKZIKUO4k6V50UWiQWhKUu1qWP4s+zngkGKnju+omobwPsVrVmCcClCa4v10+'
                               'YsM2DYcVArLdMwwzeleTAMoZgEtNO0tvGxhpzBit306Ol4eKDw3SJ7NzyjFWQ'
                               'mbU0x0QH6HGm8gGRvBAjLjFlzC9sVbdnVmdSjullAJ0joLcL351AO3tQ7AIyr'
                               'ISLLW7SGGADoG0xPfN+AL4M3FBkrOCjn9VzAq68np6d1M346Hxw/uaeBxn5Sf'
                               '6KlVVUdUx+f8oLJ8GQW86yx/PqIz5X8HHrVUkR7dtFenxwT+LCIE5bqei4J0Y'
                               'xbnc6/Q42/6pnAPHlB/z6xbqXKRkmXmr/Jpo5aOERX2OMCq3pOyBlhrp1lbnj'
                               'Izbvj1dZDG4O/YrX87yYOuo0AEGTHjGwFyM+5j/67DwW2Oo0Ho9PWQQtACFm5'
                               'REdi/UG6oymhJvvV++Br2pr6oX9sRfqBUkHVYKTOHWoyiIVqww/a8QD/U6CFh'
                               '58zpScfVe2dsI9sHXKlwU3A3DvJpf4N5FtIC2hCn7CJQ==',
                 'associated_data': 'transaction',
                 'nonce': 'HV7zFyLR6VHQ'}
            }
    r = data['resource']
    r = w.decode_notice(r)
