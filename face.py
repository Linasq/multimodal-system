from deepface import DeepFace


def verify_face(login: str, img1_path: str) -> bool:
    # there we can find registered user's photo 
    try:
        img2_path = f'db/{login}/img.png'
        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
        return result['result']
    except:
        print('User has not registered yet')

    return False


#TODO check how to send file through function or register user in main function
def register_user_face(login: str):
    pass


if __name__ == '__main__':
    result = DeepFace.verify(img1_path='db/admin/img1.png', img2_path='db/admin/img2.png')

