import socket, ssl, json, struct
import binascii

def Payload(alert='', badge=1, data={}):
     payload = {
        'aps': {
            'alert':alert,
            'sound':'k1DiveAlarm.caf',
            'badge':badge,
         },
        'acme': data,
     }
     return payload

def APN(token, payload, theCertfile):
    theHost = ( 'gateway.sandbox.push.apple.com', 2195 )
    # Create our connection using the certfile saved locally
    ssl_sock = ssl.wrap_socket(
            socket.socket( socket.AF_INET, socket.SOCK_STREAM ),
            certfile = theCertfile
        )
    ssl_sock.connect( theHost )

    # Write out our data
    for x in xrange(1,150):
        payload['aps']['alert'] = str(x)
        data = json.dumps( payload )
        # Clear out spaces in the device token and convert to hex
        deviceToken = token.replace(' ','').decode('hex')
        byteToken = binascii.unhexlify(token)
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )
        print x
        ssl_sock.write( theNotification )

    # Close the connection -- apple would prefer that we keep
    # a connection open and push data as needed.
    ssl_sock.close()

    return True