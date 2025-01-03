from deepface import DeepFace
import logging
from sklearn.metrics.pairwise import cosine_distances
import json
import numpy as np

 # set level of logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('logfile.log')
handler.setLevel(logging.DEBUG)

# set format of logs
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def save_embedding(login: str, is_login: bool):
    if is_login:
        img_path = f'tmp/{login}/img.png'
    else:
        img_path = f'db/{login}/img.png'

    result = DeepFace.represent(img_path=img_path)
    logger.info(f'Created embedding of user {login}')
    return result


def verify_face(login: str):
    try:
        img2_path = f'db/{login}/img.png'
        img1_path = f'tmp/{login}/img.png'

        # result = cosine_similarity()
        logger.info(f'Successfully calculated cosine similarity of user {login}')
        # return result['result']
    except:
        logger.error('User has not been registered yet')

    return False


if __name__ == '__main__':
    emb1 = DeepFace.represent('db/Linas/img.png')
    emb2 = DeepFace.represent('tmp/Linas/img.png')

    with open('db/Linas/test_emb.txt', 'w') as f:
        f.write(str(emb1[0]))

    with open('tmp/Linas/test_emb.txt', 'w') as f:
        f.write(str(emb2[0]))

    with open('db/Linas/test_emb.txt', 'r') as f:
        test1 = f.read()
        test1 = test1.replace("'", '"')
        test1 = test1.replace('None', '"None"')

    with open('tmp/Linas/test_emb.txt', 'r') as f:
        test2 = f.read()
        test2 = test2.replace("'", '"')
        test2 = test2.replace('None', '"None"')

    test1 = json.loads(test1)
    test1 = test1['embedding']
    test1 = np.array(test1)

    test2 = json.loads(test2)
    test2 = test2['embedding']
    test2 = np.array(test2)

    dot_product = np.dot(test1, test2)
    source_norm = np.linalg.norm(test1)
    test_norm = np.linalg.norm(test2)
    distances = 1 - dot_product / (source_norm * test_norm)

    print(distances)
    
