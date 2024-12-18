from deepface import DeepFace
import logging

 # set level of logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('logfile.log')
handler.setLevel(logging.DEBUG)

# set format of logs
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def verify_face(login: str, img_path: str) -> bool:
       # there we can find registered user's photo 
    try:
        img2_path = f'db/{login}/img.png'
        result = DeepFace.verify(img1_path=img_path, img2_path=img2_path)
        return result['result']
        logger.info(f'Successfully added photo of user {login}')
    except:
        logger.error('User has not been registered yet')

    return False


if __name__ == '__main__':
    result = DeepFace.verify(img1_path='db/admin/img1.png', img2_path='db/admin/img2.png')
    logger.info('Successfully verified user')
    print(result)
    
