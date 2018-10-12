
from PIL import Image
from io import BytesIO
import colorsys

from fs_helpers import *

class TooManyColorsError(Exception):
  pass

BLOCK_WIDTHS = {
    0: 8,
    1: 8,
    2: 8,
    3: 4,
    4: 4,
    5: 4,
    6: 4,
    8: 8,
    9: 8,
  0xA: 4,
  0xE: 8,
}
BLOCK_HEIGHTS = {
    0: 8,
    1: 4,
    2: 4,
    3: 4,
    4: 4,
    5: 4,
    6: 4,
    8: 8,
    9: 4,
  0xA: 4,
  0xE: 8,
}
BLOCK_DATA_SIZES = {
    0: 32,
    1: 32,
    2: 32,
    3: 32,
    4: 32,
    5: 32,
    6: 64,
    8: 32,
    9: 32,
  0xA: 32,
  0xE: 32,
}

IMAGE_FORMATS_THAT_USE_PALETTES = [8, 9, 0xA]

MAX_COLORS_FOR_IMAGE_FORMAT = {
  0x8: 1<<4, # C4
  0x9: 1<<8, # C8
  0xA: 1<<14, # C14X2
}



def get_rgba(color):
  if len(color) == 4:
    r, g, b, a = color
  else:
    r, g, b = color
    a = 0xFF
  return (r, g, b, a)
 
def convert_rgb565_to_color(rgb565):
  r = ((rgb565 >> 11) & 0x1F)
  g = ((rgb565 >> 5) & 0x3F)
  b = ((rgb565 >> 0) & 0x1F)
  r = r*255//0x1F
  g = g*255//0x3F
  b = b*255//0x1F
  return (r, g, b, 255)

def convert_color_to_rgb565(color):
  r, g, b, a = get_rgba(color)
  r = r >> 3
  g = g >> 2
  b = b >> 3
  rgb565 = 0x0000
  rgb565 |= ((r & 0x1F) << 11)
  rgb565 |= ((g & 0x3F) << 5)
  rgb565 |= ((b & 0x1F) << 0)
  return rgb565

def convert_rgb5a3_to_color(rgb5a3):
  # RGB5A3 format.
  # Each color takes up two bytes.
  # Format depends on the most significant bit. Two possible formats:
  # Top bit is 0: 0AAARRRRGGGGBBBB
  # Top bit is 1: 1RRRRRGGGGGBBBBB (Alpha set to 0xff)
  if (rgb5a3 & 0x8000) == 0:
    a = ((rgb5a3 >> 12) & 0x7)
    r = ((rgb5a3 >> 8) & 0xF)
    g = ((rgb5a3 >> 4) & 0xF)
    b = ((rgb5a3 >> 0) & 0xF)
    a = a*255//7
    r = r*255//0xF
    g = g*255//0xF
    b = b*255//0xF
  else:
    a = 255
    r = ((rgb5a3 >> 10) & 0x1F)
    g = ((rgb5a3 >> 5) & 0x1F)
    b = ((rgb5a3 >> 0) & 0x1F)
    r = r*255//0x1F
    g = g*255//0x1F
    b = b*255//0x1F
  return (r, g, b, a)

def convert_color_to_rgb5a3(color):
  r, g, b, a = get_rgba(color)
  if a != 255:
    a = a >> 5
    r = r >> 4
    g = g >> 4
    b = b >> 4
    rgb5a3 = 0x0000
    rgb5a3 |= ((a & 0x7) << 12)
    rgb5a3 |= ((r & 0xF) << 8)
    rgb5a3 |= ((g & 0xF) << 4)
    rgb5a3 |= ((b & 0xF) << 0)
  else:
    r = r >> 3
    g = g >> 3
    b = b >> 3
    rgb5a3 = 0x8000
    rgb5a3 |= ((r & 0x1F) << 10)
    rgb5a3 |= ((g & 0x1F) << 5)
    rgb5a3 |= ((b & 0x1F) << 0)
  return rgb5a3

def convert_ia4_to_color(ia4):
  low_nibble = ia4 & 0xF
  high_nibble = (ia4 >> 4) & 0xF
  
  r = g = b = low_nibble*0x11
  a = high_nibble*0x11
  
  return (r, g, b, a)

