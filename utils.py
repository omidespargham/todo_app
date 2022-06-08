# from kavenegar import *
# def send_rgs_code(phone_number,code):
#     try:
#         api = KavenegarAPI("6E586E67554B61664D6B324C6A4E373246636D7048555973536F423630517A326962474B6D30706455454D3D")
#         params = { 
#             'sender' : '', 
#             'receptor': phone_number,  
#             'message' :f'{str(code)}کد تایید شما' 
#             }
#         response = api.sms_send(params)
#         print(response)
#     except APIException as e: 
#         print(e)
#     except HTTPException as e:
#         print(e)