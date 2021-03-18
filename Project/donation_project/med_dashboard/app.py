import os
import random
import re
import string

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import json

from db_connect import *
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'files-directory'
ALLOWED_EXTENSIONS_PHOTO = ['png', 'jpg', 'jpeg', 'bmp', 'jfif', 'jpe']
ALLOWED_EXTENSIONS_VIDEO = ['flv', 'mp4', 'm3u8', 'ts', '3gp', 'mov', 'avi', 'wmv']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PHOTO


def create_json(datas):
    data_json = json.dumps(datas, sort_keys=True, indent=4)
    return data_json


def get_current_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


@app.route('/partial-identification', methods=['GET'])
def anketa():
    token = request.values['token']
    customerId = request.values['customerId']
    is_used = db_query_select(f"select is_used from tokens_identification where token = '{token}' ")
    is_used = is_used[0][0]
    # is_used = False

    if is_used == False:
        db_query_update_approved(f"update tokens_identification set is_used = True where token = '{token}'")
        return render_template(
            'anketaPid.html', customerId=customerId, token=token
        )
    if is_used == True:
        return render_template(
            'used_token_page.html'
        )


@app.route('/full-identification')
def full_id():
    return render_template(
        'anketaFull.html'
    )


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        token = request.form['token']
        is_uploaded = db_query_select(f"select is_uploaded from tokens_identification where token = '{token}' ")

        if is_uploaded is not None:
            is_uploaded = is_uploaded[0][0]
        else:
            return render_template('used_token_page.html')

        if is_uploaded == False:

            print(request.form)
            datas = {
                'customerId': '',
                'type': 'partial',
                'iin': '',
                'photo-path': '',
                'video-path': '',
                'doc-front': '',
                'doc-back': ''

            }
            iin = request.form['iin']
            datas['iin'] = re.sub('/D', '', iin)

            custId = request.form['customerId']
            datas['customerId'] = custId

            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], iin)):
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], iin))

            uploadiin = os.path.join(app.config['UPLOAD_FOLDER'], iin)

            photo = request.files['photo']
            if not photo:
                pass
            else:
                extension = os.path.splitext(photo.filename)[1]
                photo.filename = iin + '-photo' + extension
                datas['photo-path'] = os.path.join(uploadiin, secure_filename(photo.filename))
                photo.save(os.path.join(uploadiin, secure_filename(photo.filename)))

            video = request.files['video']
            if not video:
                pass
            else:
                extension = os.path.splitext(video.filename)[1]
                video.filename = iin + '-video' + extension
                datas['video-path'] = os.path.join(uploadiin, secure_filename(video.filename))
                video.save(os.path.join(uploadiin, secure_filename(video.filename)))

            doc_front = request.files['doc-front']
            if not doc_front:
                pass
            else:
                extension = os.path.splitext(doc_front.filename)[1]
                doc_front.filename = iin + '-docfront' + extension
                datas['doc-front'] = os.path.join(uploadiin, secure_filename(doc_front.filename))
                doc_front.save(os.path.join(uploadiin, secure_filename(doc_front.filename)))

            doc_back = request.files['doc-back']
            if not doc_back:
                pass
            else:
                extension = os.path.splitext(doc_back.filename)[1]
                doc_back.filename = iin + '-docback' + extension
                datas['doc-back'] = os.path.join(uploadiin, secure_filename(doc_back.filename))
                doc_back.save(os.path.join(uploadiin, secure_filename(doc_back.filename)))

            json_data = create_json(datas)
            created_at = get_current_time()
            db_query_insert('INSERT INTO partial_identification(info, created_at, is_approved) values(%s, %s, %s)',
                            (json_data, created_at, False))

            db_query_update_approved(f"update tokens_identification set is_uploaded = True where token = '{token}'")

            return render_template(
                'saved_success.html'
            )

        else:
            return render_template('used_token_page.html')