def convert_ia8_to_color(ia8):
  low_byte = ia8 & 0xFF
  high_byte = (ia8 >> 8) & 0xFF
  
  r = g = b = low_byte
  a = high_byte
  
  return (r, g, b, a)

def convert_color_to_ia8(color):
  r, g, b, a = get_rgba(color)
  assert r == g == b
  ia8 = 0x0000
  ia8 |= (r & 0xFF)
  ia8 |= ((a & 0xFF) << 8)
  return ia8

def convert_i4_to_color(i4):
  r = g = b = i4*0x11
  a = 255
  
  return (r, g, b, a)

def convert_i8_to_color(i8):
  r = g = b = i8
  a = 255
  
  return (r, g, b, a)

def get_interpolated_cmpr_colors(color_0_rgb565, color_1_rgb565):
  color_0 = convert_rgb565_to_color(color_0_rgb565)
  color_1 = convert_rgb565_to_color(color_1_rgb565)
  r0, g0, b0, _ = color_0
  r1, g1, b1, _ = color_1
  if color_0_rgb565 > color_1_rgb565:
    color_2 = (
      (2*r0 + 1*r1)//3,
      (2*g0 + 1*g1)//3,
      (2*b0 + 1*b1)//3,
      255
    )
    color_3 = (
      (1*r0 + 2*r1)//3,
      (1*g0 + 2*g1)//3,
      (1*b0 + 2*b1)//3,
      255
    )
  else:
    color_2 = (r0//2+r1//2, g0//2+g1//2, b0//2+b1//2, 255)
    color_3 = (0, 0, 0, 0)
  colors = [color_0, color_1, color_2, color_3]
  return colors

def get_best_cmpr_key_colors(all_colors):
  max_dist = -1
  color_1 = None
  color_2 = None
  for i in range(len(all_colors)):
    curr_color_1 = all_colors[i]
    for j in range(i+1, len(all_colors)):
      curr_color_2 = all_colors[j]
      curr_dist = get_color_distance_fast(curr_color_1, curr_color_2)
      if curr_dist > max_dist:
        max_dist = curr_dist
        color_1 = curr_color_1
        color_2 = curr_color_2
  
  if max_dist == -1:
    return ((0, 0, 0, 0xFF), (0xFF, 0xFF, 0xFF, 0xFF))
  else:
    r1, g1, b1, a1 = color_1
    color_1 = (r1, g1, b1, 0xFF)
    r2, g2, b2, a2 = color_2
    color_2 = (r2, g2, b2, 0xFF)
    
    if (r1 >> 3) == (r2 >> 3) and (g1 >> 2) == (g2 >> 2) and (b1 >> 3) == (b2 >> 3):
      if (r1 >> 3) == 0 and (g1 >> 2) == 0 and (b1 >> 3) == 0:
        color_2 = (0xFF, 0xFF, 0xFF, 0xFF)
      else:
        color_2 = (0, 0, 0, 0xFF)
    
    return (color_1, color_2)

# Picks a color from a palette that is visually the closest to the given color.
# Based off Aseprite's code: https://github.com/aseprite/aseprite/blob/cc7bde6cd1d9ab74c31ccfa1bf41a000150a1fb2/src/doc/palette.cpp#L226-L272
def get_nearest_color_slow(color, palette):
  if color in palette:
    return color
  
  r, g, b, a = get_rgba(color)
  
  if a == 0: # Transparent
    for indexed_color in palette:
      if len(indexed_color) == 4 and indexed_color[3] == 0:
        return indexed_color
  
  min_dist = 9999999999.0
  value = None
  
  col_diff_g = []
  col_diff_r = []
  col_diff_b = []
  col_diff_a = []
  for i in range(128):
    col_diff_g.append(0)
    col_diff_r.append(0)
    col_diff_b.append(0)
    col_diff_a.append(0)
  for i in range(1, 63+1):
    k = i*i
    col_diff_g[i] = col_diff_g[128-i] = k * 59 * 59
    col_diff_r[i] = col_diff_r[128-i] = k * 30 * 30
    col_diff_b[i] = col_diff_b[128-i] = k * 11 * 11
    col_diff_a[i] = col_diff_a[128-i] = k * 8 * 8
  
  for indexed_color in palette:
    r1, g1, b1, a1 = get_rgba(color)
    r2, g2, b2, a2 = get_rgba(indexed_color)
    r1 >>= 3
    g1 >>= 3
    b1 >>= 3
    a1 >>= 3
    r2 >>= 3
    g2 >>= 3
    b2 >>= 3
    a2 >>= 3
    
    coldiff = col_diff_g[g2 - g1 & 127]
    if coldiff < min_dist:
      coldiff += col_diff_r[r2 - r1 & 127]
      if coldiff < min_dist:
        coldiff += col_diff_b[b2 - b1 & 127]
        if coldiff < min_dist:
          coldiff += col_diff_a[a2 - a1 & 127]
          if coldiff < min_dist:
            min_dist = coldiff
            value = indexed_color
  
  return value

def get_nearest_color_fast(color, palette):
  if color in palette:
    return color
  
  r, g, b, a = get_rgba(color)
  
  if a < 16: # Transparent
    for indexed_color in palette:
      if len(indexed_color) == 4 and indexed_color[3] == 0:
        return indexed_color
  
  min_dist = 0x7FFFFFFF
  best_color = palette[0]
  
  for indexed_color in palette:
    curr_dist = get_color_distance_fast(color, indexed_color)
    
    if curr_dist < min_dist:
      if curr_dist == 0:
        return indexed_color
      
      min_dist = curr_dist
      best_color = indexed_color
  
  return best_color

def get_color_distance_fast(color_1, color_2):
  dist  = abs(color_1[0] - color_2[0])
  dist += abs(color_1[1] - color_2[1])
  dist += abs(color_1[2] - color_2[2])
  return dist


def decode_palettes(palette_data, palette_format, num_colors, image_format):
  if image_format not in IMAGE_FORMATS_THAT_USE_PALETTES:
    return []
  
  colors = []
  offset = 0
  for i in range(num_colors):
    raw_color = read_u16(palette_data, offset)
    if palette_format == 0:
      color = convert_ia8_to_color(raw_color)
    elif palette_format == 1:
      color = convert_rgb565_to_color(raw_color)
    elif palette_format == 2:
      color = convert_rgb5a3_to_color(raw_color)
    colors.append(color)
    offset += 2
  
  return colors

def generate_new_palettes_from_image(image, image_format, palette_format):
  if image_format not in IMAGE_FORMATS_THAT_USE_PALETTES:
    return ([],{})
  
  pixels = image.load()
  width, height = image.size
  encoded_colors = []
  colors_to_color_indexes = {}
  for y in range(height):
    for x in range(width):
      color = pixels[x,y]
      encoded_color = encode_color(color, palette_format)
      if encoded_color not in encoded_colors:
        encoded_colors.append(encoded_color)
      if color not in colors_to_color_indexes:
        colors_to_color_indexes[color] = encoded_colors.index(encoded_color)
  
  if len(encoded_colors) > MAX_COLORS_FOR_IMAGE_FORMAT[image_format]:
    raise TooManyColorsError(
      "Maximum number of colors supported by image format %d is %d, but replacement image has %d colors" % (
        image_format, MAX_COLORS_FOR_IMAGE_FORMAT[image_format], len(encoded_colors)
      )
    )
  
  return (encoded_colors, colors_to_color_indexes)

def encode_color(color, palette_format):
  if palette_format == 0:
    raw_color = convert_color_to_ia8(color)
  elif palette_format == 1:
    raw_color = convert_color_to_rgb565(color)
  elif palette_format == 2:
    raw_color = convert_color_to_rgb5a3(color)
  
  return raw_color

def encode_palette(encoded_colors, palette_format, image_format):
  if image_format not in IMAGE_FORMATS_THAT_USE_PALETTES:
    return BytesIO()
  
  if len(encoded_colors) > MAX_COLORS_FOR_IMAGE_FORMAT[image_format]:
    raise TooManyColorsError(
      "Maximum number of colors supported by image format %d is %d, but replacement image has %d colors" % (
        image_format, MAX_COLORS_FOR_IMAGE_FORMAT[image_format], len(encoded_colors)
      )
    )
  
  offset = 0
  new_palette_data = BytesIO()
  for raw_color in encoded_colors:
    write_u16(new_palette_data, offset, raw_color)
    offset += 2
  
  return new_palette_data



def decode_image(image_data, palette_data, image_format, palette_format, num_colors, image_width, image_height):
  colors = decode_palettes(palette_data, palette_format, num_colors, image_format)
  
  block_width = BLOCK_WIDTHS[image_format]
  block_height = BLOCK_HEIGHTS[image_format]
  block_data_size = BLOCK_DATA_SIZES[image_format]
  
  image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
  pixels = image.load()
  offset = 0
  block_x = 0
  block_y = 0
  while block_y < image_height:
    pixel_color_data = decode_block(image_format, image_data, offset, block_data_size, colors)
    
    for i, color in enumerate(pixel_color_data):
      x_in_block = i % block_width
      y_in_block = i // block_width
      x = block_x+x_in_block
      y = block_y+y_in_block
      if x >= image_width or y >= image_height:
        continue
      
      pixels[x,y] = color
    
    offset += block_data_size
    block_x += block_width
    if block_x >= image_width:
      block_x = 0
      block_y += block_height
  
  return image

def decode_block(image_format, image_data, offset, block_data_size, colors):
  if image_format == 0:
    return decode_i4_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 1:
    return decode_i8_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 2:
    return decode_ia4_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 3:
    return decode_ia8_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 4:
    return decode_rgb565_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 5:
    return decode_rgb5a3_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 6:
    return decode_rgba32_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 8:
    return decode_c4_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 9:
    return decode_c8_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 0xA:
    return decode_c14x2_block(image_format, image_data, offset, block_data_size, colors)
  elif image_format == 0xE:
    return decode_cmpr_block(image_format, image_data, offset, block_data_size, colors)
  else:
    raise Exception("Unknown image format: %X" % image_format)

def decode_i4_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for byte_index in range(block_data_size):
    byte = read_u8(image_data, offset+byte_index)
    for nibble_index in range(2):
      i4 = (byte >> (1-nibble_index)*4) & 0xF
      color = convert_i4_to_color(i4)
      
      pixel_color_data.append(color)
  
  return pixel_color_data

def decode_i8_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size):
    i8 = read_u8(image_data, offset+i)
    color = convert_i8_to_color(i8)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_ia4_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size):
    ia4 = read_u8(image_data, offset+i)
    color = convert_ia4_to_color(ia4)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_ia8_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size//2):
    ia8 = read_u16(image_data, offset+i*2)
    color = convert_ia8_to_color(ia8)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_rgb565_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size//2):
    rgb565 = read_u16(image_data, offset+i*2)
    color = convert_rgb565_to_color(rgb565)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_rgb5a3_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size//2):
    rgb5a3 = read_u16(image_data, offset+i*2)
    color = convert_rgb5a3_to_color(rgb5a3)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_rgba32_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(16):
    a = read_u8(image_data, offset+(i*2))
    r = read_u8(image_data, offset+(i*2)+1)
    g = read_u8(image_data, offset+(i*2)+32)
    b = read_u8(image_data, offset+(i*2)+33)
    color = (r, g, b, a)
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_c4_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for byte_index in range(block_data_size):
    byte = read_u8(image_data, offset+byte_index)
    for nibble_index in range(2):
      color_index = (byte >> (1-nibble_index)*4) & 0xF
      color = colors[color_index]
      
      pixel_color_data.append(color)
  
  return pixel_color_data

