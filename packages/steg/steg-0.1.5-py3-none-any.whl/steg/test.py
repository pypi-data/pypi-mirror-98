import steg_img

s = steg_img.IMG(payload_path='./test_data/payload.txt', image_path='./test_data/pug.png')
s.hide()

s_prime = steg_img.IMG(image_path='./new.png')
s_prime.extract()