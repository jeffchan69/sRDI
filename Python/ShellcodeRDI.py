import sys

if sys.version_info < (3,0):
    print("[!] Sorry, requires Python 3.x")
    sys.exit(1)
    
import struct
from struct import pack

MACHINE_IA64=512
MACHINE_AMD64=34404

def is64BitDLL(bytes):
    header_offset = struct.unpack("<L", bytes[60:64])[0]
    machine = struct.unpack("<H", bytes[header_offset+4:header_offset+4+2])[0]
    if machine == MACHINE_IA64 or machine == MACHINE_AMD64:
        return True   
    return False
    
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def HashFunctionName(name, module = None):

        function = name.encode() + b'\x00'

        if(module):
                module = module.upper().encode('UTF-16LE') + b'\x00\x00'

                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

                moduleHash = 0

                for b in module:
                        moduleHash = ror(moduleHash, 13, 32)
                        moduleHash += b

                functionHash += moduleHash

                if functionHash > 0xFFFFFFFF: functionHash -= 0x100000000

        else:
                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

        return functionHash

def ConvertToShellcode(dllBytes, functionHash=0x10, userData=b'None', flags=0):

    #MARKER:S
    rdiShellcode32 = "\x83\xEC\x6C\x53\x55\x56\x57\xB9\x4C\x77\x26\x07\xE8\xFD\x06\x00\x00\x8B\xF8\xB9\x49\xF7\x02\x78\x89\x7C\x24\x2C\xE8\xED\x06\x00\x00\x8B\xF0\xB9\x58\xA4\x53\xE5\x89\x74\x24\x30\xE8\xDD\x06\x00\x00\x8B\xD8\xB9\x10\xE1\x8A\xC3\x89\x5C\x24\x20\xE8\xCD\x06\x00\x00\xB9\xAF\xB1\x5C\x94\x89\x44\x24\x34\xE8\xBF\x06\x00\x00\xB9\x33\x00\x9E\x95\x89\x44\x24\x38\xE8\xB1\x06\x00\x00\xB9\x44\xF0\x35\xE0\x8B\xE8\xE8\xA5\x06\x00\x00\x89\x44\x24\x40\x85\xFF\x0F\x84\x8F\x06\x00\x00\x85\xF6\x0F\x84\x87\x06\x00\x00\x85\xDB\x0F\x84\x7F\x06\x00\x00\x83\x7C\x24\x34\x00\x0F\x84\x74\x06\x00\x00\x83\x7C\x24\x38\x00\x0F\x84\x69\x06\x00\x00\x85\xED\x0F\x84\x61\x06\x00\x00\x85\xC0\x0F\x84\x59\x06\x00\x00\x8B\xBC\x24\x80\x00\x00\x00\x8B\x77\x3C\x03\xF7\x81\x3E\x50\x45\x00\x00\x0F\x85\x41\x06\x00\x00\xB8\x4C\x01\x00\x00\x66\x39\x46\x04\x0F\x85\x32\x06\x00\x00\xF6\x46\x38\x01\x0F\x85\x28\x06\x00\x00\x0F\xB7\x4E\x14\x33\xDB\x0F\xB7\x56\x06\x83\xC1\x24\x85\xD2\x74\x1E\x03\xCE\x83\x79\x04\x00\x8B\x46\x38\x0F\x45\x41\x04\x03\x01\x8D\x49\x28\x3B\xC3\x0F\x46\xC3\x8B\xD8\x83\xEA\x01\x75\xE4\x8D\x44\x24\x58\x50\xFF\xD5\x8B\x4C\x24\x5C\x8D\x51\xFF\x8D\x69\xFF\xF7\xD2\x03\x6E\x50\x8D\x41\xFF\x03\xC3\x23\xEA\x23\xC2\x3B\xE8\x0F\x85\xD2\x05\x00\x00\x6A\x04\x68\x00\x30\x00\x00\x55\xFF\x76\x34\xFF\x54\x24\x30\x8B\xD8\x89\x5C\x24\x28\x85\xDB\x75\x13\x6A\x04\x68\x00\x30\x00\x00\x55\x50\xFF\x54\x24\x30\x8B\xD8\x89\x44\x24\x28\x8B\x84\x24\x90\x00\x00\x00\x89\x44\x24\x1C\xA8\x01\x74\x23\x8B\x47\x3C\x89\x43\x3C\x8B\x4F\x3C\x3B\x4E\x54\x73\x2E\x8B\xEF\x8D\x14\x0B\x2B\xEB\x8A\x04\x2A\x41\x88\x02\x42\x3B\x4E\x54\x72\xF4\xEB\x19\x33\xED\x39\x6E\x54\x76\x12\x8B\xD7\x8B\xCB\x2B\xD3\x8A\x04\x11\x45\x88\x01\x41\x3B\x6E\x54\x72\xF4\x8B\x6B\x3C\x33\xC9\x03\xEB\x89\x4C\x24\x20\x33\xC0\x89\x6C\x24\x14\x0F\xB7\x55\x14\x83\xC2\x28\x66\x3B\x45\x06\x73\x31\x03\xD5\x33\xF6\x39\x32\x76\x19\x8B\x42\x04\x8B\x4A\xFC\x03\xC6\x03\xCB\x8A\x04\x38\x88\x04\x31\x46\x3B\x32\x72\xEB\x8B\x4C\x24\x20\x0F\xB7\x45\x06\x41\x83\xC2\x28\x89\x4C\x24\x20\x3B\xC8\x72\xD1\x83\xBD\x84\x00\x00\x00\x00\x0F\x84\x90\x01\x00\x00\x8B\x8D\x80\x00\x00\x00\x8D\x43\x0C\x03\xC1\x33\xD2\x89\x54\x24\x18\x39\x10\x74\x0D\x8D\x40\x14\x42\x83\x38\x00\x75\xF7\x89\x54\x24\x18\x8B\x74\x24\x1C\x8B\xC6\x83\xE0\x04\x89\x44\x24\x3C\x8B\xC1\x0F\x84\xB8\x00\x00\x00\x83\xFA\x01\x0F\x86\xAF\x00\x00\x00\x83\x64\x24\x20\x00\xC1\xEE\x10\x89\x74\x24\x1C\x8D\x72\xFF\x85\xF6\x0F\x84\xA0\x00\x00\x00\x8B\x74\x24\x20\x8D\x2C\x19\x89\x6C\x24\x24\x8D\x5A\xFF\x8B\xCA\x69\xFF\xFD\x43\x03\x00\x2B\xCE\x33\xD2\xB8\xFF\x7F\x00\x00\xF7\xF1\x81\xC7\xC3\x9E\x26\x00\x33\xD2\x89\xBC\x24\x80\x00\x00\x00\x6A\x05\x8D\x48\x01\x8B\xC7\xC1\xE8\x10\x8D\x7C\x24\x48\x25\xFF\x7F\x00\x00\xF7\xF1\x8B\x54\x24\x28\x03\xC6\x6B\xC0\x14\x59\x6A\x05\x03\xC5\x8B\xF0\xF3\xA5\x59\x8B\xF2\x8B\xF8\xF3\xA5\x6A\x05\x8B\xFA\x8D\x74\x24\x48\x59\xF3\xA5\x8B\x74\x24\x20\x83\xC2\x14\x8B\xBC\x24\x80\x00\x00\x00\x46\x89\x54\x24\x24\x8B\x54\x24\x18\x89\x74\x24\x20\x3B\xF3\x72\x86\x8B\x6C\x24\x14\x8B\x5C\x24\x28\x8B\x85\x80\x00\x00\x00\xEB\x08\x8B\x4C\x24\x40\x89\x4C\x24\x1C\x8D\x34\x18\x8B\x46\x0C\x89\x74\x24\x24\x85\xC0\x0F\x84\x87\x00\x00\x00\x8B\x6C\x24\x18\x03\xC3\x50\xFF\x54\x24\x30\x8B\x3E\x03\xFB\x89\x44\x24\x20\x8B\x46\x10\x03\xC3\x89\x44\x24\x28\x8B\x0F\x85\xC9\x74\x38\x8B\x6C\x24\x20\x8B\x74\x24\x30\x79\x05\x0F\xB7\xC1\xEB\x05\x8D\x41\x02\x03\xC3\x50\x55\xFF\xD6\x8B\xC8\x83\xC7\x04\x8B\x44\x24\x28\x89\x08\x83\xC0\x04\x8B\x0F\x89\x44\x24\x28\x85\xC9\x75\xD8\x8B\x74\x24\x24\x8B\x6C\x24\x18\x83\x7C\x24\x3C\x00\x74\x14\x33\xC0\x40\x3B\xE8\x76\x0D\x69\x44\x24\x1C\xE8\x03\x00\x00\x50\xFF\x54\x24\x44\x8B\x46\x20\x83\xC6\x14\x89\x74\x24\x24\x85\xC0\x75\x81\x8B\x6C\x24\x14\x83\xBD\xE4\x00\x00\x00\x00\x74\x73\x8B\xBD\xE0\x00\x00\x00\x83\xC7\x04\x03\xFB\x89\x7C\x24\x24\x8B\x07\x85\xC0\x74\x5E\x03\xC3\x50\xFF\x54\x24\x30\x8B\x77\x08\x8B\xE8\x8B\x47\x0C\x03\xF3\x03\xC3\x89\x44\x24\x28\x83\x3E\x00\x74\x31\x8B\x7C\x24\x30\x8B\x00\x85\xC0\x79\x05\x0F\xB7\xC0\xEB\x05\x83\xC0\x02\x03\xC3\x50\x55\xFF\xD7\x89\x06\x83\xC6\x04\x8B\x44\x24\x28\x83\xC0\x04\x89\x44\x24\x28\x83\x3E\x00\x75\xD7\x8B\x7C\x24\x24\x83\xC7\x20\x89\x7C\x24\x24\x8B\x07\x85\xC0\x75\xA6\x8B\x6C\x24\x14\x8B\xC3\x2B\x45\x34\x6A\x03\x89\x44\x24\x20\x5F\x0F\x84\xC2\x00\x00\x00\x83\xBD\xA4\x00\x00\x00\x00\x0F\x84\xB5\x00\x00\x00\x8B\xB5\xA0\x00\x00\x00\x03\xF3\x83\x3E\x00\x0F\x84\xA4\x00\x00\x00\x57\x5D\x8D\x7E\x08\xEB\x7E\x0F\xB7\x0F\x66\x8B\xC1\x0F\xB7\xD1\x66\xC1\xE8\x0C\x66\x83\xF8\x0A\x75\x21\x8B\x16\x81\xE1\xFF\x0F\x00\x00\x89\x4C\x24\x40\x8D\x04\x11\x8B\x0C\x18\x03\x4C\x24\x1C\x8B\x44\x24\x40\x03\xC2\x89\x0C\x18\xEB\x45\x66\x3B\xC5\x75\x13\x8B\x06\x81\xE2\xFF\x0F\x00\x00\x8B\x4C\x24\x1C\x03\xD3\x01\x0C\x02\xEB\x2D\x33\xC9\x41\x66\x3B\xC1\x75\x09\x8B\x44\x24\x1C\xC1\xE8\x10\xEB\x0F\x6A\x02\x59\x66\x3B\xC1\x75\x14\x8B\x44\x24\x1C\x0F\xB7\xC0\x8B\x0E\x81\xE2\xFF\x0F\x00\x00\x03\xD3\x01\x04\x0A\x6A\x02\x58\x03\xF8\x8B\x46\x04\x03\xC6\x3B\xF8\x0F\x85\x75\xFF\xFF\xFF\x83\x3F\x00\x8B\xF7\x0F\x85\x65\xFF\xFF\xFF\x8B\x6C\x24\x14\x6A\x03\x5F\x0F\xB7\x75\x14\x33\xC9\x33\xC0\x89\x4C\x24\x30\x83\xC6\x28\x66\x3B\x45\x06\x0F\x83\xEF\x00\x00\x00\x8B\x7C\x24\x34\x03\xF5\xBA\x00\x00\x00\x40\x83\x3E\x00\x0F\x84\xC4\x00\x00\x00\x8B\x4E\x14\x8B\xC1\x25\x00\x00\x00\x20\x75\x0B\x85\xCA\x75\x07\x85\xC9\x78\x03\x40\xEB\x62\x85\xC0\x75\x30\x85\xCA\x75\x08\x85\xC9\x79\x04\x6A\x08\xEB\x51\x85\xC0\x75\x20\x85\xCA\x74\x08\x85\xC9\x78\x04\x6A\x02\xEB\x41\x85\xC0\x75\x10\x85\xCA\x74\x08\x85\xC9\x79\x04\x6A\x04\xEB\x31\x85\xC0\x74\x4A\x85\xCA\x75\x08\x85\xC9\x78\x04\x6A\x10\xEB\x21\x85\xC0\x74\x3A\x85\xCA\x75\x0B\x85\xC9\x79\x07\xB8\x80\x00\x00\x00\xEB\x0F\x85\xC0\x74\x27\x85\xCA\x74\x0D\x85\xC9\x78\x09\x6A\x20\x58\x89\x44\x24\x10\xEB\x1A\x85\xC0\x74\x12\x85\xCA\x74\x0E\x8B\x44\x24\x10\x85\xC9\x6A\x40\x5A\x0F\x48\xC2\xEB\xE4\x8B\x44\x24\x10\xF7\x46\x14\x00\x00\x00\x04\x74\x09\x0D\x00\x02\x00\x00\x89\x44\x24\x10\x8D\x4C\x24\x10\x51\x50\x8B\x46\xFC\xFF\x36\x03\xC3\x50\xFF\xD7\x8B\x4C\x24\x30\xBA\x00\x00\x00\x40\x0F\xB7\x45\x06\x41\x83\xC6\x28\x89\x4C\x24\x30\x3B\xC8\x0F\x82\x1F\xFF\xFF\xFF\x6A\x03\x5F\x6A\x00\x6A\x00\x6A\xFF\xFF\x54\x24\x44\x83\xBD\xC4\x00\x00\x00\x00\x74\x3A\x8B\x85\xC0\x00\x00\x00\x83\x64\x24\x40\x00\x8B\x74\x18\x0C\x33\xC0\x03\xF3\x2B\xFE\xC1\xEF\x02\x85\xF6\x0F\x45\xF8\x85\xFF\x74\x19\x8B\x6C\x24\x40\x33\xC0\x6A\x00\x40\x50\x53\xFF\x16\x45\x8D\x76\x04\x3B\xEF\x75\xEF\x8B\x6C\x24\x14\x33\xC0\x40\x50\x50\x8B\x45\x28\x53\x03\xC3\xFF\xD0\x83\xBC\x24\x84\x00\x00\x00\x00\x0F\x84\xAB\x00\x00\x00\x83\x7D\x7C\x00\x0F\x84\xA1\x00\x00\x00\x8B\x55\x78\x03\xD3\x8B\x6A\x18\x85\xED\x0F\x84\x91\x00\x00\x00\x83\x7A\x14\x00\x0F\x84\x87\x00\x00\x00\x8B\x7A\x20\x8B\x4A\x24\x03\xFB\x83\x64\x24\x38\x00\x03\xCB\x85\xED\x74\x74\x8B\x37\xC7\x44\x24\x20\x00\x00\x00\x00\x03\xF3\x74\x66\x8A\x06\x84\xC0\x74\x1A\x8B\x6C\x24\x20\x0F\xBE\xC0\x03\xE8\xC1\xCD\x0D\x46\x8A\x06\x84\xC0\x75\xF1\x89\x6C\x24\x20\x8B\x6A\x18\x8B\x84\x24\x84\x00\x00\x00\x3B\x44\x24\x20\x75\x04\x85\xC9\x75\x15\x8B\x44\x24\x38\x83\xC7\x04\x40\x83\xC1\x02\x89\x44\x24\x38\x3B\xC5\x72\xAE\xEB\x20\x0F\xB7\x09\x8B\x42\x1C\xFF\xB4\x24\x8C\x00\x00\x00\xFF\xB4\x24\x8C\x00\x00\x00\x8D\x04\x88\x8B\x04\x18\x03\xC3\xFF\xD0\x59\x59\x8B\xC3\xEB\x02\x33\xC0\x5F\x5E\x5D\x5B\x83\xC4\x6C\xC3\x83\xEC\x14\x64\xA1\x30\x00\x00\x00\x53\x55\x56\x8B\x40\x0C\x57\x89\x4C\x24\x1C\x8B\x78\x0C\xE9\xA5\x00\x00\x00\x8B\x47\x30\x33\xF6\x8B\x5F\x2C\x8B\x3F\x89\x44\x24\x10\x8B\x42\x3C\x89\x7C\x24\x14\x8B\x6C\x10\x78\x89\x6C\x24\x18\x85\xED\x0F\x84\x80\x00\x00\x00\xC1\xEB\x10\x33\xC9\x85\xDB\x74\x2F\x8B\x7C\x24\x10\x0F\xBE\x2C\x0F\xC1\xCE\x0D\x80\x3C\x0F\x61\x89\x6C\x24\x10\x7C\x09\x8B\xC5\x83\xC0\xE0\x03\xF0\xEB\x04\x03\x74\x24\x10\x41\x3B\xCB\x72\xDD\x8B\x7C\x24\x14\x8B\x6C\x24\x18\x8B\x44\x2A\x20\x33\xDB\x8B\x4C\x2A\x18\x03\xC2\x89\x4C\x24\x10\x85\xC9\x74\x34\x8B\x38\x33\xED\x03\xFA\x83\xC0\x04\x89\x44\x24\x20\x8A\x0F\xC1\xCD\x0D\x0F\xBE\xC1\x03\xE8\x47\x84\xC9\x75\xF1\x8B\x7C\x24\x14\x8D\x04\x2E\x3B\x44\x24\x1C\x74\x20\x8B\x44\x24\x20\x43\x3B\x5C\x24\x10\x72\xCC\x8B\x57\x18\x85\xD2\x0F\x85\x50\xFF\xFF\xFF\x33\xC0\x5F\x5E\x5D\x5B\x83\xC4\x14\xC3\x8B\x74\x24\x18\x8B\x44\x16\x24\x8D\x04\x58\x0F\xB7\x0C\x10\x8B\x44\x16\x1C\x8D\x04\x88\x8B\x04\x10\x03\xC2\xEB\xDB"
    rdiShellcode64 = "\x48\x8B\xC4\x48\x89\x58\x08\x44\x89\x48\x20\x4C\x89\x40\x18\x89\x50\x10\x55\x56\x57\x41\x54\x41\x55\x41\x56\x41\x57\x48\x8D\x68\xA9\x48\x81\xEC\x90\x00\x00\x00\x48\x8B\xF1\xB9\x4C\x77\x26\x07\xE8\x0F\x07\x00\x00\xB9\x49\xF7\x02\x78\x48\x89\x45\xC7\x48\x8B\xD8\xE8\xFE\x06\x00\x00\xB9\x58\xA4\x53\xE5\x48\x89\x45\xBF\x4C\x8B\xE8\xE8\xED\x06\x00\x00\xB9\x10\xE1\x8A\xC3\x4C\x8B\xF8\xE8\xE0\x06\x00\x00\xB9\xAF\xB1\x5C\x94\x48\x89\x45\xDF\x4C\x8B\xE0\xE8\xCF\x06\x00\x00\xB9\x33\x00\x9E\x95\x48\x89\x45\xE7\x48\x8B\xF8\xE8\xBE\x06\x00\x00\xB9\x44\xF0\x35\xE0\x4C\x8B\xF0\xE8\xB1\x06\x00\x00\x45\x33\xC0\x48\x89\x45\xD7\x48\x85\xDB\x0F\x84\x83\x06\x00\x00\x4D\x85\xED\x0F\x84\x7A\x06\x00\x00\x4D\x85\xFF\x0F\x84\x71\x06\x00\x00\x4D\x85\xE4\x0F\x84\x68\x06\x00\x00\x48\x85\xFF\x0F\x84\x5F\x06\x00\x00\x4D\x85\xF6\x0F\x84\x56\x06\x00\x00\x48\x85\xC0\x0F\x84\x4D\x06\x00\x00\x48\x63\x7E\x3C\x48\x03\xFE\x81\x3F\x50\x45\x00\x00\x0F\x85\x3A\x06\x00\x00\xB8\x64\x86\x00\x00\x66\x39\x47\x04\x0F\x85\x2B\x06\x00\x00\x45\x8D\x48\x01\x44\x84\x4F\x38\x0F\x85\x1D\x06\x00\x00\x0F\xB7\x4F\x14\x41\x8B\xD8\x48\x83\xC1\x24\x66\x44\x3B\x47\x06\x73\x24\x0F\xB7\x57\x06\x48\x03\xCF\x44\x39\x41\x04\x8B\x47\x38\x0F\x45\x41\x04\x03\x01\x48\x8D\x49\x28\x3B\xC3\x0F\x46\xC3\x8B\xD8\x49\x2B\xD1\x75\xE3\x48\x8D\x4D\xEF\x41\xFF\xD6\x8B\x55\xF3\x44\x8B\xC2\x44\x8D\x72\xFF\xF7\xDA\x44\x03\x77\x50\x49\x8D\x48\xFF\x8B\xC2\x4C\x23\xF0\x8B\xC3\x48\x03\xC8\x49\x8D\x40\xFF\x48\xF7\xD0\x48\x23\xC8\x4C\x3B\xF1\x0F\x85\xAF\x05\x00\x00\x48\x8B\x4F\x30\x41\xBC\x00\x30\x00\x00\x45\x8B\xC4\x41\xB9\x04\x00\x00\x00\x49\x8B\xD6\x41\xFF\xD7\x45\x33\xDB\x48\x8B\xD8\x48\x85\xC0\x75\x15\x44\x8D\x48\x04\x45\x8B\xC4\x49\x8B\xD6\x33\xC9\x41\xFF\xD7\x48\x8B\xD8\x45\x33\xDB\x44\x8B\x65\x7F\x41\xBE\x01\x00\x00\x00\x45\x84\xE6\x74\x1D\x8B\x46\x3C\x89\x43\x3C\x8B\x56\x3C\xEB\x0B\x8B\xCA\x41\x03\xD6\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\xEB\x19\x41\x8B\xD3\x44\x39\x5F\x54\x76\x10\x8B\xCA\x41\x03\xD6\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\x48\x63\x7B\x3C\x45\x8B\xD3\x48\x03\xFB\x48\x89\x7D\xCF\x44\x0F\xB7\x47\x14\x49\x83\xC0\x28\x66\x44\x3B\x5F\x06\x73\x3A\x4C\x03\xC7\x45\x8B\xCB\x45\x39\x18\x76\x1F\x41\x8B\x50\x04\x41\x8B\x48\xFC\x41\x8B\xC1\x45\x03\xCE\x48\x03\xC8\x48\x03\xD0\x8A\x04\x32\x88\x04\x19\x45\x3B\x08\x72\xE1\x0F\xB7\x47\x06\x45\x03\xD6\x49\x83\xC0\x28\x44\x3B\xD0\x72\xC9\x44\x39\x9F\x94\x00\x00\x00\x0F\x84\x51\x01\x00\x00\x8B\x8F\x90\x00\x00\x00\x45\x8B\xEB\x44\x89\x5D\xB3\x4C\x8D\x04\x19\x49\x8D\x40\x0C\x44\x39\x18\x74\x10\x45\x03\xEE\x48\x8D\x40\x14\x44\x39\x18\x75\xF4\x44\x89\x6D\xB3\x41\x8B\xC4\x83\xE0\x04\x89\x45\xB7\x8B\xC1\x0F\x84\xBF\x00\x00\x00\x45\x3B\xEE\x0F\x86\xB6\x00\x00\x00\x41\xC1\xEC\x10\x45\x8D\x4D\xFF\x45\x85\xC9\x74\x6F\x4D\x8B\xD0\x41\xBF\xFF\x7F\x00\x00\x41\x0F\x10\x02\x33\xD2\x41\x8B\xCD\x41\x2B\xCB\x69\xF6\xFD\x43\x03\x00\x41\x8B\xC7\xF7\xF1\x33\xD2\x81\xC6\xC3\x9E\x26\x00\x41\x8D\x0C\x06\x8B\xC6\xC1\xE8\x10\x41\x23\xC7\xF7\xF1\x41\x03\xC3\x45\x03\xDE\x48\x8D\x0C\x80\x41\x8B\x54\x88\x10\x41\x0F\x10\x0C\x88\x41\x0F\x11\x04\x88\x41\x8B\x42\x10\x41\x89\x44\x88\x10\x41\x0F\x11\x0A\x41\x89\x52\x10\x4D\x8D\x52\x14\x45\x3B\xD9\x72\xA0\x8B\x87\x90\x00\x00\x00\x45\x33\xDB\x8B\xF0\x48\x03\xF3\x8B\x46\x0C\x85\xC0\x74\x7E\x8B\xC8\x48\x03\xCB\xFF\x55\xC7\x44\x8B\x36\x48\x8B\xF8\x44\x8B\x7E\x10\x4C\x03\xF3\x4C\x03\xFB\x49\x8B\x0E\x48\x85\xC9\x74\x35\x4C\x8B\x6D\xBF\x79\x0B\x0F\xB7\xD1\xEB\x0D\x44\x8B\x65\xB7\xEB\xC3\x48\x8D\x51\x02\x48\x03\xD3\x48\x8B\xCF\x41\xFF\xD5\x49\x83\xC6\x08\x49\x89\x07\x49\x83\xC7\x08\x49\x8B\x0E\x48\x85\xC9\x75\xD3\x44\x8B\x6D\xB3\x83\x7D\xB7\x00\x74\x14\xB8\x01\x00\x00\x00\x44\x3B\xE8\x76\x0A\x41\x69\xCC\xE8\x03\x00\x00\xFF\x55\xD7\x8B\x46\x20\x48\x83\xC6\x14\x85\xC0\x75\x86\x48\x8B\x7D\xCF\x4C\x8B\x6D\xBF\x45\x33\xE4\x44\x39\xA7\xF4\x00\x00\x00\x74\x70\x44\x8B\xB7\xF0\x00\x00\x00\x49\x83\xC6\x04\x4C\x03\xF3\x41\x8B\x06\x85\xC0\x74\x5B\x48\x8B\x7D\xC7\x8B\xC8\x48\x03\xCB\xFF\xD7\x41\x8B\x76\x08\x4C\x8B\xE0\x45\x8B\x7E\x0C\x48\x03\xF3\x4C\x03\xFB\xEB\x25\x49\x8B\x0F\x48\x85\xC9\x79\x05\x0F\xB7\xD1\xEB\x07\x48\x8D\x51\x02\x48\x03\xD3\x49\x8B\xCC\x41\xFF\xD5\x48\x89\x06\x48\x83\xC6\x08\x49\x83\xC7\x08\x48\x83\x3E\x00\x75\xD5\x49\x83\xC6\x20\x45\x33\xE4\x41\x8B\x06\x85\xC0\x75\xAD\x48\x8B\x7D\xCF\x48\x8B\xF3\x41\xB8\x02\x00\x00\x00\x48\x2B\x77\x30\x0F\x84\xC7\x00\x00\x00\x44\x39\xA7\xB4\x00\x00\x00\x0F\x84\xBA\x00\x00\x00\x44\x8B\x8F\xB0\x00\x00\x00\x4C\x03\xCB\x45\x39\x21\x0F\x84\xA7\x00\x00\x00\x41\xBF\xFF\x0F\x00\x00\x45\x8D\x70\xFF\x4D\x8D\x51\x08\xEB\x7B\x45\x0F\xB7\x1A\x41\x0F\xB7\xCB\x41\x0F\xB7\xC3\x66\xC1\xE9\x0C\x66\x83\xF9\x0A\x75\x21\x45\x8B\x01\x4D\x23\xDF\x4B\x8D\x04\x18\x48\x8B\x14\x18\x4B\x8D\x04\x18\x48\x03\xD6\x41\xB8\x02\x00\x00\x00\x48\x89\x14\x18\xEB\x41\x66\x83\xF9\x03\x75\x0B\x49\x23\xC7\x48\x8D\x0C\x03\x8B\xC6\xEB\x29\x66\x41\x3B\xCE\x75\x13\x49\x23\xC7\x48\x8D\x0C\x03\x48\x8B\xC6\x48\xC1\xE8\x10\x0F\xB7\xC0\xEB\x10\x66\x41\x3B\xC8\x75\x11\x49\x23\xC7\x48\x8D\x0C\x03\x0F\xB7\xC6\x41\x8B\x11\x48\x01\x04\x0A\x4D\x03\xD0\x41\x8B\x41\x04\x49\x03\xC1\x4C\x3B\xD0\x0F\x85\x75\xFF\xFF\xFF\x4D\x8B\xCA\x45\x39\x22\x0F\x85\x63\xFF\xFF\xFF\x0F\xB7\x77\x14\x45\x8B\xF4\x48\x83\xC6\x28\x41\xBD\x01\x00\x00\x00\x66\x44\x3B\x67\x06\x0F\x83\x03\x01\x00\x00\x4C\x8B\x7D\xDF\x48\x03\xF7\xBA\x00\x00\x00\x40\x44\x39\x26\x0F\x84\xDA\x00\x00\x00\x8B\x46\x14\x8B\xC8\x81\xE1\x00\x00\x00\x20\x75\x14\x85\xC2\x75\x10\x85\xC0\x78\x0C\x45\x8B\xC5\x44\x89\x6D\xAF\xE9\x8D\x00\x00\x00\x85\xC9\x75\x30\x85\xC2\x75\x0A\x85\xC0\x79\x06\x44\x8D\x41\x08\xEB\x58\x85\xC9\x75\x1E\x85\xC2\x74\x04\x85\xC0\x79\x4C\x85\xC9\x75\x12\x85\xC2\x74\x0A\x85\xC0\x79\x06\x44\x8D\x41\x04\xEB\x3A\x85\xC9\x74\x55\x85\xC2\x75\x0C\x85\xC0\x78\x08\x41\xB8\x10\x00\x00\x00\xEB\x26\x85\xC9\x74\x41\x85\xC2\x75\x0C\x85\xC0\x79\x08\x41\xB8\x80\x00\x00\x00\xEB\x12\x85\xC9\x74\x2D\x85\xC2\x74\x10\x85\xC0\x78\x0C\x41\xB8\x20\x00\x00\x00\x44\x89\x45\xAF\xEB\x1D\x85\xC9\x74\x15\x85\xC2\x74\x11\x44\x8B\x45\xAF\x85\xC0\xB9\x40\x00\x00\x00\x44\x0F\x48\xC1\xEB\xE1\x44\x8B\x45\xAF\xF7\x46\x14\x00\x00\x00\x04\x74\x09\x41\x0F\xBA\xE8\x09\x44\x89\x45\xAF\x8B\x4E\xFC\x4C\x8D\x4D\xAF\x8B\x16\x48\x03\xCB\x41\xFF\xD7\xBA\x00\x00\x00\x40\x41\xB8\x02\x00\x00\x00\x0F\xB7\x47\x06\x45\x03\xF5\x48\x83\xC6\x28\x44\x3B\xF0\x0F\x82\x09\xFF\xFF\xFF\x45\x33\xC0\x33\xD2\x48\x83\xC9\xFF\xFF\x55\xE7\x44\x39\xA7\xD4\x00\x00\x00\x74\x41\x8B\x87\xD0\x00\x00\x00\xBE\x07\x00\x00\x00\x4D\x8B\xFC\x4C\x8B\x74\x18\x18\x4C\x03\xF3\x49\x2B\xF6\x48\xC1\xEE\x03\x4D\x85\xF6\x49\x0F\x45\xF4\x48\x85\xF6\x74\x18\x45\x33\xC0\x41\x8B\xD5\x48\x8B\xCB\x41\xFF\x16\x4D\x03\xFD\x4D\x8D\x76\x08\x4C\x3B\xFE\x75\xE8\x8B\x47\x28\x4D\x8B\xC5\x48\x03\xC3\x41\x8B\xD5\x48\x8B\xCB\xFF\xD0\x8B\x75\x67\x85\xF6\x0F\x84\x8F\x00\x00\x00\x44\x39\xA7\x8C\x00\x00\x00\x0F\x84\x82\x00\x00\x00\x8B\x8F\x88\x00\x00\x00\x48\x03\xCB\x44\x8B\x59\x18\x45\x85\xDB\x74\x70\x44\x39\x61\x14\x74\x6A\x44\x8B\x49\x20\x41\x8B\xFC\x8B\x51\x24\x4C\x03\xCB\x48\x03\xD3\x45\x85\xDB\x74\x55\x45\x8B\x01\x45\x8B\xD4\x4C\x03\xC3\x74\x4A\xEB\x0D\x0F\xBE\xC0\x44\x03\xD0\x41\xC1\xCA\x0D\x4D\x03\xC5\x41\x8A\x00\x84\xC0\x75\xEC\x41\x3B\xF2\x75\x05\x48\x85\xD2\x75\x12\x41\x03\xFD\x49\x83\xC1\x04\x48\x83\xC2\x02\x41\x3B\xFB\x73\x1A\xEB\xC3\x8B\x49\x1C\x0F\xB7\x12\x48\x03\xCB\x8B\x04\x91\x8B\x55\x77\x48\x03\xC3\x48\x8B\x4D\x6F\xFF\xD0\x48\x8B\xC3\xEB\x02\x33\xC0\x48\x8B\x9C\x24\xD0\x00\x00\x00\x48\x81\xC4\x90\x00\x00\x00\x41\x5F\x41\x5E\x41\x5D\x41\x5C\x5F\x5E\x5D\xC3\xCC\x48\x8B\xC4\x48\x89\x58\x08\x48\x89\x68\x10\x48\x89\x70\x18\x48\x89\x78\x20\x41\x56\x48\x83\xEC\x10\x65\x48\x8B\x04\x25\x60\x00\x00\x00\x8B\xE9\x45\x33\xF6\x48\x8B\x50\x18\x4C\x8B\x4A\x10\x4D\x8B\x41\x30\x4D\x85\xC0\x0F\x84\xB3\x00\x00\x00\x41\x0F\x10\x41\x58\x49\x63\x40\x3C\x41\x8B\xD6\x4D\x8B\x09\xF3\x0F\x7F\x04\x24\x46\x8B\x9C\x00\x88\x00\x00\x00\x45\x85\xDB\x74\xD2\x48\x8B\x04\x24\x48\xC1\xE8\x10\x66\x44\x3B\xF0\x73\x22\x48\x8B\x4C\x24\x08\x44\x0F\xB7\xD0\x0F\xBE\x01\xC1\xCA\x0D\x80\x39\x61\x7C\x03\x83\xC2\xE0\x03\xD0\x48\xFF\xC1\x49\x83\xEA\x01\x75\xE7\x4F\x8D\x14\x18\x45\x8B\xDE\x41\x8B\x7A\x20\x49\x03\xF8\x45\x39\x72\x18\x76\x8E\x8B\x37\x41\x8B\xDE\x49\x03\xF0\x48\x8D\x7F\x04\x0F\xBE\x0E\x48\xFF\xC6\xC1\xCB\x0D\x03\xD9\x84\xC9\x75\xF1\x8D\x04\x13\x3B\xC5\x74\x0E\x41\xFF\xC3\x45\x3B\x5A\x18\x72\xD5\xE9\x5E\xFF\xFF\xFF\x41\x8B\x42\x24\x43\x8D\x0C\x1B\x49\x03\xC0\x0F\xB7\x14\x01\x41\x8B\x4A\x1C\x49\x03\xC8\x8B\x04\x91\x49\x03\xC0\xEB\x02\x33\xC0\x48\x8B\x5C\x24\x20\x48\x8B\x6C\x24\x28\x48\x8B\x74\x24\x30\x48\x8B\x7C\x24\x38\x48\x83\xC4\x10\x41\x5E\xC3"
    #MARKER:E
    
    if is64BitDLL(dllBytes):

        rdiShellcode = rdiShellcode64

        bootstrap = b''
        bootstrapSize = 64

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

        # Set the offset to our DLL from pop result
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)

        # pop rcx - Capture our current location in memory
        bootstrap += b'\x59'

        # mov r8, rcx - copy our location in memory to r8 before we start modifying RCX
        bootstrap += b'\x49\x89\xc8'

        # add rcx, <Offset of the DLL>
        bootstrap += b'\x48\x81\xc1'
        bootstrap += pack('I', dllOffset)

        # mov edx, <Hash of function>
        bootstrap += b'\xba'
        bootstrap += pack('I', functionHash)

        # Setup the location of our user data
        # add r8, <Offset of the DLL> + <Length of DLL>
        bootstrap += b'\x49\x81\xc0'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += pack('I', userDataLocation)

        # mov r9d, <Length of User Data>
        bootstrap += b'\x41\xb9'
        bootstrap += pack('I', len(userData))

        # push rsi - save original value
        bootstrap += b'\x56'

        # mov rsi, rsp - store our current stack pointer for later
        bootstrap += b'\x48\x89\xe6'

        # and rsp, 0x0FFFFFFFFFFFFFFF0 - Align the stack to 16 bytes
        bootstrap += b'\x48\x83\xe4\xf0'

        # sub rsp, 0x30 - Create some breathing room on the stack 
        bootstrap += b'\x48\x83\xec'
        bootstrap += b'\x30' # 32 bytes for shadow space + 8 bytes for last arg + 8 bytes for stack alignment

        # mov dword ptr [rsp + 0x20], <Flags> - Push arg 5 just above shadow space
        bootstrap += b'\xC7\x44\x24'
        bootstrap += b'\x20'
        bootstrap += pack('I', flags)

        # call - Transfer execution to the RDI
        bootstrap += b'\xe8'
        bootstrap += pack('b', bootstrapSize - len(bootstrap) - 4) # Skip over the remainder of instructions
        bootstrap += b'\x00\x00\x00'

        # mov rsp, rsi - Reset our original stack pointer
        bootstrap += b'\x48\x89\xf4'

        # pop rsi - Put things back where we left them
        bootstrap += b'\x5e'

        # ret - return to caller
        bootstrap += b'\xc3'

        if len(bootstrap) != bootstrapSize:
            raise Exception("x64 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    else: # 32 bit
        rdiShellcode = rdiShellcode32

        bootstrap = b''
        bootstrapSize = 46

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

        # Set the offset to our DLL from pop result
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)

        # pop eax - Capture our current location in memory
        bootstrap += b'\x58'

        # push ebp
        bootstrap += b'\x55'

        # mov ebp, esp
        bootstrap += b'\x89\xe5'

        # mov ebx, eax - copy our location in memory to ebx before we start modifying eax
        bootstrap += b'\x89\xc3'

        # add eax, <Offset to the DLL>
        bootstrap += b'\x05'
        bootstrap += pack('I', dllOffset)

        # add ebx, <Offset to the DLL> + <Size of DLL>
        bootstrap += b'\x81\xc3'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += pack('I', userDataLocation)

        # push <Flags>
        bootstrap += b'\x68'
        bootstrap += pack('I', flags)

        # push <Length of User Data>
        bootstrap += b'\x68'
        bootstrap += pack('I', len(userData))

        # push ebx
        bootstrap += b'\x53'

        # push <hash of function>
        bootstrap += b'\x68'
        bootstrap += pack('I', functionHash)

        # push eax
        bootstrap += b'\x50'

        # call - Transfer execution to the RDI
        bootstrap += b'\xe8'
        bootstrap += pack('b', bootstrapSize - len(bootstrap) - 4) # Skip over the remainder of instructions
        bootstrap += b'\x00\x00\x00'

        # leave
        bootstrap += b'\xc9'

        # ret - return to caller
        bootstrap += b'\xc3'

        if len(bootstrap) != bootstrapSize:
            raise Exception("x86 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    return False