def decode_c8_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size):
    color_index = read_u8(image_data, offset+i)
    if color_index == 0xFF:
      # This block bleeds past the edge of the image
      color = None
    else:
      color = colors[color_index]
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_c14x2_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = []
  
  for i in range(block_data_size//2):
    color_index = read_u16(image_data, offset+i*2) & 0x3FFF
    if color_index == 0x3FFF:
      # This block bleeds past the edge of the image
      color = None
    else:
      color = colors[color_index]
    
    pixel_color_data.append(color)
  
  return pixel_color_data

def decode_cmpr_block(image_format, image_data, offset, block_data_size, colors):
  pixel_color_data = [None]*64
  
  subblock_offset = offset
  for subblock_index in range(4):
    subblock_x = (subblock_index%2)*4
    subblock_y = (subblock_index//2)*4
    
    color_0_rgb565 = read_u16(image_data, subblock_offset)
    color_1_rgb565 = read_u16(image_data, subblock_offset+2)
    colors = get_interpolated_cmpr_colors(color_0_rgb565, color_1_rgb565)
    
    color_indexes = read_u32(image_data, subblock_offset+4)
    for i in range(16):
      color_index = ((color_indexes >> ((15-i)*2)) & 3)
      color = colors[color_index]
      
      x_in_subblock = i % 4
      y_in_subblock = i // 4
      pixel_index_in_block = subblock_x + subblock_y*8 + y_in_subblock*8 + x_in_subblock
      
      pixel_color_data[pixel_index_in_block] = color
    
    subblock_offset += 8
  
  return pixel_color_data



def encode_image_from_path(new_image_file_path, image_format, palette_format):
  image = Image.open(new_image_file_path)
  return encode_image(image, image_format, palette_format)

def encode_image(image, image_format, palette_format):
  image = image.convert("RGBA")
  image_width, image_height = image.size
  
  encoded_colors, colors_to_color_indexes = generate_new_palettes_from_image(image, image_format, palette_format)
  
  block_width = BLOCK_WIDTHS[image_format]
  block_height = BLOCK_HEIGHTS[image_format]
  block_data_size = BLOCK_DATA_SIZES[image_format]
  
  pixels = image.load()
  offset_in_image_data = 0
  block_x = 0
  block_y = 0
  new_image_data = BytesIO()
  while block_y < image_height:
    block_data = encode_image_to_block(
      image_format,
      pixels, colors_to_color_indexes,
      block_x, block_y, block_width, block_height, image_width, image_height
    )
    
    assert len(block_data) == BLOCK_DATA_SIZES[image_format]
    
    write_bytes(new_image_data, offset_in_image_data, block_data)
    
    offset_in_image_data += BLOCK_DATA_SIZES[image_format]
    block_x += BLOCK_WIDTHS[image_format]
    if block_x >= image_width:
      block_x = 0
      block_y += BLOCK_HEIGHTS[image_format]
  
  new_palette_data = encode_palette(encoded_colors, palette_format, image_format)
  
  return (new_image_data, new_palette_data, encoded_colors)

def encode_image_to_block(image_format, pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  if image_format == 4:
    return encode_image_to_rgb563_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  elif image_format == 5:
    return encode_image_to_rgb5a3_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  elif image_format == 6:
    return encode_image_to_rgba32_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  elif image_format == 8:
    return encode_image_to_c4_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  elif image_format == 9:
    return encode_image_to_c8_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  elif image_format == 0xE:
    return encode_image_to_cmpr_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height)
  else:
    raise Exception("Unknown image format: %X" % image_format)

def encode_image_to_rgb563_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  offset = 0
  for y in range(block_y, block_y+block_height):
    for x in range(block_x, block_x+block_width):
      color = pixels[x,y]
      rgb565 = convert_color_to_rgb565(color)
      write_u16(new_data, offset, rgb565)
      offset += 2
  
  new_data.seek(0)
  return new_data.read()

def encode_image_to_rgb5a3_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  offset = 0
  for y in range(block_y, block_y+block_height):
    for x in range(block_x, block_x+block_width):
      color = pixels[x,y]
      rgb5a3 = convert_color_to_rgb5a3(color)
      write_u16(new_data, offset, rgb5a3)
      offset += 2
  
  new_data.seek(0)
  return new_data.read()

def encode_image_to_rgba32_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  for i in range(16):
    x = block_x + (i % block_width)
    y = block_y + (i // block_width)
    color = pixels[x, y]
    r, g, b, a = color
    write_u8(new_data, (i*2), a)
    write_u8(new_data, (i*2)+1, r)
    write_u8(new_data, (i*2)+32, g)
    write_u8(new_data, (i*2)+33, b)
  
  new_data.seek(0)
  return new_data.read()

def encode_image_to_c4_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  offset = 0
  
  for y in range(block_y, block_y+block_height):
    for x in range(block_x, block_x+block_width, 2):
      color_1 = pixels[x,y]
      color_1_index = colors_to_color_indexes[color_1]
      assert 0 <= color_1_index <= 0xF
      color_2 = pixels[x,y]
      color_2_index = colors_to_color_indexes[color_2]
      assert 0 <= color_2_index <= 0xF
      
      byte = ((color_1_index & 0xF) << 4) | (color_2_index & 0xF)
      
      write_u8(new_data, offset, byte)
      offset += 1
  
  new_data.seek(0)
  return new_data.read()

def encode_image_to_c8_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  offset = 0
  for y in range(block_y, block_y+block_height):
    for x in range(block_x, block_x+block_width):
      if x >= image_width or y >= image_height:
        # This block bleeds past the edge of the image
        color_index = 0xFF
      else:
        color = pixels[x,y]
        color_index = colors_to_color_indexes[color]
      write_u8(new_data, offset, color_index)
      offset += 1
  
  new_data.seek(0)
  return new_data.read()

def encode_image_to_cmpr_block(pixels, colors_to_color_indexes, block_x, block_y, block_width, block_height, image_width, image_height):
  new_data = BytesIO()
  subblock_offset = 0
  for subblock_index in range(4):
    subblock_x = block_x + (subblock_index%2)*4
    subblock_y = block_y + (subblock_index//2)*4
    
    all_colors_in_subblock = []
    needs_transparent_color = False
    for i in range(16):
      x_in_subblock = i % 4
      y_in_subblock = i // 4
      color = pixels[subblock_x+x_in_subblock,subblock_y+y_in_subblock]
      r, g, b, a = get_rgba(color)
      if a < 16:
        needs_transparent_color = True
      else:
        all_colors_in_subblock.append(color)
    
    color_0, color_1 = get_best_cmpr_key_colors(all_colors_in_subblock)
    color_0_rgb565 = convert_color_to_rgb565(color_0)
    color_1_rgb565 = convert_color_to_rgb565(color_1)
    
    if needs_transparent_color and color_0_rgb565 > color_1_rgb565:
      color_0_rgb565, color_1_rgb565 = color_1_rgb565, color_0_rgb565
      color_0, color_1 = color_1, color_0
    elif color_0_rgb565 < color_1_rgb565:
      color_0_rgb565, color_1_rgb565 = color_1_rgb565, color_0_rgb565
      color_0, color_1 = color_1, color_0
    
    colors = get_interpolated_cmpr_colors(color_0_rgb565, color_1_rgb565)
    colors[0] = color_0
    colors[1] = color_1
    
    write_u16(new_data, subblock_offset, color_0_rgb565)
    write_u16(new_data, subblock_offset+2, color_1_rgb565)
    
    color_indexes = 0
    for i in range(16):
      x_in_subblock = i % 4
      y_in_subblock = i // 4
      color = pixels[subblock_x+x_in_subblock,subblock_y+y_in_subblock]
      
      if color in colors:
        color_index = colors.index(color)
      else:
        new_color = get_nearest_color_fast(color, colors)
        color_index = colors.index(new_color)
      color_indexes |= (color_index << ((15-i)*2))
    write_u32(new_data, subblock_offset+4, color_indexes)
    
    subblock_offset += 8
  
  new_data.seek(0)
  return new_data.read()

def color_exchange(image, base_color, replacement_color, mask_path=None):
  if mask_path:
    mask_image = Image.open(mask_path).convert("RGBA")
    mask_pixels = mask_image.load()
    
    if image.size != mask_image.size:
      raise Exception("Mask image is not the same size as the texture.")
  
  base_r, base_g, base_b = base_color
  base_h, base_s, base_v = colorsys.rgb_to_hsv(base_r/255, base_g/255, base_b/255)
  base_h = int(base_h*360)
  base_s = int(base_s*100)
  base_v = int(base_v*100)
  
  replacement_r, replacement_g, replacement_b = replacement_color
  replacement_h, replacement_s, replacement_v = colorsys.rgb_to_hsv(replacement_r/255, replacement_g/255, replacement_b/255)
  replacement_h = int(replacement_h*360)
  replacement_s = int(replacement_s*100)
  replacement_v = int(replacement_v*100)
  
  s_change = replacement_s - base_s
  v_change = replacement_v - base_v
  
  pixels = image.load()
  for x in range(image.width):
    for y in range(image.height):
      if mask_path and mask_pixels[x, y] != (255, 0, 0, 255):
        continue
      
      r, g, b, a = pixels[x, y]
      h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
      h = int(h*360)
      s = int(s*100)
      v = int(v*100)
      
      new_h = replacement_h
      new_s = s + s_change
      new_v = v + v_change
      new_h = new_h % 360
      new_s = max(0, min(100, new_s))
      new_v = max(0, min(100, new_v))
      r, g, b = colorsys.hsv_to_rgb(new_h/360, new_s/100, new_v/100)
      r = int(r*255)
      g = int(g*255)
      b = int(b*255)
      pixels[x, y] = (r, g, b, a)
  
  return image
