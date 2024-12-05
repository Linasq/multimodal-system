from deepface import DeepFace

result = DeepFace.verify(img1_path='db/admin/img3.png', img2_path='db/bill.png')#, model_name='Facenet512')
print(result)

#TODO

'''
create function that returns:
    - true if person matches
    - false if not

create function that saves images of registered users
'''
