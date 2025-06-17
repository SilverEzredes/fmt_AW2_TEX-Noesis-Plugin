#------------------------------------------------
#--- Alan Wake 2 | FBC Firebreak [PC] - ".tex" plugin for Rich Whitehouse's Noesis
#
#      File: fmt_AW2_TEX.py
#    Author: SilverEzredes
#   Version: June 17, 2025 - v0.9.7
#   Purpose: To import and export Alan Wake 2 and FBC Firebreak .tex files
#   Credits: alphaZomega
#------------------------------------------------
#--- Change Log:
#   v0.9.7 
#       - Added FBC Firebreak support.
#       - Fixed an issue where some DDS formats were not being read correctly.
#------------------------------------------------
#--- Texture Guide:
#    _d: DIFFUSE_ALBEDO
#    _n: NORMAL
#    _s: SMOOTHNESS
#   _sa: SPECULAR_ALBEDO
#    _e: EMISSIVE
#   _dt: DETAIL
#------------------------------------------------
#--- Options:
isAW2Export = False         # Enable or disable export of .tex from the export list
isDebug     = False         # Enable or disable debug mode
#------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Alan Wake 2 | FBC Firebreak Texture [PC]", ".tex")
    noesis.setHandlerTypeCheck(handle, texCheckType)
    noesis.setHandlerLoadRGBA(handle, texLoadRGBA)

    noesis.logPopup()
    return 1

def texCheckType(data):
	bs = NoeBitStream(data)
     
	magic = bs.readUShort()
	if magic == 17476:
		return 1
	else: 
		print("[ FATAL ERROR ] Unknown file magic: " + str(hex(magic) + " expected DDS!"))
		return 0
    
def texLoadRGBA(data, texList):
    bs = NoeBitStream(data)

    magic = bs.readUShort()
    if magic == 16971:
         print("[ ERROR ] Invalid file magic! This is a Bink video file.")
         return 0
    magic2 = bs.readUShort()
    size = bs.readUInt()
    flags = bs.readUInt()
    height = bs.readUInt()
    width = bs.readUInt()
    linerSize = bs.readUInt()
    depth = bs.readUInt()
    mipMapCount = bs.readUInt()
    for i in range(11):
        reserved = bs.readUInt()
    size2 = bs.readUInt()
    flags2 = bs.readUInt()
    fourCC = bs.readUInt()
    RGBBitCount = bs.readUInt()
    RBitMask = bs.readUInt()
    GBitMask = bs.readUInt()
    BBitMask = bs.readUInt()
    ABitMask = bs.readUInt()
    caps = bs.readUInt()
    caps2 = bs.readUInt()
    caps3 = bs.readUInt()
    caps4 = bs.readUInt()
    reserved2 = bs.readUInt()
    dxgiFormat = bs.readUInt()
    resourceDimension = bs.readUInt()
    miscFlag = bs.readUInt()
    arraySize = bs.readUInt()
    miscFlag2 = bs.readUInt()
    
    if dxgiFormat != 91 and dxgiFormat != 87:
        if height % 4 != 0:
            height += 4 - (height % 4)
            if isDebug:
                print("[ WARNING ] Texture height adjusted!")
        if width % 4 != 0:
            width += 4 - (width % 4)
            if isDebug:
                print("[ WARNING ] Texture width adjusted!")

    if dxgiFormat == 10:
        texData = bs.readBytes(width*height)
        texData = rapi.imageDecodeRaw(texData, width, height, "R16G16B16A16")
        print("DDS Format: R16G16B16A16")
    elif dxgiFormat == 56:
        texData = bs.readBytes(width*height)*2
        texData = rapi.imageDecodeRaw(texData, width, height, "R16")
        print("DDS Format: R16_UNORM")
    elif dxgiFormat == 71 or dxgiFormat == 72:
        texData = bs.readBytes(width*height // 2)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC1) 
        print("DDS Format: BC1_UNORM_SRGB")
    elif dxgiFormat == 77 or dxgiFormat == 78:
        texData = bs.readBytes(width*height)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC3)
        print("DDS Format: BC3_UNORM_SRGB")
    elif dxgiFormat == 80:
        texData = bs.readBytes(width*height // 2)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC4)
        print("DDS Format: BC4_UNORM")
    elif dxgiFormat == 83:
        texData = bs.readBytes(width*height)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC5)
        print("DDS Format: BC5_UNORM")
    elif dxgiFormat == 87:
        texData = bs.readBytes(width*height*4)
        texData = rapi.imageDecodeRaw(texData, width, height, "B8G8R8A8")
        print("DDS Format: B8G8R8A8_UNORM") 
    elif dxgiFormat == 91:
        texData = bs.readBytes(width*height*4)
        texData = rapi.imageDecodeRaw(texData, width, height, "B8G8R8A8_SRGB")
        print("DDS Format: B8G8R8A8_UNORM_SRGB")
    elif dxgiFormat == 95 or dxgiFormat == 96:
        texData = bs.readBytes(width*height)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC6H)
        print("DDS Format: BC6")
    elif dxgiFormat == 98 or dxgiFormat == 99:
        texData = bs.readBytes(width*height)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC7)
        print("DDS Format: BC7_UNORM_SRGB")
    else:
        print("[ FATAL ERROR ] Unsupported texture type!")
        return 0
    
    tex = NoeTexture("AW2.tex", width, height, texData, noesis.NOESISTEX_RGBA32)
    texList.append(tex)

    return 1