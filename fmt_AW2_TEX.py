#------------------------------------------------
#--- Alan Wake 2 [PC] - ".tex" plugin for Rich Whitehouse's Noesis
#
#      File: fmt_AW2_TEX.py
#    Author: SilverEzredes
#   Version: November 11, 2023 - v0.9.4
#   Purpose: To import and export Alan Wake 2 .tex files
#   Credits: alphaZomega
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
bAW2Export = False       #Enable or disable export of .tex from the export list
#------------------------------------------------

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Alan Wake 2 Texture [PC]", ".tex")
    noesis.setHandlerTypeCheck(handle, CheckType)
    noesis.setHandlerLoadRGBA(handle, LoadRGBA)

    noesis.logPopup()
    return 1

def CheckType(data):
    return 1
    
def LoadRGBA(data, texList):
    bs = NoeBitStream(data)

    magic = bs.readUShort()
    if magic == 16971:
         print("Error: Invalid magic! This is a Bink video file.")
         return 0
    
    magic2 = bs.readUShort()
    size = bs.readUInt()
    flags = bs.readUInt()
    height = bs.readUInt()
    if height % 4 != 0:
        height += 4 - (height % 4)
        print("Warning: Texture height adjusted!")

    width = bs.readUInt()
    if width % 4 != 0:
        width += 4 - (width % 4)
        print("Warning: Texture width adjusted!")

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

    texData = bs.readBytes(width*height)

    if dxgiFormat == 10:
        texData = rapi.imageDecodeRaw(texData, width, height, "R16G16B16A16")
        print("Format: R16G16B16A16")
    elif dxgiFormat == 71 or dxgiFormat == 72:
        texData = bs.readBytes(width*height // 2)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC1) 
        print("Format: BC1_UNORM_SRGB")
    elif dxgiFormat == 77 or dxgiFormat == 78:
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC3)
        print("Format: BC3_UNORM_SRGB")
    elif dxgiFormat == 80:
        texData = bs.readBytes(width*height // 2)
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC4)
        print("Format: BC4_UNORM")
    elif dxgiFormat == 83:
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC5)
        print("Format: BC5_UNORM")
    elif dxgiFormat == 87: #TO DO
        texData = rapi.imageDecodeRaw(texData, width, height, "B8G8R8A8")
        print("Format: B8G8R8A8_UNORM") 
    elif dxgiFormat == 95 or dxgiFormat == 96: #couldn't find any BC6 textures so far 11.03.2023
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC6H)
        print("Format: BC6")
    elif dxgiFormat == 98 or dxgiFormat == 99:
        texData = rapi.imageDecodeDXT(texData, width, height, noesis.FOURCC_BC7)
        print("Format: BC7_UNORM_SRGB")
    else:
        print("Fatal Error: Unsupported texture type!")
        return 0
    
    tex = NoeTexture("AW2.tex", width, height, texData, noesis.NOESISTEX_RGBA32)
    texList.append(tex)

    return 1