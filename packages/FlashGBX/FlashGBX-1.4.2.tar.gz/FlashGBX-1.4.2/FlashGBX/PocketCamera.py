from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
import os, hashlib
import email.utils

class PocketCamera:
	DATA = None
	PALETTES = [
		[ 255, 255, 255,   176, 176, 176,   104, 104, 104,   0, 0, 0 ], # Grayscale
		[ 208, 217, 60,   120, 164, 106,   84, 88, 84,   36, 70, 36 ], # Game Boy
		#[ 196, 207, 161,   139, 149, 109,   77, 83, 60,   31, 31, 31 ], # Game Boy Pocket
		[ 255, 255, 255,   181, 179, 189,   84, 83, 103,   9, 7, 19 ], # Super Game Boy
		[ 240, 240, 240,   218, 196, 106,   112, 88, 52,   30, 30, 30 ], # Game Boy Color (JPN)
		[ 240, 240, 240,   220, 160, 160,   136, 78, 78,   30, 30, 30 ], # Game Boy Color (USA Gold)
		[ 240, 240, 240,   134, 200, 100,   58, 96, 132,   30, 30, 30 ], # Game Boy Color (USA/EUR)
	]
	PALETTE = [ 240, 240, 240,   218, 196, 106,   112, 88, 52,   30, 30, 30 ] # default
	IMAGES = [None] * 31
	IMAGES_DELETED = []
	ORDER = None
	
	def __init__(self):
		pass
		
	def LoadFile(self, savefile):
		if os.path.getsize(savefile) != 128*1024: return False
		with open(savefile, "rb") as file: self.DATA = file.read()
		if self.DATA[0x1FFB1:0x1FFB6] != b'Magic':
			self.DATA = None
			return False
		
		order_raw = self.DATA[0x11D7:0x11F5]
		order = [None] * 30
		deleted = []
		for i in range(0, 30):
			if order_raw[i] == 0xFF:
				deleted.append(i)
			else:
				order[order_raw[i]] = i
		
		while None in order: order.remove(None)
		order.extend(deleted)
		self.ORDER = order
		self.IMAGES_DELETED = deleted
		
		self.IMAGES[0] = self.ExtractGameFace()
		for i in range(0, 30):
			self.IMAGES[i+1] = self.ExtractPicture(i)
		return True
	
	def SetPalette(self, palette):
		if isinstance(palette, int):
			palette = self.PALETTES[palette]
		for p in range (0, len(self.IMAGES)):
			self.IMAGES[p].putpalette(palette)
		self.PALETTE = palette
	
	def GetPicture(self, index):
		return self.IMAGES[index]
	
	def IsEmpty(self, index):
		return (hashlib.sha1(self.IMAGES[index].tobytes()).digest() == b'\xefX\xa8\x12\xa8\x1a\xb1EI\xd8\xf4\xfb\x86\xe9\xec\xb5J_\xb7#')
	
	def IsDeleted(self, index):
		index = self.ORDER[index-1]
		return index in self.IMAGES_DELETED
	
	def ConvertPicture(self, buffer):
		tile_width = 16
		tile_height = 14
		
		img = Image.new(mode='P', size=(128, 112))
		img.putpalette(self.PALETTE)
		pixels = img.load()
		for h in range(tile_height):
			for w in range(tile_width):
				tile_pos = 16 * ((h * tile_width) + w)
				tile = buffer[tile_pos:tile_pos+16]
				for i in range(8):
					for j in range(8):
						hi = (tile[i * 2] >> (7 - j)) & 1
						lo = (tile[i * 2 + 1] >> (7 - j)) & 1
						pixels[(w * 8) + j, (h * 8) + i] = (lo << 1 | hi)
		
		return img
	
	def ExtractGameFace(self):
		offset = 0x11FC
		imgbuffer = self.DATA[offset:offset+0x1000]
		return self.ConvertPicture(imgbuffer)
		
	def ExtractPicture(self, index):
		index = self.ORDER[index]
		offset = 0x2000 + (index * 0x1000)
		imgbuffer = self.DATA[offset:offset+0x1000]
		return self.ConvertPicture(imgbuffer)
	
	def ExportPicture(self, index, path):
		pnginfo = PngInfo()
		pnginfo.add_text("Software", "FlashGBX")
		pnginfo.add_text("Source", "Pocket Camera")
		pnginfo.add_text("Creation Time", email.utils.formatdate())
		
		if index == 0:
			pic = self.GetPicture(0)
			pnginfo.add_text("Title", "Game Face")
		else:
			pic = self.GetPicture(index)
			pnginfo.add_text("Title", "Photo {:02d}".format(index))
		
		ext = os.path.splitext(path)[1]
		if ext.lower() == ".png":
			outpic = pic
			outpic.save(path, pnginfo=pnginfo)
		elif ext.lower() == ".gif":
			outpic = pic
			outpic.save(path)
		elif ext.lower() in (".jpg", ".jpeg"):
			outpic = pic.convert("RGB")
			outpic.save(path, quality=100, subsampling=0)
		else:
			outpic = pic.convert("RGB")
			outpic.save(path)
