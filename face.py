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


def verify_face(login: str):
   # there we can find registered user's photo 
    # try:
        img2_path = f'db/{login}/img.png'
        img1_path = f'tmp/{login}/img.png'

        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
        logger.info(f'Successfully added photo of user {login}')
        return result['result']
    # except:
        logger.error('User has not been registered yet')

    # return False


if __name__ == '__main__':
    result = DeepFace.verify(img1_path='db/Linas/img.png', img2_path='tmp/Linas/img.png')
    logger.info('Successfully verified user')
    print(result)
    
