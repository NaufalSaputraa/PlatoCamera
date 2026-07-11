import struct

img = r'D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted\product_a.img'
f = open(img, 'rb')

# Check EROFS magic at offset 1024
f.seek(1024)
magic = f.read(4)
print(f'Magic at 1024: {magic.hex()} = {magic!r}')

# Check ext4 superblock magic at offset 0x438
f.seek(0x438)
ext4_magic = f.read(2)
print(f'ext4 magic at 0x438: {ext4_magic.hex()} (53ef = ext4)')

# EROFS magic is E2E1F5E0
erofs_magic = bytes.fromhex('e0f5e1e2')
print(f'Is EROFS: {magic == erofs_magic}')

# Also check first 4 bytes
f.seek(0)
first = f.read(16)
print(f'First 16 bytes: {first.hex()}')

f.close()
