# django_rest_apis with swagger documentation

I'm sharing with you the postman api collection


https://api.postman.com/collections/31238669-dae97e70-7828-4def-a9d6-9f657f1f32e1?access_key=PMAT-01HKDH7ZH232W9F84RHR4AB0AE

open postman click on import button and then paste above key there

i make for you signup,signin,reset password (means you hit this api you enter email of your token send to your email with confirm reset api endpoint)
note im using smtp service for sending token to email but when i go to sendgrid to make testing for the test it does not allow to login me so i check properly you just need to go to settings.py file and just replace 
EMAIL_HOST_USER = 'user you make of any smtp service'
EMAIL_HOST_PASSWORD = 'password of your smtp account'
after this reset password work properly
your requirements fullfilled when you check postman collection
