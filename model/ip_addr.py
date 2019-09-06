from model.base_model import BaseModel
from workflow.workflow import Item


class IPAddr(BaseModel):
    def __init__(self):
        self.name = u'ip'
        self.desc = u'IPv4 Address Converter'

    def convert(self, query):
        v = IPAddr.ipaddr_aton(query)
        return [Item(
            title=self.name + ': ' + query,
            subtitle=str(v),
            arg=self.name + u' IPv4: ' + str(v),
            valid=True,
            icon=self.icon_path()
        )]

    @staticmethod
    def ipaddr_aton(ipaddr):
        _tmp = ''
        lead_bit = True
        base = 10
        ipaddr_len = len(ipaddr)
        blk_count = 3
        bit_count = 0
        sum = 0
        for i, item in enumerate(ipaddr):
            if lead_bit:
                if item == '0':
                    base = 8
                elif item == 'x' or item == 'X':
                    base = 16
                    lead_bit = False
                    continue
                elif item == ' ':
                    continue
                else:
                    if bit_count == 0:
                        base = 10
                        lead_bit = False

            if item != '.':
                _tmp += item
                bit_count += 1

            if item == '.' or i + 1 == ipaddr_len:
                if blk_count < 0:
                    # exception
                    return 0

                if i + 1 == ipaddr_len and blk_count != 0:
                    blk_count = 0
                try:
                    blk_value = int(_tmp, base)
                except:
                    # exception
                    return 0

                if blk_value > 255:
                    # exception
                    return 0

                sum += blk_value << (8 * blk_count)
                lead_bit = True
                _tmp = ''
                blk_count -= 1
                bit_count = 0
        return sum
