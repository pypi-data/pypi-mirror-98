import os
from email import message_from_bytes
from textwrap import wrap

import extract_msg

from asn1crypto import cms


def parse_mail(data: bytes, name='smime.p7m'):
    file_name, file_extension = os.path.splitext(name)
    if file_extension == '.msg':
        print('msg...')
        return parse_mail_msg(data)
    else:
        print('any...')
        return parse_mail_any(data)


def parse_mail_any(data: bytes):
    message = message_from_bytes(data)

    payload = b''
    for part in message.walk():
        if part.get_content_type() in ['application/pkcs7-mime'] and part.get_param('smime-type') == 'enveloped-data':
            payload = part.get_payload(decode=True)
            break

    return parse_pkcs7(payload)


def parse_mail_msg(data: bytes):
    message = extract_msg.openMsg(data)

    payload = b''
    for attachment in message.attachments:
        # print(attachment)
        if attachment.longFilename == 'smime.p7m':
            payload = attachment.data
            break

    return parse_pkcs7(payload)


def parse_pkcs7(payload: bytes):
    try:
        content_info = cms.ContentInfo.load(payload)
    except ValueError:  # ToDO(frennkie) silently fail
        return []

    enveloped_data = content_info['content']  # same as enveloped_data = content_info[1]

    recipient_infos = enveloped_data.native.get('recipient_infos')

    result = []
    for ri in recipient_infos:
        assert ri['version'] in ['v0', 'v2']  # failing hard here

        if ri['version'] == 'v0':
            rid = ri['rid']
            # print(rid['issuer'])
            # print(rid['serial_number'])
            # print(rid['issuer'])

            sn = ":".join(wrap(hex(rid['serial_number']).split('x')[1], 2))
            result.append({'issuer': rid['issuer'], 'serial': sn})

        else:
            raise NotImplementedError()  # also failing hard here

    return result
