import zlib

def compress_string(compressable_string):
    byte_string = bytes(compressable_string,'utf-8')
    compressed_string = zlib.compress(byte_string, 9)
    string_bytes = str(compressed_string)
    string_bytes_org = str(compressable_string)
    print('String ' + string_bytes_org + ' has been compressed to ' + string_bytes)
    
    return (compressed_string)


def decompress_string(compressed_string):
    decompressed_bytes = zlib.decompress(compressed_string)
    decompressed_string = str(decompressed_bytes)
    print(decompressed_string)


def compress_object(compressable_object):
    compressed_object = zlib.compressobj(9, compressable_object)



def decompress_object(compressed_object):
    decompressed_object = zlib.decompressobj(compressed_object)

compressable_string = "This is a test string"

compressable_object = ['hi', 'stop', 'test']

compressed_string = compress_string(compressable_string)
decompress_string(compressed_string)

compressed_object = compress_object(compressable_object)

