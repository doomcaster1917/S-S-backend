# import jwt
# from datetime import datetime, timedelta
# import time
#
# orig_iat = datetime.utcnow() - timedelta(hours=1)
# dt = datetime.now() + timedelta(days=1)
# print(dt)
# jwt_payload = jwt.encode({'id': 1, "exp": dt},
#     'django-insecure-kf2rz&=s_-zbat%hl+n_^4_5ek5g=0ts^w-m5@$cp0ia(l1qpl', algorithm='HS256')
#
# time.sleep(3)
#
# # JWT payload is now expired
# # But with some leeway, it will still validate
# decode = jwt.decode(jwt_payload, 'django-insecure-kf2rz&=s_-zbat%hl+n_^4_5ek5g=0ts^w-m5@$cp0ia(l1qpl',  algorithms=["HS256"])
# print(decode)

xs = [4, 6, 2, 4].remove(6)
print(xs)