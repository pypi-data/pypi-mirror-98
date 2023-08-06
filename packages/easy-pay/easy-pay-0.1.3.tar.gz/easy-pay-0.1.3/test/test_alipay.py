import pendulum

from easy_pay.ali_pay import Alipay

ALIPAY_APP_ID = "2021001161640064"
ALIPAY_PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvTUv2EdrEiSyQE2859f9DbT0rkyS6LldnF39mLq1kVgFN+MkvW5upLHua9ortLOZvL/q1n3FYOxfH8dC2jF/qbxQx7RmjZF4EQadUhUi1j32axxs9Yn8oyBlorZXX0FhcXdQRsbtE36PS5mbtgvK8l9hfPc1jYO6RWwvFM1dMjwBAnqMeOthTvBq2WzaGUGETyWnOvNCtSk+rPQxbWyrWbw2hf4Z9zhPGj1w1iCnzHAfyb6jj/jdYT+lwXl526JAgCLnvguZpR26I5BREzN03q0D0MruwXNj3SnkM4S9G7ZzgqNDtVEPe8RZ/Mig8Q3yF6khsmsTHMKwgkCmT91p/wIDAQAB"
ALIPAY_APP_PRIVATE_KEY = "MIIEowIBAAKCAQEAhdLrWgw773ng2Lt103r7IvU5tTKrSHA2p150GYTsdlNxj3i2uUNfdg8kZX03X1Ta6gDgJY467NiBjJes04H7ARrBGAB/xbimaXP2ON0beuQOvLSSB5uV8QwLZwNFzFW0V0Nzz2Vx4vDCVru/G8MRR02MbQ3BeVC3ilMW1YI2alO1kfgzUVAsOhGC6ZQo3reO78vA+HtAK/HZrUegiBcyzPhcqDGqGsa/+EEm2gLanmF4qXNX7PI1VR9AVBZE3670SyZ7z+8TpL0kOkEiB6RxZhMX2KjfJUzuph4JFLrc9qiXyaLc3dxQyxWPoX0MNet6NlIovTGPWFegue4xCtZwZQIDAQABAoIBAGdL7oTcaqsoHanN0V5DUHSkaz31dYb9rwI0A1PraYbQVBjVqd2JJrd/aq24ILTCUBRORrZWeh9141G9hhbg/vnUR/YZ9IaPSEyfyRANg/ew77szeoDK1Mtya57BRPA7u2+cTllpSaZOBwRh+VsZkE3Eiz9mXdAhwPrRtg9qakxZWQ5hnlg3yfMZUM2vr1x0u3VKzzVz4wiBBsI2+D80/O2v2rk1KNc2Hj23Fx6K0IGNzs9XV30nTjytuKa8Pp4vEeqC+cqBMQVH6QMFX1Blo+Y6xBldFQbs3orYoVDGGHWMG7wNCuCGFD/3cU5bX9rKNh6v1kdCINQO86MGVLhVwwECgYEA60NznbMetTbPJ41fuCeTx0D3LcBzMBSy7IRIbnCKoPLUy6aTIZwVKlbwnQBwPgkf//XbotLz/BAl8KhMXWvsUloolomceZVzVvMRuQmldh4yE24mTf/A+XnfrBxVwJbWZGHtncZq/739bnp1bt/JT1bswlbOrIpJJnxF4NuhbEECgYEAkZ6OzZvvfoSloYUpq86itxbRrYmko9um6kTypzfqWhS8kPH+Jc/BINpTVS+rOJbITxzkf2av9GUX+L41sqsHTzAMGWGS8xfkQnoBuful7H/cY+S+GQdLh2uTdMX0OR19NPAKl/kPIIzcSWKZfCiNar92yIY3Hx22GdY1hnIbCyUCgYBJC3xOLlsOcKII6cAacU9Uwjr8nZAmEYcsIDZM8+xW5I5lXKa5/LglmTDDzmsLF9IzqqYy+8R9MpZVDiwHpYaOWyfW9Yr7xQc2q+mIxhH1hpKNrdl+xjWoP8rOqU2Gqk6OhEk+f2ihVt/k+WiUsC7Uz2xbOpCYyabEqDkaA5cvAQKBgFv9l2bqQGRjdaLQ1Z9UfVQ+VR1U264r34kVH1llqGVZvjmutge6891GLuicoYSxND9OGEcnXrZ8eqVHu/JvusFar/oEuulYyXj5TEfqYkpCB78PTMvQ4PTej5twRjUinOspTPfufZDpi2vMnvthPt0VsPtCVmYQxe4SdWPGh7EFAoGBAIp/a4rB8skTYkssgJT40IcwnFYzJpZj0wRDjQyVGeCQWqQeKxV2k48eqhlfCIB0T23SjPNpbXey1osyS1XXqh7dJO3l/nEIyfcjzzdHUr7g7q5fg1zS5/8+Nxs0ax5zHoG27MR8ARmMvipHZNPZ3b6sl3HHU+RLZO4y6z+DMdRY"

alipay = Alipay(
    is_sandbox=False,
    app_id=ALIPAY_APP_ID,
    alipay_public_key=ALIPAY_PUBLIC_KEY,
    app_private_key=ALIPAY_APP_PRIVATE_KEY
)
now = pendulum.now()


def test_page_pay():
    r = alipay.page_pay(
        subject='糖果',
        price=1,
        trade_no=f"{now}",
        return_url='https://www.baidu.com',
        # notice_url='https://www.baidu.com',
        describe='好吃的糖果',
    )
    print(r)


def test_wap_pay():
    r = alipay.wap_pay(
        subject='糖果',
        price=1,
        trade_no=f"{now}",
        return_url='https://www.baidu.com',
        # notice_url='https://www.baidu.com',
        describe='好吃的糖果',
        quit_url='https://www.baidu.com'
    )
    print(r)


def test_pay():
    for m in ('page', 'wap'):
        r = alipay.pay(
            method=m,
            subject='糖果',
            price=1,
            trade_no=f"{now}",
            return_url='https://www.baidu.com',
            # notice_url='https://www.baidu.com',
            describe='好吃的糖果',
            quit_url='https://ydassess.com'
        )
        print(r)