@app.route('/upload-full', methods=['POST', 'GET'])
def upload_full():
    if request.method == 'POST':
        print(request.form)
        print('asdfasdf')
        datas = {
            'type': 'full',
            'iin': '',
            'place-of-birth': request.form.get('place-of-birth'),
            'nationality': request.form.get('nationality'),
            'bday': request.form.get('bday'),
            'photo-path': '',
            'video-path': '',
            'doc-path': '',
            'financial': {
                'other-jur-compane': request.form.get('other-jur-compane'),
                'inostr-nalog-residency': request.form.get('inostr-nalog-residency'),
                'country-nalog-residency': request.form.get('country-nalog-residency'),
                'number-nalog-residency': request.form.get('number-nalog-residency'),
                'jur-dohod': request.form.get('jur-dohod'),
                'jur-dohod-description': request.form.get('jur-dohod-description'),
                'postoyanniy-work': request.form.get('postoyanniy-work'),
                'postoyanniy-work-name': request.form.get('postoyanniy-work-name'),
                'postoyanniy-work-position': request.form.get('postoyanniy-work-position'),
                'own-business': request.form.get('own-business'),
                'own-business-name': request.form.get('own-business-name'),
                'own-business-type': request.form.get('own-business-type'),
                'dividents': request.form.get('dividents'),
                'dividents-name': request.form.get('dividents-name'),
                'other-work': request.form.get('other-work'),
                'other-work-name': request.form.get('other-work'),
                'other-banks': request.form.get('other-banks'),
                'bank-name': request.form.get('bank-name'),
                'bank-code': request.form.get('bank-code'),
                'bank-account': request.form.get('bank-account'),
                'wallet-description': request.form.get('wallet-description')

            },
            'document': {
                'udost': request.form.get('udost'),
                'doc-num': request.form.get('doc-num'),
                'date-established': request.form.get('date-established'),
                'date-end': request.form.get('date-end'),
                'established': request.form.get('established')
            },
            'register-address': {
                'country': request.form.get('country'),
                'province': request.form.get('province'),
                'raion': request.form.get('raion'),
                'naselenniy': request.form.get('naselenniy'),
                'street': request.form.get('street'),
                'house-num': request.form.get('house-num'),
                'flat-num': request.form.get('flat-num')
            },
            'fact-address': {
                'fact-country': request.form.get('fact-country'),
                'fact-province': request.form.get('fact-province'),
                'fact-raion': request.form.get('fact-raion'),
                'fact-naselenniy': request.form.get('fact-naselenniy'),
                'fact-street': request.form.get('fact-street'),
                'fact-house-num': request.form.get('fact-house-num'),
                'fact-flat-num': request.form.get('fact-flat-num')
            },
            'KYC': {
                'inostr-public-personal': request.form.get('inostr-public-personal'),
                'inostr-public-relatives': request.form.get('inostr-public-relatives'),
                'usa-nalog': request.form.get('usa-nalog'),
                'usa-staying': request.form.get('usa-staying'),
                'usa-registration': request.form.get('usa-registration'),
                'usa-business': request.form.get('usa-business'),
                'usa-parents': request.form.get('usa-parents'),
                'usa-greencard': request.form.get('usa-greencard'),
                'usa-trustedperson': request.form.get('usa-trustedperson'),
                'usa-nalogcode': request.form.get('usa-nalogcode'),
                'usa-description': request.form.get('usa-description')
            }
        }
        print('reqasjdf')
        iin = request.form['iin']

        datas['iin'] = iin
        print(datas)
        try:
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], iin))
        except FileExistsError:
            pass
        uploadiin = os.path.join(app.config['UPLOAD_FOLDER'], iin)
        photo = request.files['photo']
        if not photo:
            pass
        else:
            extension = os.path.splitext(photo.filename)[1]
            photo.filename = iin + '-photo' + extension
            datas['photo-path'] = os.path.join(uploadiin, secure_filename(photo.filename))
            photo.save(os.path.join(uploadiin, secure_filename(photo.filename)))

        video = request.files['video']
        if not video:
            pass
        else:
            extension = os.path.splitext(video.filename)[1]
            video.filename = iin + '-video' + extension
            datas['video-path'] = os.path.join(uploadiin, secure_filename(video.filename))
            video.save(os.path.join(uploadiin, secure_filename(video.filename)))

        json_data = create_json(datas)
        created_at = get_current_time()
        db_query_insert('INSERT INTO full_identification(info, created_at, is_approved) values(%s, %s, %s)',
                        (json_data, created_at, False))

        return render_template(
            'saved_success.html'
        )


@app.route('/upload-full-from-partial', methods=['GET', 'POST'])
def upload_full_partial():
    if request.method == 'POST':
        print(request.form)

        datas = {
            'type': 'full',
            'iin': '',
            'photo-path': '',
            'video-path': '',
            'financial': {
                'other-jur-compane': ''
            },
            'KYC': {
                'inostr-public-personal': '',
                'inostr-public-relatives': '',
                'usa-nalog': '',
                'usa-staying': '',
                'usa-registration': '',
                'usa-business': '',
                'usa-parents': '',
                'usa-greencard': '',
                'usa-trustedperson': '',
                'usa-nalogcode': '',
                'usa-description': ''
            }

        }

        return render_template(
            'saved_success.html'
        )


@app.route('/request/tkns', methods=['POST'])
def request_tkns():
    secret = request.form['secret']
    base_secret = "eKIwf;K;Eo~wrom"
    if secret[0] == '"':
        secret = secret[1:-1]
    if secret == base_secret:
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

        token = ''.join(random.choice(chars) for _ in range(64))
        created_at = get_current_time()
        db_query_insert('insert into tokens_identification(token, created_at, is_used, is_uploaded) values (%s, %s, %s, %s)',
                        (token, created_at, False, False))

        message = {
            'token': token
        }

        return jsonify(message), 200
    else:
        return jsonify({'token': None, 'comment': 'failed secret check'}, 200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False, port=5000)
